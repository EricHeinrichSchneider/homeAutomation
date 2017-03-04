# Move file to systemd folder
sudo cp myscript.service /lib/systemd/system/homeAutomation.service
# Permission for service file
sudo chmod 644 /lib/systemd/system/homeAutomation.service
# reload services
sudo systemctl daemon-reload
# enable service
sudo systemctl enable homeAutomation.service
#check status
sudo systemctl status homeAutomation.service
