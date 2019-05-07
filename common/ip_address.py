import ipaddress
import socket


def get_ipv4(ip4_or_hostname):
    """
    Get IP address version 4 by IP or Hostname
    :param ip4_or_hostname: IP or Hostname
    :return: IP version 4
    """
    ipv4 = socket.gethostbyname(ip4_or_hostname)
    return ipv4


def is_in_network(ip, ip_network):
    """
    Check if an IP address is in network or not
    :param ip: IP address need checking
    :param ip_network: IP Network, allow all 0.0.0.0 or 0.0.0.0/0
    :return: True or False
    """
    if ip_network == '0.0.0.0' or ip_network == '0.0.0.0/0':
        return True
    return ipaddress.ip_address(ip) in ipaddress.ip_network(ip_network)


def is_in_list(ip, ip_list):
    """
    Check if an IP address is in a list or not
    :param ip: IP Address need checking
    :param ip_list: IP list, can be network or specify IP
    :return: True or False
    """
    for ip_range in ip_list:
        if is_in_network(ip, ip_range):
            return True
    return False
