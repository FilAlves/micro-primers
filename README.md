# Micro-Primers
Micro-Primers is a Python and PERL coded pipeline to identify and design PCR primers for amplification of SSR loci. The pipeline takes as input just a FASTQ file containing sequences from NGS (next generation sequencing) and returns a text file with information regarding the microsatellite markers, including number of alleles in the population, the melting temperature and the respective product of primer sets to easily guide the selection of optimal markers for the species. This pipeline correctly only supports UNIX based operating systems.

For any questions please send an email to filipealvesbio@gmail.com

## Requeriments:
- Python3;
- build-essencial;
- perl;
- cutadapt;
- java;
- zlib;

## Installation (linux)

1. Using the terminal, clone the repository using the command `git clone https://github.com/FilAlves/micro-primers`;
2. Install Conda (https://docs.conda.io/en/latest/miniconda.html);
3. Create conda environment with micro-primers requirements (located in the cloned repository) `conda env create -f micro-primers/conda_requirements.yml`;
4. Activate conda environment `conda activate micro-primers`;
5. Install other necessary software `python3 setup.py`.

## Usage

To use micro-primers:

1. Activate conda environment `conda activate micro-primers`;
2. Start micro-primers (on the same terminal window) `python3 micro-primers`;

# The Pipeline

## Micro-Primers composition

Micro-Primers pipeline was written in Python version 3.6 and consists basically in two different scripts: (i) install.py that includes all necessary pre-requisites for a proper installation of Micro-Primers, and (ii) micro-primers.py, the pipeline itself. Analysis settings are described in the config.txt file, where parameters can be modified by the user accordingly to his own particular needs. The folder software, provided together with the Python scripts, contains all the scripts and external software employed by micro-primers.py with all the external programs needed for a correct execution.

![micro2](https://user-images.githubusercontent.com/38048444/73688620-56ae0180-46c4-11ea-8068-fe55a5e15f20.png)

## Input Files

In order to run Micro-Primers, users only need to provide two FASTQ files corresponding to both ends of a pair-end sequencing. Samples should come from a pool of (untagged) individuals of the same species so the microsatellite selection can be optimized. SSR selection will be performed based on the number of alleles of each SSR loci, so the more heterogeneous is the sample, the better will be the final result. Reads must come from a microsatellite library built using a restriction enzyme and following an enrichment protocol. The idea behind the enrichment protocol after digestion is to have a random representation from the whole genome where the target SSR motifs will be the most represented strands in the final library. A fragment size selection is then performed on the enriched library to keep only fragments of an average length lower than the maximum sequencing length so both paired-ends reads overlap when merged later on. The final fragment size is important for microsatellite screening and must comprise the full SSR pattern (variable in length) and the two flanking regions with fair length for primer design.

## Execution Parameters

### Input Files
All the parameters that Micro-Primers needs to properly perform the analysis must be set at the config.txt file. In this text file there are four sections with different parameters to take into account for the pipeline execution. First of all, it can be found the "Input files" section where the user has to indicate the name of the pair-end files that will be used in the analysis. 


### Cutadapt
Then, at the "CUTADAPT" section, the sequence of adapters used after the restriction enzyme digestion is required.

### SSR
Next stage is called "SSR" and several parameters regarding the microsatellite selection are involved. 

- MIN_FLANK_LEN defines the minimum length accepted in both flanking regions where the primers will be designed on. 

- MIN_MOTIF_REP sets the minimum number of repeats that every SSR region must have to continue in the pipeline. 

- EXC_MOTIF_TYPE defines what SSR motifs are to be discarded. Options for this parameter are c;c*;p1;p2;p3;p4;p5;p6, being compound, compound with imperfection, or motif with different repeats from 1 to 6 nucleotides, respectively. It should be noted that bigger motifs are supported but any higher than 6 bases does not classifies as an microsatellite, but as a minisatellite. Motifs selected previously that must be discarded should be indicated separately withcomma. 

- MIN_ALLEL_CNT defines the minimum number of alleles for a SSR loci to be selected is indicated. 

- MIN_ALLEL_SPECIAL is used to enable or disable (1=enabled, 0=disabled) the option to select microsatellites with less number of alleles previously indicated as long as the difference between the allele with higher number of repeats and the allele with a smaller number of repeats satisfy the number indicated in MIN_ALLEL_SPECIAL_DIFF. 

- PRIMER3_SETTINGS indicates the path to the Primer3 settings file. In this settings file several parameters can be changed but a general one is provided with the standard parameters that Primer3 includes.

![imagem](https://user-images.githubusercontent.com/38048444/73688787-af7d9a00-46c4-11ea-8192-49f8cf4f0f98.png)

### Notes 
- No spaces or additional text character should be present after the character "=". 

- Every setting, besides R1 and R2 file names, have a default value defined in the configuration file.

# Output

The final output file is divided by tabs and contains eight columns. Each line represents the primers designed by Primer3 for each SSR found in the sample. (a) First column (red) contains the sequence identifier. For each loci representative various primers can be designed, giving the users various options for optimal amplification. (b) Next, the total size of the SSR is shown (Brown). The primers designed are shown next, starting with the left primer and respective Tm, followed by the right Primer and respective Tm. Both primers are shown with direction 5’ to 3’. Then, the specific motif/allele found is shown with the total number of alleles for the specific SSR loci (black). The flag "|BEST|" is shown if Primer3 defines the corresponding primer as the best one for loci amplification.

![output](https://user-images.githubusercontent.com/38048444/73688993-24e96a80-46c5-11ea-8808-98fe0d5afb44.png)

