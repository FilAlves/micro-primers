import os
import sys

#Create empty file for importing python scripts
os.system("touch software/scripts/__init__.py")

from software.scripts import picker, config, text_manip, pre_primer

#Reading settings
settings = config.config("config.txt")

#Creation of hidden temp file
if os.path.isdir(".temp/") == False:
    os.system("mkdir .temp")

if os.path.isdir("logs/") == False:
    os.system("mkdir logs")

#Sequences Triming of Sequencer adapters
def trimmomatic(R1, R2):
    os.system("echo 'Trimmomatic working...'")
    os.system(
        "java -jar software/Trimmomatic-0.36/trimmomatic-0.36.jar PE -phred33 "
        "%s %s "
        ".temp/trim_out_trimmed_R1.fastq .temp/trim_out_unpaired_R1.fastq "
        ".temp/trim_out_trimmed_R2.fastq .temp/trim_out_unpaired_R2.fastq "
        "ILLUMINACLIP:./software/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 "
        "LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 2> logs/trim_log.txt"
        %(R1, R2)
        )

#Adapters removal (specifics from technology)
def cutadapt(a, g):
    os.system("echo 'Cutadapt working...'")
    os.system("cutadapt -a %s -g %s -o .temp/cut_out_nolink_R1.fastq .temp/trim_out_trimmed_R1.fastq > logs/cut_log_r1.txt" %(a, g))
    os.system("cutadapt -a %s -g %s -o .temp/cut_out_nolink_R2.fastq .temp/trim_out_trimmed_R2.fastq > logs/cut_log_r2.txt" %(a, g))

# Fusion of R1 and R2 files
def flash():
    os.system("echo 'Flash working...'")
    os.system("software/FLASH-1.2.11/flash .temp/cut_out_nolink_R1.fastq .temp/cut_out_nolink_R2.fastq -M 220 -o .temp/flash_out 2>&1 |"
             " tee logs/flash.log > logs/flash_log.txt")

# Selecion of fragments that start and ends with the pattern of the restriction enzyme
def grep():
    os.system("echo 'Selecting sequences with restriction enzime patterns...'")
    os.system("grep -B1 '^GATC\(\w*\)GATC$' .temp/flash_out.extendedFrags.fastq | sed 's/^@/>/' | perl -pe 's/--\n//g' > .temp/grep_out.fasta")

#Change id's and Length Calculation for later selection of valid microsatellites
def ids_and_len():
    os.system("echo 'Adding ids...'")
    os.system("echo 'Calculating sequences lengths...'")
    text_manip.change_ids_and_calc_len(".temp/grep_out.fasta", ".temp/ids_out.fasta", ".temp/length_calc_out.fasta")

#Search Microssatelites
def misa():
    os.system("echo 'Misa working...'")
    os.system("perl software/scripts/misa.pl .temp/ids_out.fasta 2> logs/misa_log.txt")

#Adds length to end of the sequences to misa output
def length_add():
    os.system("echo 'Adding length to misa output...'")
    text_manip.length_merger(".temp/misa_out.misa", ".temp/length_calc_out.fasta", ".temp/length_add_out.misa")

#Selection of microssatelites with enough space for primer
def good_micros(dist, rep, exclude):
    os.system("echo 'Selecting good microsatellites...'")
    picker.csv_picker(".temp/length_add_out.misa", ".temp/good_micros_out.fasta",
                ".temp/good_micros_table_out.misa",dist, rep, exclude)

#Extraction of the microsatellite sequence from allignement of fragments with flanking regions
def splitSSR():
    os.system("echo 'splitSSR working...'")
    text_manip.split(".temp/good_micros_out.fasta", ".temp/ids_out.fasta", ".temp/split_out.fasta")

#Removal of Redundacy
def cdhit():
    os.system("echo 'CD-HIT working...'")
    os.system("software/cdhit/cd-hit-est -o .temp/cdhit_out.txt -i .temp/split_out.fasta -c 0.90 -n 10 -T 10 > logs/cdhit_log.txt")

#Cluster assignement
def cluster():
    os.system("echo 'Calculating number of sequences for each cluster...'")
    text_manip.cluster(".temp/cdhit_out.txt.clstr", ".temp/clusters_out.txt")

#Adding cluster information to Microssatelites table
def cluster_info():
    os.system("echo 'Adding information to the table of microsatellites...'")
    text_manip.add_cluster_info(".temp/clusters_out.txt", ".temp/good_micros_table_out.misa", ".temp/cluster_info_out.txt")

def cluster_filter(MIN_SEL_SRR, MIN_SEL_SRR_SPECIAL, MIN_SEL_SSR_SPECIAL_DIF):
    picker.allels(".temp/cluster_info_out.txt", ".temp/cluster_filter_out.txt", MIN_SEL_SRR, MIN_SEL_SRR_SPECIAL, MIN_SEL_SSR_SPECIAL_DIF)

# Selecting one sequence per cluster
def selected_micros():
    os.system("echo 'Selecting one sequence per cluster...'")
    picker.selected_micros(".temp/cluster_filter_out.txt", ".temp/selected_micros_out_seqs.txt", ".temp/selected_micros_out_tabs.txt")

#Creating input file for Primer3
def create_pseudofasta():
    os.system("echo 'Creating Primer3 input file...'")
    pre_primer.pseudofasta(".temp/selected_micros_out_seqs.txt", ".temp/ids_out.fasta", ".temp/pseudo_out.fasta")

#Check if primer3 input is empty
def size_check(SPECIAL_CASE):
    if os.path.getsize(".temp/pseudo_out.fasta") < 1:
        print("Empty primer3 input file. \n")
        if SPECIAL_CASE == 0:
            sys.exit("No valid SSR's were selected. Try using the special search.")
        elif SPECIAL_CASE == 1:
            sys.exit("No valid SSR's were selected.")


#Primer design and creation
def primer3(p3_settings):
    os.system("echo 'Creating Primers...'")
    os.system("software/primer3/src/./primer3_core -default_version=2 -p3_settings_file=%s "
              ".temp/pseudo_out.fasta -output=.temp/micros_selected_long.primers" %(p3_settings) )

#Selection of primers following laboratory criteria
def select():
    os.system("echo 'Selecting best primers...'")
    pre_primer.final_primers(".temp/selected_micros_out_tabs.txt", ".temp/micros_selected_long.primers", "final_primers.txt")

#Removal of .temp directory
def junk():
    os.system("rm -r .temp/")

#Pipeline
trimmomatic(settings[0], settings[1])
cutadapt(settings[2], settings[3])
flash()
grep()
ids_and_len()
misa()
length_add()
good_micros(int(settings[4]), int(settings[5]), settings[6])
splitSSR()
cdhit()
cluster()
cluster_info()
cluster_filter(int(settings[7]), int(settings[8]), int(settings[9]))
selected_micros()
create_pseudofasta()
size_check(int(settings[8]))
primer3(settings[10])
select()
#junk()

os.system("echo 'Done!'")


#É preciso fazer make do CD-HIT, Primer3 e flash
