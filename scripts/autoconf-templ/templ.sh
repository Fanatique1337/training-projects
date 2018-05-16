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
echo 'bind-interfaces' >> /etc/dnsmasq.conf
echo 'listen-address=127.0.0.1' >> /etc/dnsmasq.conf
echo 'cache-size=1024' >> /etc/dnsmasq.conf
echo 'server=8.8.8.8' >> /etc/dnsmasq.conf
echo 'server=8.8.8.4' >> /etc/dnsmasq.conf
echo 'server=212.73.140.66' >> /etc/dnsmasq.conf
echo 'server=78.128.126.1' >> /etc/dnsmasq.conf
echo 'bogus-priv' >> /etc/dnsmasq.conf
echo 'neg-ttl=86400' >> /etc/dnsmasq.conf
echo 'domain-needed' >> /etc/dnsmasq.conf

#iptables configuration
cd $HOME
echo <<EOT >> iptables.txt
# set default policy to drop
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP

# allow loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# drop invalid packets
iptables -A INPUT  -m state --state INVALID -j DROP
iptables -A OUTPUT -m state --state INVALID -j DROP
iptables -A FORWARD -m state --state INVALID -j DROP

# allow established, related packets we've already seen
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

iptables -A INPUT -p tcp -m tcp --dport (SSH port) -m comment --comment "SSH" -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 53 -m comment --comment "DNS-TCP" -j ACCEPT
iptables -A INPUT -p udp -m udp --dport 53 -m comment --comment "DNS-UDP" -j ACCEPT
iptables -A INPUT -p udp -m udp --dport 67:68 -m comment --comment "DHCP" -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 443 -m comment --comment "HTTPS" -j ACCEPT


# allow icmp packets (e.g. ping...)
iptables -A INPUT -p icmp -m state --state NEW -j ACCEPT
EOT
iptables-restore < iptables.txt
/etc/init.d/iptables save

#configuring SSHD
cat <<EOT >> /etc/sshd_config
AllowUsers *@10.*
AllowUsers *@192.168.*

PasswordAuthentication yes
PermitEmptyPasswords no
PermitRootLogin no
Port 7822
PubkeyAuthentication yes
RSAAuthentication yes
UseDNS no
X11Forwarding no

ClientAliveInterval 3600
ClientAliveCountMax 0
EOT

/etc/init.d/ssh restart

#Remove auto updates
echo 'APT::Periodic:Update-Package-Lists "0";' >> /etc/apt/apt.conf.d/10periodic

#Turn off hardware acceleration:
echo ‘Section "Extensions"’ > /etc/X11/xorg.conf.d/disable-gpu.conf
echo ‘\tOption "GLX" "Disable"’ > /etc/X11/xorg.conf.d/disable-gpu.conf
echo ‘EndSection’ > /etc/X11/xorg.conf.d/disable-gpu.conf



#Zabbix for Ubuntu 14.04 ^
wget https://repo.zabbix.com/zabbix/2.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_2.4-1+trusty_all.deb
dpkg -i zabbix-release_2.4-1+trusty_all.deb
apt-get update
apt-get install zabbix-agent zabbix-sender

#Monitoring
echo 'deb http://mon.tb-pro.com/tb/pool/main/t/tbmon ./' > /etc/apt/sources.list.d/tbmon.list
apt-get update
apt-get install tbmon
