sudo apt-get update
sudo apt install nfs-kernel-server
mkdir mnt
cd mnt
mkdir sharedfolder
cd
sudo chown nobody:nogroup mnt/sharedfolder
sudo chmod 777 mnt/sharedfolder
sudo chmod 777 /etc/exports
echo '/mnt/newfolder *(rw,sync,no_subtree_check)' >> /etc/exports
sudo exportfs -a
showmount -e
sudo systemctl restart nfs-kernel-server
sudo ufw allow from 192.168.43.0/24 to any port nfs

