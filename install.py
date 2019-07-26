import os

os.system("sudo apt-get install cutadapt")
os.system("sudo apt-get install build-essential")
os.system("sudo apt-get install zlib1g")
os.system("sudo apt-get install zlib1g-dev")
os.system("sudo apt-get install default-jre")

os.system("sed -i -e 's/CC_OPTS    = -g -Wall -D__USE_FIXED_PROTOTYPES__/CC_OPTS = -g -Wall -D__USE_FIXED_PROTOTYPES_ -fpermissive/' software/primer3/src/Makefile")

os.system("make -C software/primer3/src/")
os.system("make -C software/cdhit")
os.system("make -C software/FLASH-1.2.11")
