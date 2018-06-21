#/bin/bash -e
#Install necessary packages
sudo apt-get install curl dnsmasq tcpdump vim debsums

#Add Google Chrome repo
sudo wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list

#Add Skype repo
sudo curl https://repo.skype.com/data/SKYPE-GPG-KEY | sudo apt-key add -
sudo echo "deb https://repo.skype.com/deb stable main" | sudo tee /etc/apt/sources.list.d/skypeforlinux.list

#Install the rest of the packages
sudo apt-get install openvpn skypeforlinux google-chrome

#Make the necessary configurations:

#DNSmasq configuration (addn-hosts, namesevers...., cache-size)
sudo cp dnsmasq.conf /etc/dnsmasq.conf

#iptables configuration

sudo iptables-restore < iptables.conf
sudo /etc/init.d/iptables save

#configuring SSHD
sudo cp sshd_config /etc/ssh/sshd_config

sudo /etc/init.d/ssh restart

#Remove auto updates
sudo echo 'APT::Periodic:Update-Package-Lists "0";' >> /etc/apt/apt.conf.d/10periodic

#Turn off hardware acceleration:
sudo cp disable-gpu.conf /etc/X11/xorg.conf.d/disable-gpu.conf



#Zabbix for Ubuntu 14.04 ^
sudo wget https://repo.zabbix.com/zabbix/2.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_2.4-1+trusty_all.deb
sudo dpkg -i zabbix-release_2.4-1+trusty_all.deb
sudo apt-get update
sudo apt-get install zabbix-agent zabbix-sender

#Monitoring
sudo echo 'deb http://mon.tb-pro.com/tb/pool/main/t/tbmon ./' > /etc/apt/sources.list.d/tbmon.list
sudo apt-get update
sudo apt-get install tbmon
