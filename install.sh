#!/bin/bash

# Set install directory
install_dir_bin="$HOME/.local/bin"
install_dir_service_menu="$HOME/.local/share/kservices5/"

# Set directory for config file
config_dir="$HOME/.config/tasker"

# Set bin as executable
chmod +x scan_dir.py

# Check if directory exist, else create them
if [[ ! -d "$install_dir_bin" ]]; then
    mkdir "$install_dir_bin"
fi
if [[ ! -d "$install_dir_service_menu" ]]; then
    mkdir "$install_dir_service_menu"
fi
if [[ ! -d "$config_dir" ]]; then
    mkdir "$config_dir"
fi

# Then, copy the files
cp scan_dir.py "$install_dir_bin"/scan_dir
cp addTask.desktop "$install_dir_service_menu"/addTask.desktop
cp config.yml "$config_dir"/

# Add to cron:
#write out current crontab
crontab -l > mycron
#echo new cron into cron file
#echo "@daily scan_dir" >> mycron
echo "* * * * * python3 $install_dir_bin/scan_dir -v" >> mycron
#install new cron file
crontab mycron
rm mycron
