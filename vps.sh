JMTHON="\nJMTHON USERBOT DEPLOY ON VPS"
JMTHON+="\n "
JMTHON+="\n "
JMTHON+="\n★ Channel: @JMTHON ★"
JMTHON+="\n★ Support: @jmthon_support ★"
JMTHON+="\n "
ROZ="\n "
echo -e $JMTHON
echo -e $ROZ
echo "WAIT ..."
echo -e $ROZ
sudo apt update && upgrade -y
sudo apt install git -y
clear
echo -e $JMTHON
echo -e $ROZ
echo "installing python3"
echo -e $ROZ
sudo apt install python3
sudo apt install python3-pip
sudo apt install postgresql
sudo apt install neofetch
sudo apt install ffmpeg
sudo apt install curl
sudo apt install megatools
sudo apt install unzip
sudo apt install wget
sudo apt install liblapack-dev
sudo apt install aria2
sudo apt install zip
sudo apt install nano
sudo apt install sudo
sudo apt install python3-wand
sudo apt install python3-lxml
sudo apt install postgresql-client
pip3 install av -q --no-binary av
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
echo -e $JMTHON
echo -e $ROZ
echo "⚙️ Github Installer"
echo -e $ROZ
echo -e $JMTHON
echo -e $ROZ
echo "Cloning jmthon Userbot"
echo -e $ROZ
git clone -b bro https://github.com/thejmthon/sbb_b0
echo -e $JMTHON
echo -e $ROZ
echo "runing jmthon now"
echo -e $ROZ
cd sbb_b0
pip3 install -r requirements.txt
python3 razan/session/jmthon.py
