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

    outfile1.close()
    outfile2.close()

def csv_picker(rf,
               of_micros_good,
               of_micros_tab,
               min_ext_dist,
               min_rep,
               exclude_ssr):

    readfile = open(rf, "r")
    outfile1 = open(of_micros_good, "w")
    outfile2 = open(of_micros_tab, "w")

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
                outfile1.write("\t".join(good_micros))
                outfile2.write("\t".join(selected_line))
                id += 1

    #Adding "\n" to the end of the file. It alsos messes with splitSSR script
    outfile1.write("\n")
    outfile1.close()
    outfile2.close()

def allele(rf1,
           of1,
           MIN_ALLELE_CNT,
           MIN_ALLELE_SPECIAL,
           MIN_ALLELE_SPECIAL_DIF):

    readfile1 = open(rf1, "r")
    outfile1 = open(of1, "w")

    #Clusters to be exluded for having few allele size diferences
    cluster_exclude = []

    #Dictionary for saving sequence id and allele for each cluster
    dic_pool = {}
    dic_allele = {}

    dic_writer(readfile1, dic_pool)
    allele_finder(dic_pool, dic_allele, MIN_ALLELE_SPECIAL)

    if MIN_ALLELE_SPECIAL == 0:
        for cluster in dic_allele.keys():
            if dic_allele[cluster] < MIN_ALLELE_CNT:
                cluster_exclude.append(cluster)
    else:
        for cluster in dic_allele:
            if max(dic_allele[cluster]) - min(dic_allele[cluster]) < MIN_ALLEL_SPECIAL_DIF:
                cluster_exclude.append(cluster)

    #Reseting file cursor
    readfile1.seek(0)

    #Selecting sequences form clusters not excluded
    for line in readfile1:
        selected_line = line.split("\t")
        selected_line[9] = selected_line[9].rstrip()
        if selected_line[8] not in cluster_exclude:
            selected_line.append(str(dic_allele[selected_line[8]]) + "\n")
            outfile1.write("\t".join(selected_line))

    outfile1.close()

def allele_finder(dic_pool, dic_allele, MIN_ALLELE_SPECIAL):
    for cluster_num in dic_pool:

        #List of every different allel for a given cluster
        dic_pool_cluster = {}

        #Selecting allel size
        for values in dic_pool[cluster_num]:
            id = values[0]
            allele_type, allele_size = values[1].split(")")
            allele_type = allele_type.replace("(","")

            #adding unique allel to list

            if allele_size in dic_pool_cluster.keys():
                dic_pool_cluster[allele_size][0] += 1
            else:
                dic_pool_cluster[allele_size] = [[],[]]
                dic_pool_cluster[allele_size][0] = 1
            dic_pool_cluster[allele_size][1].append(id)


            if MIN_ALLELE_SPECIAL == 1:
                dic_allele[cluster_num] = list(map(int,dic_pool_cluster.keys()))
            dic_allele[cluster_num] = len(dic_pool_cluster.keys())

def dic_writer(readfile1, dic):
    for line in readfile1:

        selected_line = line.split("\t")
        short_id = selected_line[0][0:10]

        # Writing dictionary
        if selected_line[8] not in dic.keys():
            dic[selected_line[8]] = []
            templist = [short_id, selected_line[3]]
            dic[selected_line[8]].append(templist)
        else:
            dic[selected_line[8]].append([short_id, selected_line[3]])
