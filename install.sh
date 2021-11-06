#!/bin/bash

# Set install directory
install_dir="$HOME/.local/bin"

# Set directory for config file
config_dir="$HOME/.config/tasker"

# Set bin as executable
chmod +x scan_dir.py

# Check if directory exist, else create them
if [[ ! -d "$install_dir" ]]; then
    mkdir "$install_dir"
fi
if [[ ! -d "$config_dir" ]]; then
    mkdir "$config_dir"
fi

# Then, copy the files
cp scan_dir.py "$install_dir"/scan_dir
cp config.yml "$config_dir"/

# Add to cron:
#write out current crontab
crontab -l > mycron
#echo new cron into cron file
#echo "@daily scan_dir" >> mycron
echo "* * * * * python3 $install_dir/scan_dir -v" >> mycron
#install new cron file
crontab mycron
rm mycron
