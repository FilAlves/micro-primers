
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

def final_primers(rf1, of1):

    readfile1 = open(rf1, "r")
    outfile1 = open(of1, "w")

    for line in readfile1:
        if "SEQUENCE_ID" in line:
            aa, id = line.split("=")
            print(id)


#final_primers(".temp/micros_selected_long.primers", ".temp/selected_micros_tabs.txt")
