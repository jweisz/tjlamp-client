#!/bin/sh
sudo cp tjlamp.service /etc/systemd/system
sudo chmod 644 /etc/systemd/system/tjlamp.service
sudo systemctl daemon-reload
sudo systemctl enable tjlamp
echo "service installed! execute 'systemctl start tjlamp' to run the service"
echo "and make sure tjlamp-client is installed at /home/pi/Desktop/tjlamp-client/"
echo "(or update /etc/systemd/system/tjlamp.service with the right path)"
