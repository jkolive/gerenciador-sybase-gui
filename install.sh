#!/usr/bin/env bash

install -o $USER -d /opt/sybase
# Fonte dos binários ( Domínio Sistemas )
# http://download.dominiosistemas.com.br/instalacao/diversos/sybase16_linux_64/ASA-1600-2747-Linux-64.tar.gz
# tar -xvf ASA-1600-2747-Linux-64.tar.gz -C /opt/sybase --strip-components=1 > /dev/null 2>&1
cp -R bin/sybase/* /opt/sybase
chmod +x -R /opt/sybase/SYBSsa16/bin64

cat /proc/version | grep "Ubuntu"

if [ $? -eq 0 ]; then

  # Depedências
  apt install jq -y > /dev/null 2>&1

fi

cat /proc/version | grep "Red Hat"

if [ $? -eq 0 ]; then

  # Dependência
  yum install jq -y > /dev/null 2>&1

fi
