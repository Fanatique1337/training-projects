#/bin/bash -e
#Remove auto updates
echo 'APT::Periodic:Update-Package-Lists "0";' >> /etc/apt/apt.conf.d/10periodic

#Add Google Chrome repo
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list

#Add Skype repo
apt-get install curl
curl https://repo.skype.com/data/SKYPE-GPG-KEY | sudo apt-key add -
echo "deb https://repo.skype.com/deb stable main" | sudo tee /etc/apt/sources.list.d/skypeforlinux.list


apt-get install openvpn chromium google-chrome-stable skypeforlinux dnsmasq postfix tcpdump vim debsums

#DNSmasq configuration (addn-hosts, namesevers...., cache-size)
echo 'listen-address=127.0.0.1' >> /etc/dnsmasq.conf
echo 'cache-size=2000' >> /etc/dnsmasq.conf
echo 'server=8.8.8.8' >> /etc/dnsmasq.conf
echo 'server=8.8.8.4' >> /etc/dnsmasq.conf
echo 'server=62.176.126.3' >> /etc/dnsmasq.conf
echo 'addn-hosts=/tmp/adblocks' >> /etc/dnsmasq.conf

#Zabbix for Ubuntu 14.04 ^


wget https://repo.zabbix.com/zabbix/2.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_2.4-1+trusty_all.deb
dpkg -i zabbix-release_2.4-1+trusty_all.deb
apt-get update
apt-get install zabbix-agent zabbix-sender

#Monitoring

echo 'deb http://mon.tb-pro.com/tb/pool/main/t/tbmon ./' > /etc/apt/sources.list.d/tbmon.list
apt-get update
apt-get install tbmon
