#!/bin/bash

echo "This setup script is meant to work on Ubuntu (and similar) distros (using APT)."
while true
do
      read -r -p "Install masscan? (do this if this is the first time running) [Y/n] " input

      case $input in
            [yY][eE][sS]|[yY])
                  apt install masscan
                  wget https://raw.githubusercontent.com/robertdavidgraham/masscan/master/data/exclude.conf
                  echo "Installation Complete."
                  break
                  ;;
            [nN][oO]|[nN])
                  echo "Continuing..."
                  break
                  ;;
            *)
                  echo "Invalid input..."
                  ;;
      esac
done

while true
do
      read -r -p "Begin scanning? Note, this will take a while. [Y/n] " input

      case $input in
            [yY][eE][sS]|[yY])
                  echo "Beginning Scan..."

                  if (($# > 0)); then
                    masscan -p25565 0.0.0.0/0 --max-rate "$1" --excludefile exclude.conf -oL masscan.txt
                  else
                    masscan -p25565 0.0.0.0/0 --max-rate 3079  --excludefile exclude.conf -oL masscan.txt
                  fi

                  echo "Scan Complete."

                  break
                  ;;
            [nN][oO]|[nN])
                  if test -f masscan.txt
                  then
                    echo "masscan.txt exists, continuing to mcscanner stage."
                  else
                    echo "Exiting..."
                    exit 0
                  fi

                  break
                  ;;
            *)
                  echo "Invalid input..."
                  ;;
      esac
done

apt install python3 python3-pip

pip install mcstatus

echo "Setup Complete. "
while true
do
      read -r -p "Launch minecraft server scanner? [Y/n] " input

      case $input in
            [yY][eE][sS]|[yY])
                  python3 mcscanner.py
                  echo "Scan Complete."
                  break
                  ;;
            [nN][oO]|[nN])
                  echo "Exiting..."
                  break
                  ;;
            *)
                  echo "Invalid input..."
                  ;;
      esac
done

