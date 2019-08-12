#!/bin/bash

cd /run/media/$USER/rootfs

pi=home/pi

echo "Copying public key to ~/.ssh/authorized_keys..."
mkdir -p $pi/.ssh

cat ~/.ssh/id_rsa.pub > $pi/.ssh/authorized_keys

echo ":: Setting term=xterm (#JustKittyTermThings)..."
sed -i '10aexport TERM=xterm\n' $pi/.bashrc

echo ":: Copying wpa_supplicant.conf..."
sudo cp ~/code/attendance/wpa_supplicant.conf etc/wpa_supplicant

echo ":: Enabling ssh"
touch ../boot/ssh

# echo ":: Installing libraries..."
# run "sudo apt install -qy python3-requests python3-pip python3-rpi.gpio git neovim"

# echo "Installing python libraries..."
# run "sudo pip3 install pi-rc522"

# echo ":: Enabling SPI interface..."
# run "sudo raspi-config"

echo ":: Cloning attendance repo..."
git clone https://github.com/lyneca/attendance $pi/attendance

echo ":: Installing systemd service..."
sudo cp $pi/attendance/attendance.service etc/systemd/system

echo ":: Transferring Firebase secret and usyd card key..."
cp ~/code/attendance/secret ~/code/attendance/usyd_key $pi

echo -n ":: Enter a device name: "
read name

echo ":: Setting device name as $name..."

echo "   - /etc/hostname"
sudo bash -c "echo attbot-$name > etc/hostname"

echo "   - /etc/hosts"
sudo bash -c "cat << EOL > etc/hosts
127.0.0.1       localhost
::1             localhost ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters
 
127.0.1.1       attbot-$name
EOL"

echo -n ":: Enter a device ID: "
read id

echo ":: Setting device as ID $id..."
echo $id > $pi/id

echo "Done."

