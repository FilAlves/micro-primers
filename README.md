# Micro-Primers
Micro-Primers is a Python and PERL coded pipeline to identify and design PCR primers for amplification of SSR loci. The pipeline takes as input just a fastq file containing sequences from NGS (next generation sequencing) technologies and returns a text file with the primers and their respective melting temperature to easily perform an amplification of the same loci in other individuals of the same species.

## More info
A report file (Micro-primers.pdf) is avaible for more information on the construction and work flow of Micro-Primers. The report uses the layout of "Bioinformatics" magazine but was NOT published in it. 

For any questions please send an email to filipealvesbio@gmail.com

## Requeriments:
Python3;
build-essencial;
perl;
cutadapt;
java;
zlib;
A bit of pacience and happiness;



## Installation (linux)

1. Using the terminal, use "git clone https://github.com/FilAlves/micro-primers"
2. Download Primer3 from http://primer3.sourceforge.net/releases.php
3. Move primer3.tar.gz file to micro-primers/software
4. Unzip using manually or using the comand "tar -xvzf (file_name)"
5. Rename unziped primer3 file to "primer3"
6. On the console type: "sudo python3 ~/micro-primers/install.py
9. Enjoy life!
