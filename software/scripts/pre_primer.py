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
                outfile1.write("SEQUENCE_ID=" + line[1:] + "SEQUENCE_TEMPLATE=" + nextline + "=" + "\n")

    outfile1.close()

def final_primers(rf1, rf2, of1):

    readfile1 = open(rf1, "r")
    readfile2 = open(rf2, "r")
    outfile1 = open(of1, "w")

    out = []
    dic_attr = {}

    for line in readfile1:
        line = line.rstrip()
        selected_line = line.split("\t")
        dic_attr[selected_line[0]] = [selected_line[1], selected_line[2], selected_line[3], selected_line[4], selected_line[5]]

    transform(readfile2, outfile1, dic_attr)

    readfile1.close()
    readfile2.close()
    outfile1.close()

def transform(readfile, outfile, dic):
    out = []
    for line in readfile:
        line = line.rstrip()
        if re.match("^SEQUENCE_ID", line):
            id = line.split("=")[1]
            count = 0
        elif re.match("^PRIMER_LEFT_\d_SEQUENCE", line):
            out.append(line.split("=")[1])
        elif re.match("^PRIMER_RIGHT_\d_SEQUENCE", line):
            out.append(line.split("=")[1])
        elif re.match("^PRIMER_LEFT_\d_TM", line):
            out.append(line.split("=")[1])
        elif re.match("^PRIMER_RIGHT_\d_TM=", line):
            out.append(line.split("=")[1])
        elif re.match("^PRIMER_LEFT_\d=(\d*),(\d*)", line):
            next = line.split("=")[1]
            left_ini, left_len = next.split(",")
        elif re.match("^PRIMER_RIGHT_\d=(\d*),(\d*)", line):
            next = line.split("=")[1]
            right_ini, right_len = next.split(",")
        elif re.match("^PRIMER_PAIR_\d_PRODUCT_SIZE=\d", line):
            out.append(line.split("=")[1])

            out.append(dic[id][0])
            out.append(dic[id][4])
            start = int(dic[id][1])
            end = int(dic[id][2])
            cluster = dic[id][3]

            good_left = int(left_ini) + int(left_len)
            good_right = int(right_ini)

            if (good_left < start) and (good_right > end):
                out = list(out[i] for i in [4,0,2,1,3,5,6])
                out = [str(id)] + out
                outfile.write("\t".join(out))
                if count == 0 :
                    outfile.write("\t| BEST |" )
                    count  = 1
                outfile.write("\n")
            out = []
