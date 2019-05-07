import csv
from io import StringIO

import pandas
from django.http.response import StreamingHttpResponse

from common.constants import FileType


class Echo(object):
    """An object that implements just the write method of the file-like interface."""

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


class CsvStreamingHttpResponse(StreamingHttpResponse):
    CONTENT_TYPE = 'text/csv'
    FILE_EXTENSION = '.csv'
    # FORCE_UTF8_ENCODING = True
    FORCE_ONE_LINE_ROW = True

    def __init__(self, filename, rows, header=None, row_transformer=None, *args, **kwargs):
        self.filename = filename
        self.header = header
        self.rows = rows
        self.row_transformer = row_transformer
        kwargs.pop('content_type', None)  # ignore content type
        super(CsvStreamingHttpResponse, self).__init__(self.streaming_content_generator(),
                                                       content_type=self.CONTENT_TYPE,
                                                       *args, **kwargs)
        if not filename.lower().endswith(self.FILE_EXTENSION.lower()):
            filename += self.FILE_EXTENSION
        self['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    def streaming_content_generator(self):
        writer = csv.writer(Echo())
        return (writer.writerow(row) for row in self.content_generator())

    def content_generator(self):
        if self.header:
            yield self.header
        for row in self.rows:
            if self.row_transformer is not None:
                row = self.row_transformer(row)
            # if self.FORCE_UTF8_ENCODING is True:
            #     row = map(self.force_utf8_encoding, row)
            if self.FORCE_ONE_LINE_ROW is True:
                row = map(self.force_one_line_text, row)
            yield row

    # @staticmethod
    # def force_utf8_encoding(value):
    #     if isinstance(value, unicode):
    #         return value.encode('utf8')
    #     return value

    @staticmethod
    def force_one_line_text(value):
        if isinstance(value, (str, bytes)):
            return value.replace('\r\n', ' ').replace('\n', ' ')
        return value


class ExcelStreamingHttpResponse(CsvStreamingHttpResponse):
    CONTENT_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    FILE_EXTENSION = '.xlsx'
    FORCE_UTF8_ENCODING = False
    FORCE_ONE_LINE_ROW = False

    def streaming_content_generator(self):
        sio = StringIO()
        data_frame = pandas.DataFrame(self.content_generator())
        # noinspection PyTypeChecker
        writer = pandas.ExcelWriter(sio, engine='xlsxwriter')
        data_frame.to_excel(writer, header=False, index=False)
        writer.save()
        sio.seek(0)
        workbook = sio.getvalue()
        return workbook


class StreamingHttpResponseFactory(object):
    @staticmethod
    def get(content_type, filename, rows, header=None, row_transformer=None, *args, **kwargs):
        if content_type == FileType.CSV:
            return CsvStreamingHttpResponse(filename, rows, header, row_transformer, *args, **kwargs)
        elif content_type == FileType.XLSX:
            return ExcelStreamingHttpResponse(filename, rows, header, row_transformer, *args, **kwargs)
