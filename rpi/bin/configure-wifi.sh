#!/bin/bash

# -------------------
# Configure RPi3 WiFi
# -------------------

function configure()
{
  ssid=$1
  pass=$2
  echo "Configuring AP [$ssid]"
  sudo cat <<EOF > /etc/wpa_supplicant/wpa_supplicant.conf
network={
    ssid="$ssid"
    psk="$pass"
}
EOF
  echo "Restarting WiFi"
  sudo ifdown wlan0
  sudo ifup wlan0
  echo "Done"
}

function list() 
{
  sudo iwlist wlan0 scan | grep ESSID | cut -d':' -f2 | sed 's/"//g'
}

if [ $# -lt 1 ]
then
  echo "Usage: $0 [list|configure <ssid> <pass>]"
  exit 1
fi

if [ "$1" == "list" ]
then
  list
fi

if [ "$1" == "configure" ]
then
  if [ $# -lt 3 ]
  then
    echo "Usage: $0 configure <ssid> <pass>"
    exit 2
  fi
  configure $2 $3
fi
