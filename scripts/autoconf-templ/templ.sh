#/bin/bash -e
#Install necessary packages
apt-get install curl dnsmasq postfix tcpdump vim debsums

#Add Google Chrome repo
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list

#Add Skype repo
curl https://repo.skype.com/data/SKYPE-GPG-KEY | sudo apt-key add -
echo "deb https://repo.skype.com/deb stable main" | sudo tee /etc/apt/sources.list.d/skypeforlinux.list

#Install the rest of the packages
apt-get install openvpn skypeforlinux google-chrome

#Make the necessary configurations:

#DNSmasq configuration (addn-hosts, namesevers...., cache-size)
cp dnsmasq.conf /etc/dnsmasq.conf

#iptables configuration

iptables-restore < iptables.conf
/etc/init.d/iptables save

#configuring SSHD
cp sshd_config /etc/ssh/sshd_config

/etc/init.d/ssh restart

#Remove auto updates
echo 'APT::Periodic:Update-Package-Lists "0";' >> /etc/apt/apt.conf.d/10periodic

#Turn off hardware acceleration:
cp disable-gpu.conf /etc/X11/xorg.conf.d/disable-gpu.conf



#Zabbix for Ubuntu 14.04 ^
wget https://repo.zabbix.com/zabbix/2.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_2.4-1+trusty_all.deb
dpkg -i zabbix-release_2.4-1+trusty_all.deb
apt-get update
apt-get install zabbix-agent zabbix-sender

#Monitoring
echo 'deb http://mon.tb-pro.com/tb/pool/main/t/tbmon ./' > /etc/apt/sources.list.d/tbmon.list
apt-get update
apt-get install tbmon
