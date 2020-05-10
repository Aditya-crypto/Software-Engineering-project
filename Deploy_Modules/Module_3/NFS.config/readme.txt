server side:

ServerConfig.sh
sudo ufw allow from (clientIP) to any port nfs
sudo ufw status
   if status is inactive:
        sudo ufw enable
 client Machine:
 
 ClientConfig.sh
 sudo mount (serverIP):/mnt/sharedfolder /server
  OR

 sudo mount -t nfs (serverIP):/mnt/sharedfolder /server
