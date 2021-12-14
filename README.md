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

## Usage

To use micro-primers:

1. Activate conda environment `conda activate micro-primers`;
2. Start micro-primers (on the same terminal window) `python3 micro-primers`;

# The Pipeline

## Micro-Primers composition

Micro-Primers pipeline was written in Python version 3.6. It can be used with either:
- GUI interface (for single sample analysis).
- Terminal interface (for pipelines and servers).

With `python3 micro-primers.py -h` the user can see all arguments that can be used in terminal mode.

If no parameters are given, the GUI interface will be initialized.
If at least one parameters is given, the terminal interface will be initialized.

The folder software, provided together with the Python scripts, contains all the scripts and external software employed by micro-primers.py with all the external programs needed for its correct execution.

## Input Files

In order to run Micro-Primers, users only need to provide two FASTQ files corresponding to both ends of a pair-end sequencing. Samples should come from a pool of (untagged) individuals of the same species so the microsatellite selection can be optimized. SSR selection will be performed based on the number of alleles of each SSR loci, so the more heterogeneous is the sample, the better will be the final result. Reads must come from a microsatellite library built using a restriction enzyme and following an enrichment protocol. The idea behind the enrichment protocol after digestion is to have a random representation from the whole genome where the target SSR motifs will be the most represented strands in the final library. A fragment size selection is then performed on the enriched library to keep only fragments of an average length lower than the maximum sequencing length so both paired-ends reads overlap when merged later on. The final fragment size is important for microsatellite screening and must comprise the full SSR pattern (variable in length) and the two flanking regions with fair length for primer design.

![micro2](https://user-images.githubusercontent.com/38048444/73688620-56ae0180-46c4-11ea-8068-fe55a5e15f20.png)

# Execution Parameters

The basic parameters required by Micro-Primers are set in the different tabs of the program interface. 

## GUI interface

### Main Window

 - **Input R1 and R2 files** - Input pair-end fastq files

 - **Outuput File** - Ouput file containg the designed primers.

 - **Prefix** - Prefix for the results.

The “Settings” button contains three sections with different parameters to be considered for the pipeline execution: 

### Settings - Pre-Processing
    
- **CutAdapt (3' and 5')** - adapters used after the restriction enzyme action and the pattern remaining in the sequence after the digestion. 
    
- **Restriction enzyme pattern** - If the data was not produced by restriction enzyme this option can be disabled at this section as well. 

### Settings - Primers
    
- **Primers types to be excluded** - One or more SSR types can be excluded from the available options: c (compound), c* (compound with imperfection) and p1 to p6 (repeated motif of 1 to 6 nucleotides). 
    
- **Primer3 settings file** - A tuned Primer3 setting file can be selected in case the default one included in Micro-Primers is not convenient. 
    
- **Filter primers inside SSRs**

### Setings - Alleles

- **Minimal number of alleles in cluster** - Minimum number of alleles for a SSR locus to be selected. Based on the observed alleles (default value set to 5). 
    
- **Minimal distance between alleles** - Considering the difference between the alleles with higher and lower number of repeats, only loci that satisfy the minimum number of alleles indicated in this parameter are kept. This parameter is used only when the option “Special Search” is enabled (ON). 

- **Minimum flank region length** - Discard every sequence with at least one flanking region shorter that the minimum.

- **Minimum motif repetition** - Minimum number of repetitions in a SSR.

- **Special Search** - Toggle button to activate "Special Search".

## Terminal interface

    -h, --help               show this help message and exit
    -r1 , --fastqr1          Path to R1 input file.
    -r2 , --fastqr2          Path to R2 input file.
    -o , --output            Output file name.
    -exc , --exclude         SSR types to be excluded from search.
    -enz [], --resenzime []  Restriction enzime pattern. Default = No enzime pattern.
    -spc, --special          Activates special search. Default: False.
    -p3f, --p3filter         Filters primers designed inside SSR region. Default: False.
    -p3 , --primer3          Path to primer3 settings file.
    -c3 , --cutadapt3        Reverse adapter sequence (CutAdapt).
    -c5 , --cutadapt5        Foward adapter sequence (CutAdapt).
    -flank , --minflank      Minimum length accepted in both flanking regions. Default: 50.
    -cnt , --mincount        Minimum number of alleles for a SSR loci. Default: 5.
    -motif , --minmotif      Minimum number of SSR motif repetitions. Default: 5.
    -diff , --mindiff        Minimum difference between the allele with higher
                           number of repeats and the allele with a smaller
                           number. Only used if special search is activated. Default: 8.
    -p , --prefix            Loci name on output file. Default: SSR.


![imagem](https://user-images.githubusercontent.com/38048444/73688787-af7d9a00-46c4-11ea-8192-49f8cf4f0f98.png)

# Output

It has twelve columns, and each line  represents the primers designed by Primer3 for each SSR recovered from the multi- individual sample. From left to right, the first column, in red, is the unique name of each  cluster (ID) composed by a prefix (set by the user), the number of the loci and the primer pair number. Lines sharing the same loci number represent different primer pairs for the same SSR loci. The second column has the length (Size) of the sequence resultant from PCR amplification using the respective primer pairs. The third and fourth columns are the forward primer sequence and its melting temperature. The fifth and sixth columns refer to the equivalent information for the reverse primer. In the seventh column, the specific motif found is shown with the number of repeats present in the representative sequence. The column identified as ’Range’ shows the length span of the alleles detected for the same SSR. The nineth column contains the total number of alleles for the specific SSR loci. The tenth column indicates the potential number of alleles to be found in the population estimated from the difference between the longest and shortest alleles found. The eleventh column indicates the best combination of primer pairs for each loci (coded as “ | BEST | ”) as provided by Primer3 and the last column contain the representative sequence for the SSR loci from which the primers where designed.

![output](https://user-images.githubusercontent.com/38048444/146002543-344d79fb-28e2-459a-b10b-d2a8edc8da3a.png)

