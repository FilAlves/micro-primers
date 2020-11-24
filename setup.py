import os

os.system("sudo apt-get -y install cutadapt build-essential zlib1g zlib1g-dev default-jre")

os.system("sed -i -e 's/CC_OPTS    = -g -Wall -D__USE_FIXED_PROTOTYPES__/CC_OPTS = -g -Wall -D__USE_FIXED_PROTOTYPES_ -fpermissive/' software/primer3/src/Makefile")

os.system("make -C software/primer3/src/")
os.system("make -C software/cdhit")
os.system("make -C software/FLASH-1.2.11")
