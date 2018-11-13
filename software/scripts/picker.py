def selected_micros(rf, of_sel_micros, of_id_micros):
    readfile = open(rf, "r")
    outfile1 = open(of_sel_micros, "w")
    outfile2 = open(of_id_micros, "w")

    dic_cluster = {}

    for line in readfile:

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
                good_micros = list( selected_line[i] for i in [0, 5, 6, 7])
                outfile.write("\t".join(good_micros))
                outfile2.write("\t".join(selected_line))

    #Adding "\n" to the end of the file. It alsos messes with splitSSR script
    outfile.write("\n")
