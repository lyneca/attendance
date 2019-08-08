#!/bin/bash

pi=pi@$1

function run() {
    TERM=xterm ssh $pi $*
}

echo "Copying public key to ~/.ssh/authorized_keys..."
cat ~/.ssh/id_rsa.pub | run "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys" 

echo ":: Setting term=xterm (#JustKittyTermThings)..."
run "sed -i '10aexport TERM=xterm\n' .bashrc"

echo ":: Installing libraries..."
run "sudo apt install -qy python3-requests python3-pip python3-rpi.gpio git neovim"

echo ":: Enabling SPI interface..."
run "sudo raspi-config"

echo ":: Cloning attendance repo..."
run "git clone https://github.com/lyneca/attendance"

echo ":: Installing systemd service..."
run "sudo cp attendance/attendance.service /etc/systemd/system"

echo ":: Enabling service..."
run "sudo systemctl enable attendance.service"

echo ":: Transferring Firebase secret and usyd card key..."
scp secret usyd_key $pi:~

echo -n ":: Enter a device name: "
read name

echo ":: Setting device name as $name..."

echo "   - hostname"
run "sudo hostname $name"

echo "   - /etc/hostname"
run "sudo echo $name > /etc/hostname"

echo "   - /etc/hosts"
scp hosts $pi:~
run "sed -i s/{NAME}/$name/g hosts"
run "sudo mv hosts /etc/hosts"

echo -n ":: Enter a device ID: "
read id

echo ":: Setting device as ID $id..."
run "echo $id > ~/id"

echo ":: Setting device password..."
pass -c bot
run "passwd"

echo "Rebooting..."
run "sudo reboot"

echo "Done."

