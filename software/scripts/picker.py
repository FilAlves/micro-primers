def dna_reverse(seq):
    #Complementary DNA dictionary
    dic_comp={"A":"T", "T":"A", "G":"C", "C":"G"}

    #Returning complementary sequence (NOT REVERSED)
    return ''.join(dic_comp[base] for base in seq)


def selected_micros(rf1, of_sel_micros, of_id_micros):
    readfile1 = open(rf1, "r")
    outfile1 = open(of_sel_micros, "w")
    outfile2 = open(of_id_micros, "w")

    dic_cluster = {}

    for line in readfile1:

        #Split by tab
        selected_line = line.split("\t")

        #Creating dictionary for selection of one sequencing per cluster
        if not selected_line[8] in dic_cluster.keys():
            dic_cluster[selected_line[8]] = selected_line[0]

            #Creating outfile with sequenceID, ssr, start and end positions of the ssr
            selected_micros = list( selected_line[i] for i in [0, 3, 5, 6, 8, 10])
            outfile2.write("\t".join(selected_micros))

    #creating tab_selected
    for keys,values in dic_cluster.items():
        outfile1.write(values + "\n")

def csv_picker(rf, of_micros_good, of_micros_tab, dist, rep, exclude):
    readfile = open(rf, "r")
    outfile = open(of_micros_good, "w")
    outfile2 = open(of_micros_tab, "w")


    #Minimal number of bases after and before SSR
    min_ext_dist = dist

    #Mnimal repetitions of SSR
    min_rep = rep

    #Types of ssr to exclude from further search
    exclude_ssr = exclude

    id = 1

    for line in readfile:
        #Split by tab
        selected_line = line.split("\t")

        #Select line which do not contain the correct SSR motif type.
        if not selected_line[2] in exclude_ssr:

            #Remove second "_" from ID. It messes with splitSSR script.
            remove_under = list(selected_line[0])
            for i in range (10, (len(remove_under))-1):
                if remove_under[i] == "_":
                    remove_under[i] = " "
            selected_line[0] = "".join(remove_under)

            # Selecting only sequences that have at least 50 bases before and after the SSR

            if int(selected_line[7]) - int(selected_line[6]) >= min_ext_dist and int(selected_line[5]) >= min_ext_dist:
                good_micros = list(selected_line[i] for i in [0, 5, 6, 7])
                good_micros = [str(id)] + good_micros
                outfile.write("\t".join(good_micros))
                outfile2.write("\t".join(selected_line))
                id += 1

    #Adding "\n" to the end of the file. It alsos messes with splitSSR script
    outfile.write("\n")

def allel(rf1, of1, MIN_SEL_SRR, MIN_SEL_SRR_SPECIAL, MIN_SEL_SSR_SPECIAL_DIF):

    readfile1 = open(rf1, "r")
    outfile1 = open(of1, "w")

    #Clusters to be exluded for having few allel size diferences
    cluster_exclude = []

    #Dictionary for saving sequence id and allel for each cluster
    dic_allel = {}
    dic_fuck = {}
    dic_shit = {}

    for line in readfile1:

        selected_line = line.split("\t")
        short_id = selected_line[0][0:10]

        # Writing dictionary
        if selected_line[8] not in dic_allel.keys():
            dic_allel[selected_line[8]] = []
            templist = [short_id, selected_line[3]]
            dic_allel[selected_line[8]].append(templist)
        else:
            dic_allel[selected_line[8]].append([short_id, selected_line[3]])


    for cluster_num in dic_allel:

        #List of every different allel for a given cluster
        dic_allel_cluster = {}

        #Selecting allel size
        for values in dic_allel[cluster_num]:
            id = values[0]
            allel_type, allel_size = values[1].split(")")
            allel_type = allel_type.replace("(","")

            #adding unique allel to list

            if allel_size in dic_allel_cluster.keys():
                dic_allel_cluster[allel_size][0] += 1
                dic_allel_cluster[allel_size][1].append(id)

            else:
                dic_allel_cluster[allel_size] = [[],[]]
                dic_allel_cluster[allel_size][0] = 1
                dic_allel_cluster[allel_size][1].append(id)

            dic_shit[cluster_num] = len(dic_allel_cluster.keys())
            if MIN_SEL_SRR_SPECIAL == 1:
                dic_fuck[cluster_num] = list(map(int,dic_allel_cluster.keys()))


    if MIN_SEL_SRR_SPECIAL == 0:
        for cluster in dic_shit.keys():
            #print(dic_shit.keys())
            if dic_shit[cluster] < MIN_SEL_SRR:
                cluster_exclude.append(cluster)
    else:
        for cluster in dic_fuck:
            if max(dic_fuck[cluster]) - min(dic_fuck[cluster]) < MIN_SEL_SSR_SPECIAL_DIF:
                cluster_exclude.append(cluster)

    #Reseting file cursor
    readfile1.seek(0)

    #Selecting sequences form clusters not excluded
    for line in readfile1:
        selected_line = line.split("\t")
        selected_line[9] = selected_line[9].rstrip()
        if selected_line[8] not in cluster_exclude:
            selected_line.append(str(dic_shit[selected_line[8]]) + "\n")
            outfile1.write("\t".join(selected_line))
