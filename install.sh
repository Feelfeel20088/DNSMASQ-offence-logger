sudo systemctl daemon-reload  
sudo systemctl enable dnsmasq-logger.timer  
sudo systemctl start dnsmasq-logger.timer  
sudo systemctl status dnsmasq-logger.timer
