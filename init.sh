#!/usr/bin/env bash

# JQ variaveis
srvnome=$(cat .data.json | jq -r '.banco[].nome_servidor')
mem_cache=$(cat .data.json | jq -r '.banco[].mem_cache')M
param_redes=$(cat .data.json | jq -r '.banco[].param_redes')
param_servidor=$(cat .data.json | jq -r '.banco[].param_servidor')
automatico=$(cat .data.json | jq -r '.banco[].automatico')
desativado=$(cat .data.json | jq -r '.banco[].desativado')
caminho=$(cat .data.json | jq -r '.banco[].caminho')
nome_arquivo=$(cat .data.json | jq -r '.banco[].nome_arquivo')

cat /proc/version | grep "Ubuntu"

if [ $? -eq 0 ]; then

  # Inicialização DEB
  touch /etc/init.d/startDomsis.sh
  chmod +x /etc/init.d/startDomsis.sh
  cat <<- EOF > /etc/init.d/startDomsis.sh
#!/bin/bash
### BEGIN INIT INFO
# Provides: SQL Anywhere
# Required-Start: $remote_fs $syslog
# Required-Stop:  $remote_fs $syslog
# Default-Start:  2 3 4 5
# Default-Stop:   0 1 6
# Short-Description: Start daemon at boot time
# Description: Enable service provided by daemon.
### END INIT INFO
source /opt/sybase/bin64/setenv > /dev/null 2>&1
echo 'Liberando porta 2638 no firewall'
iptables -D INPUT -p tcp --dport 2638 -j ACCEPT > /dev/null 2>&1
iptables -I INPUT -p tcp --dport 2638 -j ACCEPT
iptables -D INPUT -p udp --dport 2638 -j ACCEPT > /dev/null 2>&1
iptables -I INPUT -p udp --dport 2638 -j ACCEPT
echo 'Iniciando o servidor...'
dbsrv16 $param_redes $param_servidor -c $mem_cache -n $srvnome -ud -o '$caminho/log/logservidor.txt' '$caminho/$nome_arquivo' >>/etc/init.d/startDomsis.sh

# Comando para inicialização do sistema
update-rc.d startDomsis.sh defaults > /dev/null 2>&1
EOF
fi

cat /proc/version | grep "Red Hat"

if [ $? -eq 0 ]; then

  # Inicialização RPM
  touch /etc/init.d/startDomsis.sh
  chmod +x /etc/init.d/startDomsis.sh
  cat <<- EOF > /etc/init.d/startDomsis.sh
#!/bin/bash
# chkconfig: 345 99 10
# description: Domsis
source /opt/sybase/SYBSsa16/bin64/setenv > /dev/null 2>&1
echo 'Liberando porta 2638 no firewall'
firewall-cmd --permanent --zone=public --remove-port=2638/tcp
firewall-cmd --permanent --zone=public --remove-port=2638/udp
firewall-cmd --permanent --zone=public --add-port=2638/tcp
firewall-cmd --permanent --zone=public --add-port=2638/udp
systemctl restart firewalld.service
echo 'Iniciando o servidor...'
dbsrv16 $param_redes $param_servidor -c $mem_cache -n $srvnome -ud -o '$caminho/log/logservidor.txt' '$caminho/$nome_arquivo' >>/etc/init.d/startDomsis.sh
EOF
  cd /etc/init.d/
  chkconfig --add startDomsis.sh >/dev/null 2>&1
  chkconfig --level 235 startDomsis.sh on >/dev/null 2>&1
fi