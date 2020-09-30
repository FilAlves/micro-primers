import os

os.system("sudo apt-get install cutadapt")
os.system("sudo apt-get install build-essential")
os.system("sudo apt-get install zlib1g")
os.system("sudo apt-get install zlib1g-dev")
os.system("sudo apt-get install default-jre")
os.system("sudo pip install -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython")
os.system("wget -q -O /tmp/libpng12.deb http://mirrors.kernel.org/ubuntu/pool/main/libp/libpng/libpng12-0_1.2.54-1ubuntu1_amd64.deb   && sudo dpkg -i /tmp/libpng12.deb   && sudo rm /tmp/libpng12.deb")


os.system("sed -i -e 's/CC_OPTS    = -g -Wall -D__USE_FIXED_PROTOTYPES__/CC_OPTS = -g -Wall -D__USE_FIXED_PROTOTYPES_ -fpermissive/' software/primer3/src/Makefile")

os.system("make -C software/primer3/src/")
os.system("make -C software/cdhit")
os.system("make -C software/FLASH-1.2.11")
