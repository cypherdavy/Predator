#!/bin/bash
pip3 install -r requirements.txt
mkdir -p ~/.predator/templates
cp -r templates/* ~/.predator/templates/
echo "alias predator='python3 -m predator'" >> ~/.bashrc
source ~/.bashrc
