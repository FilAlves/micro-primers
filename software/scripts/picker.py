def selected_micros(rf1, of_sel_micros, of_id_micros):
    readfile1 = open(rf1, "r")
    outfile1 = open(of_sel_micros, "w")
    outfile2 = open(of_id_micros, "w")

    dic_cluster = {}

    for line in readfile1:

        #Split by tab
        selected_line = line.split("\t")

        #Creating dictionary for selection of one sequencing per cluster
        if not selected_line[9] in dic_cluster.keys():
            dic_cluster[selected_line[9]] = selected_line[0]

            #Creating outfile with sequenceID, ssr, start and end positions of the ssr
            selected_micros = list( selected_line[i] for i in [0, 3, 5, 6])
            outfile2.write("\t".join(selected_micros) + "\n")

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

        #Select line which do not contain c, c* and p1 type SSR
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

def allels(rf1, of1, MIN_SEL_SRR, MIN_SEL_SRR_SPECIAL):

    readfile1 = open(rf1, "r")
    outfile1 = open(of1, "w")

    #Clusters to be exluded for having few allels size diferences
    cluster_exclude = []

    #Dictionary for saving sequence id and allel for each cluster
    dic_allels = {}

    for line in readfile1:

        selected_line = line.split("\t")

        # Writing dictionary
        if selected_line[8] not in dic_allels.keys():
            dic_allels[selected_line[8]] = []
            templist = [selected_line[0], selected_line[3]]
            dic_allels[selected_line[8]].append(templist)
        else:
            dic_allels[selected_line[8]].append([selected_line[0], selected_line[3]])


    for cluster_num in dic_allels:

        #List of every different allel for a given cluster
        allels_list = []

        #Selecting allel size
        for values in dic_allels[cluster_num]:
            junk, allels_size = values[1].split(")")

            #adding unique allels to list
            if MIN_SEL_SRR_SPECIAL == 0:
                if allels_size not in allels_list:
                    allels_list.append(allels_size)
            else:
                allels_list.append(int(allels_size))

        #Selecting cluster for exclusion
        if MIN_SEL_SRR_SPECIAL == 0:
            if len(allels_list) < MIN_SEL_SRR:
                cluster_exclude.append(cluster_num)
        else:
            if max(allels_list) - min(allels_list) < 6:
                cluster_exclude.append(cluster_num)

    #Reseting file cursor
    readfile1.seek(0)

    #Selecting sequences form clusters not excluded
    for line in readfile1:
        selected_line = line.split("\t")
        if selected_line[8] not in cluster_exclude:
            outfile1.write("\t".join(selected_line))
