#!/usr/bin/env bash
apt-get install -y python3-dev # python3-dev
apt-get install -y libmysqlclient-dev
apt-get install -y python-mysqldb

# signxml
apt-get install -y python3-cffi
apt-get install -y libxml2-dev
apt-get install -y libxslt1-dev
apt-get install -y libssl-dev
apt-get install -y python3-lxml
apt-get install -y python3-cryptography
apt-get install -y python3-openssl
apt-get install -y python3-certifi
apt-get install -y python3-defusedxml

# xmlsec
apt-get install -y python3-libxml2
apt-get install -y libxmlsec1-dev
apt-get install -y pkg-config
apt-get install -y libxml-security-c-dev
apt-get install -y xmlsec1
