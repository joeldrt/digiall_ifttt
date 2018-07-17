# digiall_ifttt

API for ifttt using skylinknet products

for installing as service in digital-ocean droplet

edit da_ifttt_api.service file
- all parts marked with !!!! should be replaced with indicated value
- move da_ifttt_api.service file to /etc/systemd/system/

start service
- $ sudo systemctl start da_ifttt_api
- $ sudo systemctl enable da_ifttt_api