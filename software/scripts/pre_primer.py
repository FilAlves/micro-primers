import re


def pseudofasta(rf1, rf2, of1):

    readfile1 = open(rf1, "r")
    readfile2 = open(rf2, "r")
    outfile1 = open(of1, "w")

    selected_seqs = []

    for line in readfile1:
        selected_seqs.append(line)

    for line in readfile2:
        if line[0] == ">" :
            if line[1:] in selected_seqs:
                nextline = readfile2.readline()
                outfile1.write("SEQUENCE_ID=" + line[1:] +
                               "SEQUENCE_TEMPLATE=" + nextline +
                               "=" + "\n")

    outfile1.close()


def final_primers(rf1, rf2, of1, prefix):

    readfile1 = open(rf1, "r")
    readfile2 = open(rf2, "r")
    outfile1 = open(of1, "w")

    out = []
    dic_attr = {}

    for line in readfile1:
        line = line.rstrip()
        selected_line = line.split("\t")
        dic_attr[selected_line[0]] = [selected_line[1], selected_line[2],
                                     selected_line[3], selected_line[4],
                                     selected_line[5], selected_line[6],
                                     selected_line[7]]

    final_matrix = transform(readfile2, outfile1, dic_attr)

    id_loci = 0
    id_pair = 1

    outfile1.write("ID\tSize\tFw Primer\tFw Tm\tRv Primer\tRv Tm\tMotif\tAmplicon Amplitude\tAlleles Found\tPotential Alleles\tFlag\tSequence\n")
    for line in sorted(final_matrix, key=lambda line: int(line[8]), reverse = True):

        # Checks if current Loci is new.
        if line[10][:8:] == "| BEST |":

            # Resets pair (First to be found for the new loci) and increments loci.
            id_pair = 1
            id_loci += 1

        # Adds loci and pair id.
        line[0] = prefix + "_Loci" + str(id_loci) + "_Pair" + str(id_pair)
        line = "\t".join(line)

        # Increments id_pair
        id_pair += 1

        outfile1.write(line)



    readfile1.close()
    readfile2.close()
    outfile1.close()


def transform(readfile, outfile, dic):
    out = []
    final_matrix = []
    for line in readfile:
        line = line.rstrip()

        # ID
        if re.match("^SEQUENCE_ID", line):
            id = line.split("=")[1]
            count = 0

        # DNA sequence
        elif re.match("^SEQUENCE_TEMPLATE", line):
            sequence = line.split("=")[1]

        # Left primer sequence
        elif re.match("^PRIMER_LEFT_\d_SEQUENCE", line):
            out.append(line.split("=")[1])

        # Right primer sequence
        elif re.match("^PRIMER_RIGHT_\d_SEQUENCE", line):
            out.append(line.split("=")[1])

        # Left primer Tm
        elif re.match("^PRIMER_LEFT_\d_TM", line):
            out.append(line.split("=")[1])

        # Right primer Tm
        elif re.match("^PRIMER_RIGHT_\d_TM=", line):
            out.append(line.split("=")[1])

        # Left primer start position and length
        elif re.match("^PRIMER_LEFT_\d=(\d*),(\d*)", line):
            next = line.split("=")[1]
            left_ini, left_len = next.split(",")

        # Right primer start position and length
        elif re.match("^PRIMER_RIGHT_\d=(\d*),(\d*)", line):
            next = line.split("=")[1]
            right_ini, right_len = next.split(",")

        # Amplicon size
        elif re.match("^PRIMER_PAIR_\d_PRODUCT_SIZE=\d", line):
            out.append(line.split("=")[1])

            #print(out)
            # Declaring Amplicon size
            ampl_size = out[4]
            # Declaring allele used for amplicon design
            ampl_allele = dic[id][0].split(")")[1]

            # Sequence ID
            out.append(dic[id][0])

            # Amplicon start position
            start = int(dic[id][1])

            # Amplicon end position
            end = int(dic[id][2])

            possible_alleles = (int(dic[id][5]) - int(dic[id][4])) + 1
            alleles_found = dic[id][6]

            # Allele motif for amplicon range calculation
            motif = out[5]

            # String construction of possible amplicon size range
            ampl_min = amplicon_calc(ampl_size, ampl_allele, dic[id][4], motif)
            ampl_max = amplicon_calc(ampl_size, ampl_allele, dic[id][5], motif)
            ampl_range = "[" + str(ampl_min) + "," + str(ampl_max) + "]"

            good_left = int(left_ini) + int(left_len)
            good_right = int(right_ini)

            # Output construction
            if (good_left < start) and (good_right > end):
                out = list(out[i] for i in [4, 0, 2, 1, 3, 5])
                out = [id] + out + [ampl_range] + [alleles_found] + [str(possible_alleles)]
                if count == 0:
                    out.append("| BEST |\t" + sequence + "\n")
                    count = 1
                else:
                    out.append("\t" + sequence + "\n")
                final_matrix.append(out)
            out = []
    return final_matrix


# Calculation of the size range of the amplicon
def amplicon_calc(ampl_size, ampl_allele, allele, motif):

    # Convert all arguments to int
    ampl_size, ampl_allele, allele = int(ampl_size), int(ampl_allele), int(allele)

    # Calculate motif lengths
    motif_len = len(motif.split(")")[0]) - 1

    # Add or subtract if alleles are bigger or smaller than base allele
    if allele > ampl_allele:
        ampl_result = ampl_size + (abs(ampl_allele - allele) * motif_len)
    else:
        ampl_result = ampl_size - (abs(ampl_allele - allele) * motif_len)
    return ampl_result
