def config(rd):
    readfile = open(rd, "r")

    #Saves settings parameters as list
    settings = []

    for line in readfile:
        #Split line by "="
        selected_line = line.split("=")

        #Selects only the values after "="
        if len(selected_line) > 1:
            selected_line[1] = selected_line[1].rstrip()
            settings.append(selected_line[1])

    #Converts ssr_type from string to list
    ssr_type = settings[6].split(",")
    settings[6] = ssr_type

    return settings
