#Remove build before building the project
sudo rm -r build

#Build the project
pip3 install --break-system-packages  .

#Remove the project
pip3 uninstall smo --bresk-system-packages
