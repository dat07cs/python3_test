import datetime

from rest_framework_xml import parsers


class XMLParser(parsers.XMLParser):
    def _type_convert(self, value):
        """
        Converts the value returned by the XMl parse into the equivalent
        Python type
        NOTE: try to convert datetime only
        """
        if value is None:
            return value

        try:
            return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            pass

        return value


class XMLWithRawParser(XMLParser):
    convert_started = False

    def _xml_convert(self, element):
        is_root_element = not self.convert_started
        if is_root_element:  # get root element only
            try:
                from defusedxml import ElementTree
                self.raw_xml = ElementTree.tostring(element)
            except:
                pass
            self.convert_started = True

        data = super(XMLParser, self)._xml_convert(element)
        if is_root_element and isinstance(data, dict):
            try:
                from defusedxml import ElementTree
                data['__raw_xml'] = ElementTree.tostring(element)
            except:
                pass
            self.convert_started = True
        return data
