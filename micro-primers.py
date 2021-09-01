from software.scripts import picker, text_manip, pre_primer
import sys, wx, os, time, threading, argparse, subprocess


def micro_primers_system_call(cmd, erro):
    rvalue = os.system(cmd)  # returns the exit code
    if rvalue != 0:
        sys.exit(erro)


# Create empty file for importing python scripts
micro_primers_system_call("touch software/scripts/__init__.py", "Error: could not create init.py.")

global cut3, cut5, grep, exclude, primer3_txt, minFlank, minMotif, minCnt, minDiff, special, r1, out, primer3Filter

class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer(sizer)
        self.Layout()


class TabPreProcessing(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        global cut3, cut5, grep

        gridSizer = wx.GridBagSizer(hgap=2, vgap=5)
        sizerCut_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizerCut_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizerGrep = wx.BoxSizer(wx.HORIZONTAL)

        cutLabel_3 = wx.StaticText(self, wx.ID_ANY, "CutAdapt 3' adapter sequence:")
        self.cutText_3 = wx.TextCtrl(self, wx.ID_ANY, value=cut3, size=(220, 30))

        cutLabel_5 = wx.StaticText(self, wx.ID_ANY, "CutAdapt 5' adapter sequence:")
        self.cutText_5 = wx.TextCtrl(self, wx.ID_ANY, value=cut5, size=(220, 30))

        grepLabel = wx.StaticText(self, wx.ID_ANY, "Restriction enzyme pattern:")
        self.grepText = wx.TextCtrl(self, wx.ID_ANY, value=grep, size=(220, 30))

        self.grepToggle = wx.ToggleButton(self, wx.ID_ANY, label="ON")
        self.grepToggle.Bind(wx.EVT_TOGGLEBUTTON, self.onToggle1)

        sizerCut_3.Add(cutLabel_3, wx.ALIGN_CENTER)
        sizerCut_3.Add(self.cutText_3, wx.ALIGN_CENTER)

        sizerCut_5.Add(cutLabel_5, wx.ALIGN_CENTER)
        sizerCut_5.Add(self.cutText_5, wx.ALIGN_CENTER)

        sizerGrep.Add(grepLabel, wx.ALIGN_CENTER)
        sizerGrep.Add(self.grepText, wx.ALIGN_CENTER)
        sizerGrep.Add(self.grepToggle)

        gridSizer.Add(sizerCut_3, pos=(0, 0))
        gridSizer.Add(sizerCut_5, pos=(1, 0))
        gridSizer.Add(sizerGrep, pos=(2, 0))

        self.SetSizer(gridSizer)
        self.Layout()

    def onToggle1(self, event):
        if self.grepToggle.GetValue():
            self.grepToggle.SetLabel("OFF")
            self.grepText.SetValue("")
        else:
            self.grepToggle.SetLabel("ON")
            self.grepText.SetValue(grep)


class TabPrimer(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        global exclude, primer3_txt, minFlank, minMotif

        gridSizer = wx.GridBagSizer(hgap=3, vgap=5)
        sizerExclude = wx.BoxSizer(wx.HORIZONTAL)
        sizerPrimer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizerPrimer3Filter = wx.BoxSizer(wx.HORIZONTAL)

        self.excludeLabel = wx.StaticText(self, wx.ID_ANY, "Primers types to be excluded: ")
        self.excludeText = wx.TextCtrl(self, wx.ID_ANY, value=exclude, size=(220, 30))

        primer3Label = wx.StaticText(self, wx.ID_ANY, "Primer3 setting file:")
        self.primer3Text = wx.TextCtrl(self, wx.ID_ANY, value=primer3_txt, size=(220, 30))
        primer3Button = wx.Button(self, label="Select")
        self.Bind(wx.EVT_BUTTON,
                  lambda event, box=self.primer3Text: self.get_path(event, box),
                  primer3Button)

        filterLabel = wx.StaticText(self, wx.ID_ANY, "Filter primers inside SSR: ")
        self.filterToggle = wx.ToggleButton(self, wx.ID_ANY, label="OFF")
        self.filterToggle.Bind(wx.EVT_TOGGLEBUTTON, self.onToggle)

        sizerExclude.Add(self.excludeLabel, wx.ALIGN_CENTER)
        # sizerExclude.Add(self.excludeText)

        sizerPrimer3.Add(self.primer3Text, wx.ALL | wx.ALIGN_CENTER)
        sizerPrimer3.Add(primer3Button)

        gridSizer.Add(sizerExclude, pos=(0, 0))
        gridSizer.Add(self.excludeText, pos=(0, 1))
        gridSizer.Add(primer3Label, pos=(1, 0))
        gridSizer.Add(sizerPrimer3, pos=(1, 1))
        gridSizer.Add(filterLabel, pos=(2, 0))
        gridSizer.Add(self.filterToggle, pos=(2, 1))

        self.SetSizer(gridSizer)
        self.Layout()

    def onToggle(self, event):
        if self.filterToggle.GetValue():
            self.filterToggle.SetLabel("ON")
        else:
            self.filterToggle.SetLabel("OFF")

    def get_path(self, event, box):
        test_dir = wx.FileDialog(self, "Choose a directory:")
        if test_dir.ShowModal() == wx.ID_OK:
            path = test_dir.GetPath()
            box.write(path)
        test_dir.Destroy()


class TabAlleles(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        gridSizer = wx.GridBagSizer(hgap=5, vgap=5)

        cntLabel = wx.StaticText(self, wx.ID_ANY, "Minimum number of alleles in cluster: ")
        self.cntText = wx.TextCtrl(self, wx.ID_ANY, value=minCnt, size=(220, 30))

        flankLabel = wx.StaticText(self, wx.ID_ANY, "Minimum flank region length: ")
        self.flankText = wx.TextCtrl(self, wx.ID_ANY, value=minFlank, size=(220, 30))

        motifLabel = wx.StaticText(self, wx.ID_ANY, "Minimum motif repetition: ")
        self.motifText = wx.TextCtrl(self, wx.ID_ANY, value=minMotif, size=(220, 30))

        specialLabel = wx.StaticText(self, wx.ID_ANY, "Special Search: ")
        self.specialToggle = wx.ToggleButton(self, wx.ID_ANY, label="OFF")
        self.specialToggle.Bind(wx.EVT_TOGGLEBUTTON, self.onToggle)

        diffLabel = wx.StaticText(self, wx.ID_ANY, "Minimum distance between alelles (Special Search): ")
        self.diffText = wx.TextCtrl(self, wx.ID_ANY, value=minDiff, size=(220, 30))

        gridSizer.Add(cntLabel, pos=(0, 0))
        gridSizer.Add(self.cntText, pos=(0, 1))
        gridSizer.Add(diffLabel, pos=(1, 0))
        gridSizer.Add(self.diffText, pos=(1, 1))
        gridSizer.Add(flankLabel, pos=(2, 0))
        gridSizer.Add(self.flankText, pos=(2, 1))
        gridSizer.Add(motifLabel, pos=(3, 0))
        gridSizer.Add(self.motifText, pos=(3, 1))
        gridSizer.Add(specialLabel, pos=(4, 0))
        gridSizer.Add(self.specialToggle, pos=(4, 1))

        self.SetSizer(gridSizer)
        self.Layout()

    def onToggle(self, event):
        if self.specialToggle.GetValue():
            self.specialToggle.SetLabel("ON")
        else:
            self.specialToggle.SetLabel("OFF")


class FrameSettings(wx.Frame):
    def __init__(self, parent=None, title="Micro-Primers", id=-1):
        wx.Frame.__init__(self, parent, id, title, size=(600, 500))

        self.panel = MyPanel(self)

        nb = wx.Notebook(self.panel)

        self.tabPreProcessing = TabPreProcessing(nb)
        self.tabPrimer = TabPrimer(nb)
        self.tabAllele = TabAlleles(nb)

        nb.AddPage(self.tabPreProcessing, "Pre-Processing")
        nb.AddPage(self.tabPrimer, "Primers")
        nb.AddPage(self.tabAllele, "Alleles")

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.panel.SetSizer(sizer)

    def OnClose(self, event):
        global cut3, cut5, grep, exclude, primer3_txt, minFlank, minMotif, minCnt, minDiff, special, primer3Filter

        cut3 = self.tabPreProcessing.cutText_3.GetValue()
        cut5 = self.tabPreProcessing.cutText_5.GetValue()
        if self.tabPreProcessing.grepToggle.GetValue():
            grep = ""
        exclude = self.tabPrimer.excludeText.GetValue()
        primer3_txt = self.tabPrimer.primer3Text.GetValue()
        primer3Filter = self.tabPrimer.filterToggle.GetValue()
        minFlank = self.tabAllele.flankText.GetValue()
        minMotif = self.tabAllele.motifText.GetValue()
        minCnt = self.tabAllele.cntText.GetValue()
        minDiff = self.tabAllele.diffText.GetValue()
        special = self.tabAllele.specialToggle.GetValue()

        try:
            int(minFlank)
        except ValueError:
            self.ErrorMessage("Minimal flanking region length", "integer")

        try:
            int(minMotif)
        except ValueError:
            self.ErrorMessage("Minimal motif repetition", "integer")

        try:
            int(minCnt)
        except ValueError:
            self.ErrorMessage("Minimal number of alleles in a cluster", "integer")

        try:
            int(minDiff)
        except ValueError:
            self.ErrorMessage("Minimal Distance between alleles", "integer")

        print("Getting Values...")

        self.Destroy()

    def ErrorMessage(self, errorLocation, errorType):
        errorMessage = wx.MessageBox( errorLocation + " is not a " + errorType + "." , errorLocation + " Error.")

class MyFrame(wx.Frame):

    def __init__(self, parent=None, title="Micro-Primers", id=-1):
        wx.Frame.__init__(self, parent, id, title, size=(600, 500))

        self.panel = MyPanel(self)

        menuBar = wx.MenuBar()

        helpm = wx.Menu()
        helpm.Append(wx.ID_ABOUT, "About")
        menuBar.Append(helpm, "&Help")

        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.onMenu)

        sizer = wx.BoxSizer(wx.VERTICAL)
        gridSizer = wx.GridBagSizer(hgap=5, vgap=5)

        labelTitle = wx.StaticText(self, wx.ID_ANY,
                                   "Micro-Primers - Design primers for microsattelite amplification")

        self.labelR1 = wx.StaticText(self, wx.ID_ANY, "Fastq R1:")
        self.textR1 = wx.TextCtrl(self, wx.ID_ANY, size=(220, 30))
        self.buttonR1 = wx.Button(self, label="Select")
        self.Bind(wx.EVT_BUTTON,
                  lambda event, box=self.textR1: self.get_path(event, box),
                  self.buttonR1)

        self.labelR2 = wx.StaticText(self, wx.ID_ANY, "Fastq R2:")
        self.textR2 = wx.TextCtrl(self, wx.ID_ANY, size=(220, 30))
        self.buttonR2 = wx.Button(self, label="Select")
        self.Bind(wx.EVT_BUTTON,
                  lambda event, box=self.textR2: self.get_path(event, box),
                  self.buttonR2)

        self.labelOut = wx.StaticText(self, wx.ID_ANY, "Output file name: ")
        self.textOut = wx.TextCtrl(self, wx.ID_ANY, size=(220, 30))

        self.labelPre = wx.StaticText(self, wx.ID_ANY, "Primer ID prefix: ")
        self.textPre = wx.TextCtrl(self, wx.ID_ANY, value="SSR", size=(220, 30))

        self.buttonSettings = wx.Button(self, label="Settings")
        self.Bind(wx.EVT_BUTTON, self.settings, self.buttonSettings)

        self.buttonRun = wx.Button(self, label="Run")
        self.Bind(wx.EVT_BUTTON, self.run, self.buttonRun)

        sizer.Add(labelTitle, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 20)

        gridSizer.Add(self.labelR1, pos=(0, 0))
        gridSizer.Add(self.textR1, pos=(0, 1))
        gridSizer.Add(self.buttonR1, pos=(0, 2))
        #
        gridSizer.Add(self.labelR2, pos=(1, 0))
        gridSizer.Add(self.textR2, pos=(1, 1))
        gridSizer.Add(self.buttonR2, pos=(1, 2))
        #
        gridSizer.Add(self.labelOut, pos=(2, 0))
        gridSizer.Add(self.textOut, pos=(2, 1))
        #
        gridSizer.Add(self.labelPre, pos=(3, 0))
        gridSizer.Add(self.textPre, pos=(3, 1))

        sizer.Add(gridSizer, 0, wx.CENTER)
        sizer.Add(self.buttonSettings, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 30)
        sizer.Add(self.buttonRun, 0, wx.CENTER)

        self.SetSizer(sizer)
        self.Layout()

    def onMenu(self, event):
        evt_id = event.GetId()
        if evt_id == wx.ID_ABOUT:
            self.panel = AboutFrame(self)
            self.panel.Show(True)
            return True

    def settings(self, event):
        self.settings = FrameSettings()
        self.settings.Show(True)
        return True

    def run(self, event):
        global r1, r2, cut3, cut5, exclude, primer3_txt, minFlank, minMotif, minCnt, minDiff, special, prefix, badSSR, out, primer3Filter
        self.running = True
        r1 = self.textR1.GetValue()
        r2 = self.textR2.GetValue()
        out = self.textOut.GetValue()
        prefix = self.textPre.GetValue()

        # Checking if path to input files exist.
        if os.path.exists(r1) == False or os.path.exists(r2) == False:
            # Error Message
            inputError = wx.MessageBox("One of the input files path is empty or incorrect.", "Input Error")

        else:
            badSSR = exclude.split(",")
            micro_primers_system_call("touch software/scripts/__init__.py", "Error: could not create init.py.")

            print(r1, r2, cut3, cut5, grep, minFlank, minMotif, badSSR, minCnt, special, minDiff, primer3_txt, primer3Filter)

            # Progress Bar
            self.progress = wx.ProgressDialog("Processing...", "Creating Folders...", maximum=18, parent=self,
                                              style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME | wx.PD_CAN_ABORT)

            workThread_pipeline = threading.Thread(target=self.pipeline_gui)
            workThread_updater = threading.Thread(target=self.updater)
            workThread_pipeline.start()
            workThread_updater.start()

    def updater(self):
        while self.running:
            time.sleep(1)
            wx.CallAfter(self.progress.Update, self.step)

        # self.progress.ShowModal()

    # Pipeline with GUI
    def pipeline_gui(self):
        folder([".temp/", "logs/"])

        wx.CallAfter(self.progress.Update, 1, 'Trimmomatic working...')
        self.step = 1
        trimmomatic(r1, r2)

        wx.CallAfter(self.progress.Update, 2, newmsg='Cutadapt working...')
        self.step = 2
        cutadapt(cut3, cut5)

        wx.CallAfter(self.progress.Update, 3, newmsg='Flash working...')
        self.step = 3
        flash()

        if grep == "":
            wx.CallAfter(self.progress.Update, 4, newmsg='Converting sequences from fastq to fasta...')
            self.step = 4
            fastq_to_fasta()
        else:
            wx.CallAfter(self.progress.Update, 4, newmsg='Selecting sequences with restriction enzyme pattern...')
            self.step = 4
            python_grep(grep)

        wx.CallAfter(self.progress.Update, 5, newmsg='Adding ids and Calculating sequences lengths...')
        self.step = 5
        ids_and_len()

        wx.CallAfter(self.progress.Update, 6, newmsg='Misa working...')
        self.step = 6
        misa()

        wx.CallAfter(self.progress.Update, 7, newmsg='Adding length to misa output...')
        self.step = 7
        length_merger()

        wx.CallAfter(self.progress.Update, 8, newmsg='Selecting good microsatellites...')
        self.step = 8
        good_micros(int(minFlank), int(minMotif), badSSR)

        wx.CallAfter(self.progress.Update, 9, newmsg='splitSSR working...')
        self.step = 9
        splitSSR()

        wx.CallAfter(self.progress.Update, 10, newmsg='CD-HIT working...')
        self.step = 10
        cdhit()

        wx.CallAfter(self.progress.Update, 11, newmsg='Calculating number of sequences for each cluster...')
        self.step = 11
        cluster()

        wx.CallAfter(self.progress.Update, 12, newmsg='Adding information to the table of microsatellites...')
        self.step = 12
        cluster_info()
        cluster_filter(int(minCnt), special, int(minDiff))

        wx.CallAfter(self.progress.Update, 13, newmsg='Selecting one sequence per cluster...')
        self.step = 13
        selected_micros()

        wx.CallAfter(self.progress.Update, 14, newmsg='Creating Primer3 input file...')
        self.step = 14
        primer3_input()
        size_check(special)

        wx.CallAfter(self.progress.Update, 15, newmsg='Creating Primers...')
        self.step = 15
        primer3(primer3_txt)

        wx.CallAfter(self.progress.Update, 16, newmsg='Selecting best primers...')
        self.step = 16
        output(primer3Filter)

        wx.CallAfter(self.progress.Update, 17, newmsg='Removing temporary files...')
        self.step = 17
        #junk()

        wx.CallAfter(self.progress.Update, 18, newmsg='Done! You can close the window!')
        self.step = 18
        self.running = False
        # self.progress.Destroy()
        print('Done!')

    def get_path(self, event, box):
        test_dir = wx.FileDialog(self, "Choose a directory:")
        if test_dir.ShowModal() == wx.ID_OK:
            path = test_dir.GetPath()
            box.write(path)
        test_dir.Destroy()


# Creation of hidden temp file
def folder(folders):
    for i in folders:
        if os.path.isdir(i) == False:
            micro_primers_system_call("mkdir %s" % (i), "Error: could not create %s directory." % (i))


# Sequences Triming of Sequencer adapters
def trimmomatic(R1, R2):
    print('Trimmomatic working...')
    micro_primers_system_call(
        "trimmomatic PE -phred33 "
        "%s %s "
        ".temp/trim_out_trimmed_R1.fastq .temp/trim_out_unpaired_R1.fastq "
        ".temp/trim_out_trimmed_R2.fastq .temp/trim_out_unpaired_R2.fastq "
        "ILLUMINACLIP:./software/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 "
        "LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 2> logs/trim_log.txt"
        % (R1, R2),
        "Error: Trimmomatic could not remove adapters")


# Adapters removal (specifics from technology)
def cutadapt(a, g):
    print('Cutadapt working...')
    micro_primers_system_call("cutadapt "
                              "-a %s "
                              "-g %s "
                              "-o .temp/cut_out_nolink_R1.fastq .temp/trim_out_trimmed_R1.fastq "
                              "> logs/cut_log_r1.txt"
                              % (a, g),
                              "Error: CutAdapt could not remove adapters from R1 sequence.")
    micro_primers_system_call("cutadapt "
                              "-a %s "
                              "-g %s "
                              "-o .temp/cut_out_nolink_R2.fastq .temp/trim_out_trimmed_R2.fastq "
                              "> logs/cut_log_r2.txt"
                              % (a, g),
                              "Error: CutAdapt could not remove adapters from R2 sequence.")


# Fusion of R1 and R2 files
def flash():
    print('Flash working...')
    micro_primers_system_call("flash "
                              ".temp/cut_out_nolink_R1.fastq "
                              ".temp/cut_out_nolink_R2.fastq "
                              "-M 220 -o .temp/flash_out 2>&1 |"
                              " tee logs/flash.log "
                              "> logs/flash_log.txt",
                              "Error: FLASH couldn0t merge sequences.")


# Selection of fragments that start and ends with the pattern of the restriction enzyme
def python_grep(grep_pattern):
    print('Selecting sequences with restriction enzyme patterns...')
    text_manip.python_grep(".temp/flash_out.extendedFrags.fastq", ".temp/grep_out.fasta", grep_pattern)


def fastq_to_fasta():
    print('Selecting sequences with restriction enzyme patterns...')
    text_manip.fastqToFasta(".temp/flash_out.extendedFrags.fastq", ".temp/grep_out.fasta")


# Change id's and Length Calculation for later selection of valid microsatellites
def ids_and_len():
    print('Adding ids...\nCalculating sequences lengths...')
    text_manip.change_ids_and_calc_len(".temp/grep_out.fasta", ".temp/ids_out.fasta", ".temp/length_calc_out.fasta")


# Search Microsatellites
def misa():
    print('Misa working...')
    micro_primers_system_call("perl software/scripts/misa.pl "
                              ".temp/ids_out.fasta "
                              "2> logs/misa_log.txt",
                              "Error: Misa failed")


# Adds length to end of the sequences to misa output
def length_merger():
    print('Adding length to misa output...')
    text_manip.length_merger(".temp/length_calc_out.fasta", ".temp/misa_out.misa", ".temp/length_add_out.misa")


# Selection of microssatelites with enough space for primer
def good_micros(MIN_FLANK_LEN, MIN_MOTIF_REP, EXC_MOTIF_TYPE):
    print('Selecting good microsatellites...')
    picker.matrix_picker(".temp/length_add_out.misa", ".temp/good_micros_out.fasta",
                         ".temp/good_micros_table_out.misa", MIN_FLANK_LEN, MIN_MOTIF_REP, EXC_MOTIF_TYPE)


# Extraction of the microsatellite sequence from allignement of fragments with flanking regions
def splitSSR():
    print('splitSSR working...')
    text_manip.split(".temp/good_micros_out.fasta", ".temp/ids_out.fasta", ".temp/split_out.fasta")


# Removal of Redundancy
def cdhit():
    print('CD-HIT working...')
    micro_primers_system_call("cd-hit-est "
                              "-o .temp/cdhit_out.txt "
                              "-i .temp/split_out.fasta "
                              "-c 0.90 "
                              "-n 10 "
                              "-T 10 "
                              "> logs/cdhit_log.txt",
                              "Error: CD-HIT failed")


# Cluster assignment
def cluster():
    print('Calculating number of sequences for each cluster...')
    text_manip.cluster(".temp/cdhit_out.txt.clstr", ".temp/clusters_out.txt")


# Adding cluster information to Microssatelites table
def cluster_info():
    print('Adding information to the table of microsatellites...')
    text_manip.add_cluster_info(".temp/clusters_out.txt", ".temp/good_micros_table_out.misa",
                                ".temp/cluster_info_out.txt")


def cluster_filter(MIN_ALLELE_CNT, MIN_ALLELE_SPECIAL, MIN_ALLELE_SPECIAL_DIF):
    picker.allele(".temp/cluster_info_out.txt", ".temp/cluster_filter_out.txt", MIN_ALLELE_CNT, MIN_ALLELE_SPECIAL,
                  MIN_ALLELE_SPECIAL_DIF)


# Selecting one sequence per cluster
def selected_micros():
    print('Selecting one sequence per cluster...')
    picker.selected_micros(".temp/cluster_filter_out.txt", ".temp/selected_micros_out_seqs.txt",
                           ".temp/selected_micros_out_tabs.txt")


# Creating input file for Primer3
def primer3_input():
    print('Creating Primer3 input file...')
    pre_primer.pseudofasta(".temp/selected_micros_out_seqs.txt", ".temp/ids_out.fasta",
                           ".temp/primer3_input_out.fasta")


# Check if primer3 input is empty
def size_check(SPECIAL_CASE):
    if os.path.getsize(".temp/primer3_input_out.fasta") < 1:
        print("Empty primer3 input file. \n")
        if not SPECIAL_CASE:
            sys.exit("No valid SSR's were selected. Try to use a broader search.")
        elif SPECIAL_CASE:
            sys.exit("No valid SSR's were selected.")


# Primer design and creation
def primer3(p3_settings):
    print('Creating Primers...')
    # software/primer3/src/./primer3_core
    micro_primers_system_call("primer3_core "
                                   "-default_version=2 -p3_settings_file={} "
                                   ".temp/primer3_input_out.fasta "
                                   "-output=.temp/primer3_out.primers "
                                   .format(p3_settings),
                                   "Error: Primer3 failed")


# Defining output name
def name(file_name):
    if out == "":
        output_name = file_name.split("_R")[0] + "_primers.txt"
    else:
        if out[-4::] == ".txt":
            output_name = out
        else:
            output_name = out + ".txt"
    return output_name


# Selection of primers following laboratory criteria and output formatting
def output(primer3Filter):
    print('Selecting best primers...')
    print('Creating final file...')
    pre_primer.final_primers(".temp/selected_micros_out_tabs.txt", ".temp/primer3_out.primers", name(r1),
                             prefix, primer3Filter)


# Removal of .temp directory
def junk():
    micro_primers_system_call("rm -r .temp/", "Error: could not remove .temp directory.")


def micro_primers_system_call(cmd, erro):
    rvalue = os.system(cmd)  # returns the exit code
    if rvalue != 0:
        sys.exit(erro)


class AboutFrame(wx.Frame):
    def __init__(self, parent=None, title="About", id=-1):
        wx.Frame.__init__(self, parent, id, title, size=(450, 250))
        # self.panel = MyPanel(self)

        boxSizer = wx.BoxSizer(wx.VERTICAL)
        authorSizer = wx.BoxSizer(wx.VERTICAL)

        whatLabel = wx.StaticText(self, wx.ID_ANY, "Micro-Primers - Design primers for microsattelite amplification")
        versionLabel = wx.StaticText(self, wx.ID_ANY, "Version: 1.0")
        author1Label = wx.StaticText(self, wx.ID_ANY, "Author(s):")
        author2Label = wx.StaticText(self, wx.ID_ANY, "Filipe Alves,  MSc")
        author3Label = wx.StaticText(self, wx.ID_ANY, "António Mérida Muñoz, PhD, CIBIO - inBIO")
        author4Label = wx.StaticText(self, wx.ID_ANY, "Miguel Areias, PhD, University of Porto - Faculty of Science ")

        authorSizer.Add(author1Label, 0, wx.ALIGN_CENTER)
        authorSizer.Add(author2Label, 0, wx.ALIGN_CENTER)
        authorSizer.Add(author3Label, 0, wx.ALIGN_CENTER)
        authorSizer.Add(author4Label, 0, wx.ALIGN_CENTER)

        boxSizer.AddSpacer(20)
        boxSizer.Add(whatLabel, 0, wx.ALIGN_CENTER)
        boxSizer.AddSpacer(50)
        boxSizer.Add(versionLabel, 0, wx.ALIGN_CENTER)
        boxSizer.AddSpacer(50)
        boxSizer.Add(authorSizer, 0, wx.ALIGN_CENTER)

        self.SetSizer(boxSizer)
        self.Layout()


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame()
        self.frame.Show(True)
        return True


# Pipeline for terminal mode.
def pipeline_terminal():
    folder([".temp/", "logs/"])
    trimmomatic(r1, r2)
    cutadapt(cut3, cut5)
    flash()

    if grep == "":
        fastq_to_fasta()
    else:
        python_grep(grep)

    ids_and_len()
    misa()
    length_merger()
    good_micros(int(minFlank), int(minMotif), exclude.split(","))
    splitSSR()
    cdhit()
    cluster()
    cluster_info()
    cluster_filter(int(minCnt), special, int(minDiff))
    selected_micros()
    primer3_input()
    size_check(special)
    primer3(primer3_txt)
    output(primer3Filter)
    junk()
    print('Done!')


if len(sys.argv) > 1:
    parser = argparse.ArgumentParser(
        description='Pipeline for identification and design of PCR primers for amplification of SSR loci.')
    parser.add_argument("-r1", "--fastqr1", metavar="", help="Path to R1 input file.")
    parser.add_argument("-r2", "--fastqr2", metavar="", help="Path to R2 input file.")
    parser.add_argument("-o", "--output", metavar="", help="Output file name.")
    parser.add_argument("-exc", "--exclude", metavar="", default="c,c*,p1",
                        help="SSR types to be excluded from search.")
    parser.add_argument("-enz", "--resenzime", metavar="", default="GATC",
                        help="Restriction enzime pattern. Default: GATC.")
    parser.add_argument("-spc", "--special", action="store_true", help="Activates special search. Default: False.")
    parser.add_argument("-p3f", "--p3filter", action="store_true", help="Filters primers designed inside SSR region. Default: False.")
    parser.add_argument("-p3", "--primer3", metavar="", default="primer3_setting.txt",
                        help="Path to primer3 settings file.")
    parser.add_argument("-c3", "--cutadapt3", metavar="", default="CCAAGCTTCCCGGGTACCGC",
                        help="Reverse adapter sequence (CutAdapt).")
    parser.add_argument("-c5", "--cutadapt5", metavar="", default="GCGGTACCCGGGAAGCTTGG",
                        help="Foward adapter sequence (CutAdapt).")
    parser.add_argument("-flank", "--minflank", metavar="", default="50",
                        help="Minimum length accepted in both flanking regions. Default: 50.")
    parser.add_argument("-cnt", "--mincount", metavar="", default="5",
                        help="Minimum number of alleles for a SSR loci. Default: 5.")
    parser.add_argument("-motif", "--minmotif", metavar="", default="5",
                        help="Minimum number of SSR motif repetitions. Default: 5.")
    parser.add_argument("-diff", "--mindiff", metavar="", default="8",
                        help="Minimum difference between the allele with higher number of repeats and the allele with a smaller number. Only used if special search is activated. Default: 8.")
    parser.add_argument("-p", "--prefix", metavar="", default="SSR",
                        help="Loci name on output file. Default: SSR.")

    args = parser.parse_args()

    r1 = args.fastqr1
    r2 = args.fastqr2
    cut3 = args.cutadapt3
    cut5 = args.cutadapt5
    grep = args.resenzime
    exclude = args.exclude
    primer3_txt = args.primer3
    minFlank = args.minflank
    minMotif = args.minmotif
    minCnt = args.mincount
    minDiff = args.mindiff
    special = args.special
    primer3Filter = args.p3filter
    prefix = args.prefix
    out = args.output

    pipeline_terminal()

else:
    r1 = ""
    cut3 = "CCAAGCTTCCCGGGTACCGC"
    cut5 = "GCGGTACCCGGGAAGCTTGG"
    grep = "GATC"
    exclude = "c,c*,p1"
    primer3_txt = "primer3_setting.txt"
    minFlank = "50"
    minMotif = "5"
    minCnt = "5"
    minDiff = "8"
    special = False
    primer3Filter = False
    out = ""

    app = MyApp()
    app.MainLoop()
