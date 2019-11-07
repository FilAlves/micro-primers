import re

def change_ids_and_calc_len(rf1, of1, of2):

    readfile1 = open(rf1, "r")
    outfile1 = open(of1, "w")
    outfile2 = open(of2, "w")

    #ID counter
    counter = 1

    #ID saver
    len_line = ""

    # Cycle trough all lines
    for line in readfile1:

        #Selecting only lines with sequence ID
        if line[0] == ">":

            #Adding ID
            ids_line = line[0] + str(counter) + "_" + line[1:]

            #Saving ID string excluding ">"
            len_line = ids_line[1:]

            counter += 1
            outfile1.write(ids_line)

        #Selecting DNA sequence
        else:
            outfile1.write(line)

            #Calculate sequence size
            size = len(line) - 1

            #Constructing final string
            len_line = len_line.strip("\n")
            len_line = len_line + "\t" + str(size)
            outfile2.write(len_line + "\n")

    outfile1.close()
    outfile2.close()

def split(rf1, rf2, of1):

    readfile1 = open(rf1, "r")
    readfile2 = open(rf2, "r")
    outfile1 = open(of1, "w")

    #Criating Dictionary containing Number ID, Sequence ID, start and end of SSR
    dic_micros = {}

    for line in readfile1:
        selected_line = line.split("\t")
        if len(selected_line) > 1:
            dic_micros[selected_line[0]] = [selected_line[1][0:10], selected_line[2], selected_line[3]]

    # Search and cut of SSR in selected Sequences
    ssr_cut(readfile2, outfile1, dic_micros)

    outfile1.close()

def ssr_cut(readfile2, outfile1, dic):

    #Save last sequnce ID
    last_seq = ""
    #Save last DNA Sequence
    dna_line = ""

    for line in readfile2:
        selected_line = line.split("\t")

        for key in dic:

            if selected_line[0][1:11] in str(dic[key][0]):

                #Selecting Sequence ID
                if selected_line[0][0] == ">":

                    #If there is multiple SSR's the DNA Seq is saved
                    if last_seq == selected_line[0][1:11]:
                        nextline = dna_line
                        last_seq = ""

                    else:
                        #Selection of the next line, containing the DNA sequence
                        nextline = readfile2.readline()

                        dna_line = nextline
                    #Slicing away SSR
                    first_cut = int(dic.get(key)[1]) - 1
                    second_cut = int(dic.get(key)[2])
                    nextline = nextline[0 : first_cut] + nextline[second_cut: ]

                    #Output writing
                    outfile1.write(selected_line[0] + nextline)

                #Saving last sequence ID:
                if selected_line[0][0] == ">":
                    last_seq = selected_line[0][1:11]


def cluster(rf1, of1):
    readfile1 = open(rf1, "r")
    outfile1 = open(of1, "w")

    current_cluster = ""

    #Creating dictionary to save each sequence of each cluster
    dic_cluster = {}

    for line in readfile1:

        #Selecting cluster ID
        if ">" in line[0]:
            selected_line = line.split()
            current_cluster = selected_line[1]

            #Creating cluster entry on the dictionary
            dic_cluster[current_cluster] = []

        else:
            #Replacing "_" for ">"" for easy selection of sequence ID
            line = line.replace("_", ">")
            selected_line = line.split(">")

            #Adding sequence ID to corresponding cluster on the dictionary
            dic_cluster[current_cluster].append(selected_line[1])


    for key, value in dic_cluster.items():
        for x in value:
            #Defining cluster size
            size_cluster = len(dic_cluster[key])
            outfile1.write(str(x) + "\t" + str(key) + "\t" + str(size_cluster) + "\n")

    outfile1.close()

def add_cluster_info(rf1, rf2, of1):

    readfile1 = open(rf1, "r")
    readfile2 = open(rf2, "r")
    outfile1 = open(of1, "w")

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

        #Outfile writing
        outfile1.write("\t".join(selected_line) + "\n")

    outfile1.close()

def length_merger(rf1, rf2, of1):

    readfile_csv = open(rf1, "r")
    readfile_length = open(rf2, "r")
    outfile1 = open(of1,"w")

    #Creating dicitonary with SeqID and ssr length
    dic_length = {}

    # Dictionary writing
    for line in readfile_length:

        #Spliting file by tabs
        selected_line = line.split("\t")

        #Saving only 10 first caracters of ID.
        dic_length[selected_line[0][0:10]] = selected_line[1]

    for line in readfile_csv:
        selected_line = line.split("\t")

        #Removing \n from end tab
        selected_line[6] = selected_line[6].rstrip()

        #Creating new tab with ssr length
        if selected_line[0][0:10] in dic_length.keys():
            selected_line.append(dic_length[selected_line[0][0:10]])
            outfile1.write("\t".join(selected_line))

    outfile1.close()

def python_grep(rf1, of1):
    readfile1 = open(rf1, "r")
    outfile1 = open(of1, "w")

    for line in readfile1:
        pattern = r'^GATC\w*GATC$'
        seq = re.match(pattern, line)
        if seq:
            print(re.sub("^@",">",prev_line) + seq.group(0), file=outfile1)
        prev_line = line
