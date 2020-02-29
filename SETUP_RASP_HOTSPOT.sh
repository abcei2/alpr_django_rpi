
SSID=LPR2020
PASS=LPR2020

sudo apt install -y dnsmasq hostapd
sudo systemctl stop dnsmasq
sudo systemctl stop hostapd

grep -R "interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_suppliant" /etc/dhcpcd.conf >> var    
if [ $(wc -l var) -eq 0 ]; then 
    echo "interface wlan0
        static ip_address=192.168.4.1/24
        nohook wpa_supplicant" >> /etc/dhcpcd.conf
else
    echo "/etc/dhcpcd.conf already setup"
    #cat /etc/dhcpcd.conf
fi

sudo service dhcpcd restart
    
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig

FILE=/etc/dnsmasq.conf
CONTENT="interface=wlan0      # Use the require wireless interface - usually wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h"
if test -f "$FILE"; then
    grep -R CONTENT $FILE >> var
    if [ $(wc -l var) -eq 0 ]; then 
        echo CONTENT >> $FILE
    else
        echo "$FILE already setup"
        #cat $FILE
    fi
fi

sudo systemctl start dnsmasq

FILE=/etc/hostapd/hostapd.conf
CONTENT="interface=wlan0
driver=nl80211
ssid=$SSID
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=$PASS
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP"
if test -f "$FILE"; then
    grep -R CONTENT $FILE >> var
    if [ $(wc -l var) -eq 0 ]; then 
        echo CONTENT >> $FILE
    else
        echo "$FILE already setup"
        cat $FILE
    fi
fi

FILE=/etc/default/hostapd
CONTENT="DAEMON_CONF=\"/etc/hostapd/hostapd.conf\""

if test -f "$FILE"; then
    grep -R CONTENT $FILE >> var
    if [ $(wc -l var) -eq 0 ]; then 
        sudo echo CONTENT >> $FILE
    else
        echo "$FILE already setup"
        #cat $FILE
    fi
else
    echo "EXISTs"
fi

sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
sudo systemctl status hostapd
sudo systemctl status dnsmasq 
#url: https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md
