#!/bin/bash

./systemd_service_mon.py 2>> /var/log/tbmon/systemd_service_mon.log | /usr/share/tbmon2/bin/monjson2zbx.pl --once -s `/bin/cat /etc/tbmon_server` -u api_user -p `/bin/cat /etc/zbx_api_auth` -h `/bin/hostname` -f /var/tmp/systemd_service_mon_f.json 2>> /var/log/tbmon/monjson2zbx.log | /usr/bin/zabbix_sender -z `/bin/cat /etc/zabbix/zabbix_agentd.d/01-tbmon-*-server.conf | /bin/grep -ioP "ServerActive=\K.*\.\d+"` -s `/bin/hostname` -T -i -
