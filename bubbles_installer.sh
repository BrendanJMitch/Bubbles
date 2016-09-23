#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi


apt-get install python
apt-get install python-pygame
wget https://github.com/avarog/Bubbles/raw/master/bubbles_1.1.1.tar.gz -O ~/Downloads/bubbles_1.1.1.tar.gz
chmod +x ~/Downloads/bubbles_1.1.1.tar.gz
tar -xvzf ~/Downloads/bubbles_1.1.1.tar.gz -C /usr/games
mv /usr/games/Bubbles ~/Desktop
chmod +x ~/Desktop/Bubbles
gvfs-set-attribute -t string ~/Desktop/Bubbles metadata::custom-icon file:///usr/games/3redballs.png
