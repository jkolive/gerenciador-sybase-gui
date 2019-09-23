#!/bin/bash
install -o $USER -d /opt/sybase
wget -c -P /tmp http://download.dominiosistemas.com.br/instalacao/diversos/sybase16_linux_64/ASA-1600-2747-Linux-64.tar.gz
tar -xvf /tmp/ASA-1600-2747-Linux-64.tar.gz -C /opt/sybase --strip-components=1 > /dev/null 2>&1
chmod +x -R /opt/sybase/SYBSsa16/bin64

# JQ variaveis
srvnome=$(cat .data.json | jq -r '.banco[].nome_servidor')
mem_cache=$(cat .data.json | jq -r '.banco[].mem_cache')
param_redes=$(cat .data.json | jq -r '.banco[].param_redes')
param_servidor=$(cat .data.json | jq -r '.banco[].param_servidor')
automatico=$(cat .data.json | jq -r '.banco[].automatico')
desativado=$(cat .data.json | jq -r '.banco[].desativado')
caminho=$(cat .data.json | jq -r '.banco[].caminho')
nome_arquivo=$(cat .data.json | jq -r '.banco[].nome_arquivo')


# Environment
touch /etc/profile.d/domsis.sh
chmod +x /etc/profile.d/domsis.sh
cat << EOF > /etc/profile.d/domsis.sh
#!/bin/bash
PATH="$PATH:/opt/sybase/SYBSsa16/bin64"
LD_LIBRARY_PATH="/opt/sybase/SYBSsa16/lib64"
export PATH LD_LIBRARY_PATH
export PATH="$PATH:/opt/sybase/SYBSsa16/bin64"
EOF

source /opt/sybase/SYBSsa16/bin64/setenv

cat /proc/version | grep "Ubuntu"

if [ $? -eq 0 ]; then

  # Depedências
  apt install jq -y > /dev/null 2>&1

  # Inicialização DEB
  touch /etc/init.d/startDomsis.sh
  chmod +x /etc/init.d/startDomsis.sh
  echo '#!/bin/bash' >>/etc/init.d/startDomsis.sh
  echo '### BEGIN INIT INFO' >>/etc/init.d/startDomsis.sh
  echo '# Provides: SQL Anywhere' >>/etc/init.d/startDomsis.sh
  echo '# Required-Start: $remote_fs $syslog' >>/etc/init.d/startDomsis.sh
  echo '# Required-Stop:  $remote_fs $syslog' >>/etc/init.d/startDomsis.sh
  echo '# Default-Start:  2 3 4 5' >>/etc/init.d/startDomsis.sh
  echo '# Default-Stop:   0 1 6' >>/etc/init.d/startDomsis.sh
  echo '# Short-Description: Start daemon at boot time' >>/etc/init.d/startDomsis.sh
  echo '# Description: Enable service provided by daemon.' >>/etc/init.d/startDomsis.sh
  echo '### END INIT INFO' >>/etc/init.d/startDomsis.sh
  echo 'source /opt/sybase/bin64/setenv > /dev/null 2>&1' >>/etc/init.d/startDomsis.sh
  echo 'echo 'Liberando porta 2638 no firewall'' >>/etc/init.d/startDomsis.sh
  echo 'iptables -D INPUT -p tcp --dport 2638 -j ACCEPT > /dev/null 2>&1' >>/etc/init.d/startDomsis.sh
  echo 'iptables -I INPUT -p tcp --dport 2638 -j ACCEPT' >>/etc/init.d/startDomsis.sh
  echo 'iptables -D INPUT -p udp --dport 2638 -j ACCEPT > /dev/null 2>&1' >>/etc/init.d/startDomsis.sh
  echo 'iptables -I INPUT -p udp --dport 2638 -j ACCEPT' >>/etc/init.d/startDomsis.sh
  echo 'echo 'Iniciando o servidor...'' >>/etc/init.d/startDomsis.sh
  echo "dbsrv16 -c "$mem_cache"M -n $srvnome -ud -o '$caminho/log/logservidor.txt' '$caminho/$nome_arquivo'" >>/etc/init.d/startDomsis.sh

  # Comando para inicialização do sistema
  update-rc.d startDomsis.sh defaults > /dev/null 2>&1
fi

cat /proc/version | grep "Red Hat"

if [ $? -eq 0 ]; then

  # Dependência
  yum install jq -y > /dev/null 2>&1

  # Inicialização RPM
  touch /etc/init.d/startDomsis.sh
  chmod +x /etc/init.d/startDomsis.sh
  echo '#!/bin/bash' >>/etc/init.d/startDomsis.sh
  echo '# chkconfig: 345 99 10' >>/etc/init.d/startDomsis.sh
  echo '# description: Domsis' >>/etc/init.d/startDomsis.sh
  echo 'source /opt/sybase/SYBSsa16/bin64/setenv > /dev/null 2>&1' >>/etc/init.d/startDomsis.sh
  echo 'echo 'Liberando porta 2638 no firewall'' >>/etc/init.d/startDomsis.sh
  echo 'firewall-cmd --permanent --zone=public --remove-port=2638/tcp' >>/etc/init.d/startDomsis.sh
  echo 'firewall-cmd --permanent --zone=public --remove-port=2638/udp' >>/etc/init.d/startDomsis.sh
  echo 'firewall-cmd --permanent --zone=public --add-port=2638/tcp' >>/etc/init.d/startDomsis.sh
  echo 'firewall-cmd --permanent --zone=public --add-port=2638/udp' >>/etc/init.d/startDomsis.sh
  echo 'systemctl restart firewalld.service' >>/etc/init.d/startDomsis.sh
  echo 'echo 'Iniciando o servidor...'' >>/etc/init.d/startDomsis.sh
  echo "dbsrv16 -c "$mem_cache"M -n $srvnome -ud -o '$caminho/log/logservidor.txt' '$caminho/$nome_arquivo'" >>/etc/init.d/startDomsis.sh
  cd /etc/init.d/
  chkconfig --add startDomsis.sh >/dev/null 2>&1
  chkconfig --level 235 startDomsis.sh on >/dev/null 2>&1
fi
