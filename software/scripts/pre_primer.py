import re

def pseudofasta(rf1, rf2, of1):

    readfile1 = open(rf1, "r")
    readfile2 = open(rf2, "r")
    outfile1 = open(of1, "w")

    selected_seqs = []

    for line in readfile1:
        #line = line.rstrip()
        selected_seqs.append(line)

    #print(selected_seqs)

    for line in readfile2:
        if line[0] == ">" :
            if line[1:] in selected_seqs:
                nextline = readfile2.readline()
                outfile1.write("SEQUENCE_ID=" + line[1:] + "SEQUENCE_TEMPLATE=" + nextline + "=" + "\n")

def final_primers(rf1, rf2, of1):

    readfile1 = open(rf1, "r")
    readfile2 = open(rf2, "r")
    outfile1 = open(of1, "w")

    dic_primers = {}
    dic_selected = {}

    for line in readfile1:
        line = line.rstrip()
        selected_line = line.split("\t")
        dic_selected[selected_line[0]] = [selected_line[1], selected_line[2], selected_line[3]]

    for line in readfile2:
        line = line.rstrip()
        if re.match("^SEQUENCE_ID", line):
            junk, id = line.split("=")
            count = 0
        elif re.match("^PRIMER_LEFT_\d_SEQUENCE", line):
            junk, left = line.split("=")
        elif re.match("^PRIMER_RIGHT_\d_SEQUENCE", line):
            junk, right = line.split("=")
        elif re.match("^PRIMER_LEFT_\d_TM", line):
            junk, left_tm = line.split("=")
        elif re.match("^PRIMER_RIGHT_\d_TM=", line):
            junk, right_tm = line.split("=")
        elif re.match("^PRIMER_LEFT_\d=(\d*),(\d*)", line):
            junk, next = line.split("=")
            left_ini, left_len = next.split(",")
        elif re.match("^PRIMER_RIGHT_\d=(\d*),(\d*)", line):
            junk, next = line.split("=")
            right_ini, right_len = next.split(",")
        elif re.match("^PRIMER_PAIR_\d_PRODUCT_SIZE=\d", line):
            junk, product = line.split("=")

            motif = dic_selected[id][0]
            start = int(dic_selected[id][1])
            end = int(dic_selected[id][2])

            good_left = int(left_ini) + int(left_len)
            good_right = int(right_ini) - int(right_len)

            if (good_left < start) and (good_right > end):
                if count == 0:
                    outfile1.write(id + "\t" + product + "\t" + left + "\t" + left_tm + "\t" + right + "\t" + right_tm + "\t" + motif + "\t" + "| BEST |" + "\n")
                    count = 1
                else:
                    outfile1.write(id + "\t" + product + "\t" + left + "\t" + left_tm + "\t" + right + "\t" + right_tm + "\t" + motif + "\n")
