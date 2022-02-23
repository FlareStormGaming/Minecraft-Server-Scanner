#!/bin/bash

echo "This setup script is meant to work on Ubuntu (and similar) distros (using APT)."
apt install masscan
wget https://raw.githubusercontent.com/robertdavidgraham/masscan/master/data/exclude.conf

if (($# > 0)); then
  masscan -p25565 0.0.0.0/0 --max-rate "$1" --excludefile exclude.conf -oL masscan.txt
else
  masscan -p25565 0.0.0.0/0 --max-rate 3079  --excludefile exclude.conf -oL masscan.txt
fi

pip install mcstatus