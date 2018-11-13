def rule(row):
        return int(row[0])

def order(rf1, rf2, of1):

    readfile1 = open(rf1, "r")
    readfile2 = open(rf2, "r")
    outfile1 = open(of1, "w")

    # Ordena a lista por id, talvez transformar id em index fixo para melhor eficiência
    #data = csv.reader(readfile1,delimiter='\t')
    #sortedlist = sorted(data, key=rule)

    #Creating dictionary to save cluster # and cluster size
    dic_cluster = {}

    for line in readfile1:
        selected_line = line.split("\t")
        selected_line[2] = selected_line[2].rstrip()

        #Create dictionary using ID as key and cluster # and cluster size
        dic_cluster[selected_line[0]] =  [selected_line[1], selected_line[2]]

    for line in readfile2:

        # Split by tab and remove \n
        selected_line = line.rstrip()
        selected_line = selected_line.split("\t")

        #Selecting only id
        id, junk = selected_line[0].split("_")

        #Appending to misa file cluster # and size
        for item in dic_cluster[id]:
            selected_line.append(item)
        selected_line.append("\n")

        #Outfile writing
        outfile1.write("\t".join(selected_line))


def template(rf1, rf2, of1):

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

#template(".temp/selected_micros_seqs.txt", ".temp/ids_out.fasta", "teste1.txt")
#order(".temp/clusters_out.txt", ".temp/good_micros_table_out.misa", ".temp/cluster_info_out.txt")
