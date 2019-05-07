from ftplib import FTP_TLS


def upload_file_tls(host, user, password, local_path, remote_path, timeout=None):
    ftp = FTP_TLS(host=host, user=user, passwd=password, timeout=timeout)
    ftp.prot_p()
    local_file = open(local_path, 'rb')
    ftp.storbinary('STOR {}'.format(remote_path), local_file)
    local_file.close()
    ftp.quit()


def download_file_tls(host, user, password, local_path, remote_path, timeout=None):
    ftp = FTP_TLS(host=host, user=user, passwd=password, timeout=timeout)
    ftp.prot_p()
    ftp.retrbinary('RETR {}'.format(remote_path), open(local_path, 'wb').write)
    ftp.quit()
