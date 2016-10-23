#!/bin/bash

# -------------------
# Configure RPi3 WiFi
# -------------------

function configure()
{
  mode=$1
  ssid=$2
  pass=$3
  if [ ! -f ../etc/interfaces.$mode ]
  then
    echo "Mode [$mode] non supporte. Utiliser les modes wep ou wpa."
    exit 4
  fi
  echo "Configuring [$mode] AP [$ssid]"
  
  case "$mode" in
  "wpa")
    echo "Wpa"
    sudo cat <<EOF > /etc/wpa_supplicant/wpa_supplicant.conf
network={
    ssid="$ssid"
    psk="$pass"
}
EOF
    sudo cp ../etc/interfaces.$mode /etc/network/interfaces
    ;;
  "wep")
    echo "Wep"
    sudo cat ../etc/interfaces.$mode | sed "s/ESSID/$ssid/" | sed "s/PASS/$pass/" | sudo tee /etc/network/interfaces
    ;;
  *)
    echo "Mode [$mode] non supporte. Utiliser les modes web ou wpa"
    exit 4
    ;;
  esac

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
  echo "Usage: $0 [list|configure <mode> <ssid> <pass>]"
  exit 1
fi

if [ "$1" == "list" ]
then
  list
fi

if [ "$1" == "configure" ]
then
  if [ $# -lt 4 ]
  then
    echo "Usage: $0 configure <mode> <ssid> <pass>"
    exit 2
  fi
  configure $2 $3 $4
fi
