# Micro-Primers
Micro-Primers is a Python and PERL coded pipeline to identify and design PCR primers for amplification of SSR loci. The pipeline takes as input just a FASTQ file containing sequences from NGS and returns a text file with information regarding the microsatellite markers, including number of alleles in the population, the melting temperature and the respective product of primer sets to easily guide the selection of optimal markers for the species. This pipeline correctly only supports UNIX based operating systems.

For any questions please send an email to filipealvesbio@gmail.com

## Requeriments:
- Python3;
- build-essencial;
- perl;
- cutadapt;
- java;
- zlib;

## Installation (linux)

1. Using the terminal, clone the repository using the command 'git clone https://github.com/FilAlves/micro-primers'.
2. Install suing the command 'sudo python3 ~/micro-primers/install.py'
3. Configure config.txt 

# The Pipeline

## Micro-Primers composition

Micro-Primers pipeline was written in Python version 3.6 and consists basically in two different scripts: (i) install.py that includes all necessary pre-requisites for a proper installation of Micro-Primers, and (ii) micro-primers.py, the pipeline itself. Analysis settings are described in the config.txt file, where parameters can be modified by the user accordingly to his own particular needs. The folder software, provided together with the Python scripts, contains all the scripts and external software employed by micro-primers.py with all the external programs needed for a correct execution.

## Input Files

In order to run Micro-Primers, users only need to provide two FASTQ files corresponding to both ends of a pair-end sequencing. Samples should come from a pool of (untagged) individuals of the same species so the microsatellite selection can be optimized. SSR selection will be performed based on the number of alleles of each SSR loci, so the more heterogeneous is the sample, the better will be the final result. Reads must come from a microsatellite library built using a restriction enzyme and following an enrichment protocol such as the one described in [78]. The idea behind the enrichment protocol after digestion is to have a random representation from the whole genome where the target SSR motifs will be the most represented strands in the final library. A fragment size selection is then performed on the enriched library to keep only fragments of an average length lower than the maximum sequencing length so both paired-ends reads overlap when merged later on. The final fragment size is important for microsatellite screening and must comprise the full SSR pattern (variable in length) and the two flanking regions with fair length for primer design.

## Execution Parameters

All the parameters that Micro-Primers needs to properly perform the analysis must be set at the config.txt file. In this text file there are four sections with different parameters to take into account for the pipeline execution. First of all, it can be found the "Input files" section where the user has to indicate the name of the pair-end files that will be used in the analysis. Then, at the "CUTADAPT" section, the sequence of adapters used after the restriction enzyme digestion is required.

These adapters were necessary to transform the longer overhangs into blunt ends after the enzyme digestion. Next stage is called "SSR" and several parameters regarding the microsatellite selection are involved. The parameter MIN_FLANK_LEN indicates the minimum length accepted in both flanking regions where the primers will be designed on. PCR amplification primers usually have a length around 20-25 nucleotides and some particularities are required, like the presence of G or C at the 3’ end, certain percentage of GC for a proper melting temperature, both primers should have similar melting temperature for the hybridization to take place at the same time [85]. All these factors make critical the length of the flanking areas since a very narrow window can make impossible the primer design and subsequently the SSR to be discarded. Thus, every sequence with shorter flanking region in one or both ends will be discarded.

The MIN_MOTIF_REP sets the minimum number of repeats that every SSR region must have to continue in the pipeline. 

EXC_MOTIF_TYPE defines what SSR motifs are to be discarded. Options for this parameter are c;c*;p1;p2;p3;p4;p5;p6, being compound, compound with imperfection, or motif with different repeats from 1 to 6 nucleotides, respectively. It should be noted that bigger motifs are supported but any higher than 6 bases does not classifies as an microsatellite, but as a minisatellite. Motifs selected previously that must be discarded should be indicated separately withcomma. 

MIN_ALLEL_CNT defines the minimum number of alleles for a SSR loci to be selected is indicated. 

MIN_ALLEL_SPECIAL is used to enable or disable (1=enabled, 0=disabled) the option to select microsatellites with less number of alleles previously indicated as long as the difference between the allele with higher number of repeats and the allele with a smaller number of repeats satisfy the number indicated in MIN_ALLEL_SPECIAL_DIFF. 

Last section in the config.txt file is about PRIMER3. Here the only requirement is to indicate the path to the Primer3 settings file. In this settings file several parameters can be changed but a general one is provided with the standard parameters that Primer3 includes.

No spaces or additional text character should be present after the character "=". 

Every setting, besides R1 and R2 file names, have a default value defined in the configuration file.
