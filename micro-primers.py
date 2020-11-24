
from software.scripts import picker, text_manip, pre_primer
import sys, wx, os, time, threading

def micro_primers_system_call(cmd, erro):
    rvalue = os.system(cmd) # returns the exit code
    if rvalue != 0:
        sys.exit(erro)

#Create empty file for importing python scripts
micro_primers_system_call("touch software/scripts/__init__.py", "Error: could not create init.py.")

global cut3, cut5, exclude, primer3, minFlank, minMotif, minCnt, minDiff, special, r1
r1 = ""
cut3 = "CCAAGCTTCCCGGGTACCGC"
cut5 = "GCGGTACCCGGGAAGCTTGG"
exclude = "c,c*,p1"
primer3 = "primer3_setting.txt"
minFlank = "50"
minMotif = "5"
minCnt = "5"
minDiff = "8"
special = False

class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer(sizer)
        self.Layout()

class TabCutadapt(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        global cut3, cut5

        gridSizer = wx.GridBagSizer(hgap=5, vgap=5)
        sizerCut_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizerCut_5 = wx.BoxSizer(wx.HORIZONTAL)

        cutLabel_3 = wx.StaticText(self, wx.ID_ANY, "CutAdapt 3' adapter sequence:")
        self.cutText_3 = wx.TextCtrl(self, wx.ID_ANY, value = cut3, size=(220, 30))

        cutLabel_5 = wx.StaticText(self, wx.ID_ANY, "CutAdapt 5' adapter sequence:")
        self.cutText_5 = wx.TextCtrl(self, wx.ID_ANY, value = cut5, size=(220, 30))

        sizerCut_3.Add(cutLabel_3)
        sizerCut_3.Add(self.cutText_3)

        sizerCut_5.Add(cutLabel_5)
        sizerCut_5.Add(self.cutText_5)

        gridSizer.Add(sizerCut_3, pos=(0,0))
        gridSizer.Add(sizerCut_5, pos=(1,0))

        self.SetSizer(gridSizer)
        self.Layout()


class TabPrimer(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        global exclude, primer3, minFlank, minMotif


        gridSizer = wx.GridBagSizer(hgap=2, vgap=5)
        sizerExclude = wx.BoxSizer(wx.HORIZONTAL)
        sizerPrimer3 = wx.BoxSizer(wx.HORIZONTAL)


        self.excludeLabel = wx.StaticText(self, wx.ID_ANY, "Primers types to be excluded: ")
        self.excludeText = wx.TextCtrl(self, wx.ID_ANY, value = exclude, size=(220, 30))

        primer3Label = wx.StaticText(self, wx.ID_ANY, "Primer3 setting file:")
        self.primer3Text = wx.TextCtrl(self, wx.ID_ANY, value = primer3, size=(220, 30))
        primer3Button = wx.Button(self, label="Select")
        self.Bind(wx.EVT_BUTTON,
                  lambda event, box=self.primer3Text: self.get_path(event, box),
                  primer3Button)


        sizerExclude.Add(self.excludeLabel, wx.ALIGN_CENTER)
        #sizerExclude.Add(self.excludeText)

        sizerPrimer3.Add(self.primer3Text,wx.ALL | wx.ALIGN_CENTER)
        sizerPrimer3.Add(primer3Button)

        gridSizer.Add(sizerExclude, pos=(0, 0))
        gridSizer.Add(self.excludeText, pos=(0, 1))
        gridSizer.Add(primer3Label, pos=(1, 0))
        gridSizer.Add(sizerPrimer3, pos=(1, 1))

        self.SetSizer(gridSizer)
        self.Layout()

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
        self.cntText = wx.TextCtrl(self, wx.ID_ANY, value = minCnt, size=(220, 30))

        flankLabel = wx.StaticText(self, wx.ID_ANY, "Minimum flank region length: ")
        self.flankText = wx.TextCtrl(self, wx.ID_ANY, value = minFlank, size=(220, 30))

        motifLabel = wx.StaticText(self, wx.ID_ANY, "Minimum motif repetition: ")
        self.motifText = wx.TextCtrl(self, wx.ID_ANY, value = minMotif, size=(220, 30))

        specialLabel = wx.StaticText(self, wx.ID_ANY, "Special Search: ")
        self.specialToggle = wx.ToggleButton(self, wx.ID_ANY, label="Special Search OFF")
        self.specialToggle.Bind(wx.EVT_TOGGLEBUTTON, self.onToggle)

        diffLabel = wx.StaticText(self, wx.ID_ANY, "Minimum distance between alelles (Special Search): ")
        self.diffText = wx.TextCtrl(self, wx.ID_ANY, value = minDiff, size=(220, 30))

        gridSizer.Add(cntLabel, pos=(0,0))
        gridSizer.Add(self.cntText, pos=(0,1))
        gridSizer.Add(diffLabel, pos=(1,0))
        gridSizer.Add(self.diffText, pos=(1,1))
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
            self.specialToggle.SetLabel("Special Search ON")
        else:
            self.specialToggle.SetLabel("Special Search OFF")

class FrameSettings(wx.Frame):
    def __init__(self,parent=None, title="Micro-Primers", id=-1):

        wx.Frame.__init__(self, parent, id, title, size=(600,500))

        self.panel = MyPanel(self)

        nb = wx.Notebook(self.panel)

        self.tabCut = TabCutadapt(nb)
        self.tabPrimer = TabPrimer(nb)
        self.tabAllele = TabAlleles(nb)

        nb.AddPage(self.tabCut, "Cutadapt")
        nb.AddPage(self.tabPrimer, "Primers")
        nb.AddPage(self.tabAllele, "Alleles")

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.panel.SetSizer(sizer)


    def OnClose(self, event):
        global cut3, cut5, exclude, primer3, minFlank, minMotif, minCnt, minDiff, special

        cut3 = self.tabCut.cutText_3.GetValue()
        cut5 = self.tabCut.cutText_5.GetValue()
        exclude = self.tabPrimer.excludeText.GetValue()
        primer3 = self.tabPrimer.primer3Text.GetValue()
        minFlank = self.tabAllele.flankText.GetValue()
        minMotif = self.tabAllele.motifText.GetValue()
        minCnt = self.tabAllele.cntText.GetValue()
        minDiff = self.tabAllele.diffText.GetValue()
        special = self.tabAllele.specialToggle.GetValue()

        print("Getting Values...")

        self.Destroy()

class MyFrame(wx.Frame):

    step = 0
    running = True

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
        sizerR1 = wx.BoxSizer(wx.HORIZONTAL)
        sizerR2 = wx.BoxSizer(wx.HORIZONTAL)
        sizerPre = wx.BoxSizer(wx.HORIZONTAL)
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

        self.labelPre = wx.StaticText(self, wx.ID_ANY, "Primer ID Preffix: ")
        self.textPre = wx.TextCtrl(self, wx.ID_ANY, size=(220, 30))


        self.buttonSettings = wx.Button(self, label="Settings")
        self.Bind(wx.EVT_BUTTON, self.settings, self.buttonSettings)

        self.buttonRun = wx.Button(self, label="Run")
        self.Bind(wx.EVT_BUTTON, self.run, self.buttonRun)

        sizer.Add(labelTitle, 0, wx.CENTER | wx.TOP | wx.BOTTOM, 20)

        gridSizer.Add(self.labelR1, pos=(0,0))
        gridSizer.Add(self.textR1, pos=(0,1))
        gridSizer.Add(self.buttonR1, pos=(0,2))
        #
        gridSizer.Add(self.labelR2, pos=(1,0))
        gridSizer.Add(self.textR2, pos=(1,1))
        gridSizer.Add(self.buttonR2, pos=(1,2))
        #
        gridSizer.Add(self.labelPre, pos=(2,0))
        gridSizer.Add(self.textPre, pos=(2,1))

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
        global r1, r2, cut3, cut5, exclude, primer3, minFlank, minMotif, minCnt, minDiff, special, preffix, preffix, badSSR
        running = True
        r1 = self.textR1.GetValue()
        r2 = self.textR2.GetValue()
        preffix = self.textPre.GetValue()

        badSSR = exclude.split(",")
        self.micro_primers_system_call("touch software/scripts/__init__.py", "Error: could not create init.py.")

        print(r1, r2, cut3, cut5, minFlank, minMotif, badSSR, minCnt, special, minDiff, primer3)

        #Progress Bar
        self.progress = wx.ProgressDialog("Processing...", "Creating Folders...", maximum=18, parent=self, style=wx.PD_APP_MODAL|wx.PD_ELAPSED_TIME|wx.PD_CAN_ABORT)
        
        workThread_pipeline = threading.Thread(target=self.pipeline)
        workThread_updater = threading.Thread(target=self.updater)
        workThread_pipeline.start()
        workThread_updater.start()
        
    def updater(self):
        while self.running == True:
            time.sleep(1)
            wx.CallAfter(self.progress.Update, self.step)

        #self.progress.ShowModal()
        
    # Pipeline
    def pipeline(self):
        self.folder([".temp/", "logs/"])

        wx.CallAfter(self.progress.Update, 1, 'Trimmomatic working...')
        self.step = 1
        self.trimmomatic(r1, r2)
        
        wx.CallAfter(self.progress.Update, 2, newmsg='Cutadapt working...')
        self.step = 2
        self.cutadapt(cut3, cut5)
        
        wx.CallAfter(self.progress.Update, 3, newmsg='Flash working...')
        self.step = 3
        self.flash()
        
        wx.CallAfter(self.progress.Update, 4, newmsg='Selecting sequences with restriction enzime patterns...')
        self.step = 4
        self.python_grep()
        
        wx.CallAfter(self.progress.Update, 5, newmsg='Adding ids and Calculating sequences lengths...')
        self.step = 5
        self.ids_and_len()
        
        wx.CallAfter(self.progress.Update, 6, newmsg='Misa working...')
        self.step = 6
        self.misa()

        wx.CallAfter(self.progress.Update, 7, newmsg='Adding length to misa output...')
        self.step = 7
        self.length_merger()

        wx.CallAfter(self.progress.Update, 8, newmsg ='Selecting good microsatellites...')
        self.step = 8
        self.good_micros(int(50), int(5), badSSR)

        wx.CallAfter(self.progress.Update, 9, newmsg='splitSSR working...')
        self.step = 9
        self.splitSSR()

        wx.CallAfter(self.progress.Update, 10, newmsg='CD-HIT working...')
        self.step = 10
        self.cdhit()

        wx.CallAfter(self.progress.Update, 11, newmsg='Calculating number of sequences for each cluster...')
        self.step = 11
        self.cluster()

        wx.CallAfter(self.progress.Update, 12, newmsg='Adding information to the table of microsatellites...')
        self.step = 12
        self.cluster_info()
        self.cluster_filter(int(minCnt), special, int(minDiff))

        wx.CallAfter(self.progress.Update, 13, newmsg='Selecting one sequence per cluster...')
        self.step = 13
        self.selected_micros()

        wx.CallAfter(self.progress.Update, 14, newmsg='Creating Primer3 input file...')
        self.step = 14
        self.primer3_input()
        self.size_check(special)

        wx.CallAfter(self.progress.Update, 15, newmsg='Creating Primers...')
        self.step = 15
        self.primer3(primer3)

        wx.CallAfter(self.progress.Update, 16, newmsg='Selecting best primers...')
        self.step = 16
        self.output()

        wx.CallAfter(self.progress.Update, 17, newmsg='Removing temporary files...')
        self.step = 17
        #self.junk()

        wx.CallAfter(self.progress.Update, 18, newmsg='Done! You can close the window!')
        self.step = 18
        self.running = False
        #self.progress.Destroy()
        print('Done!')

    def get_path(self, event, box):
        test_dir = wx.FileDialog(self, "Choose a directory:")
        if test_dir.ShowModal() == wx.ID_OK:
            path = test_dir.GetPath()
            box.write(path)
        test_dir.Destroy()

    #Creation of hidden temp file
    def folder (self, folders):
        for i in folders:
            if os.path.isdir(i) == False:
                self.micro_primers_system_call("mkdir %s" %(i), "Error: could not create %s directory." %(i))


    #Sequences Triming of Sequencer adapters
    def trimmomatic(self, R1, R2):
        print('Trimmomatic working...')
        self.micro_primers_system_call(
            "java -jar software/Trimmomatic-0.36/trimmomatic-0.36.jar PE -phred33 "
            "%s %s "
            ".temp/trim_out_trimmed_R1.fastq .temp/trim_out_unpaired_R1.fastq "
            ".temp/trim_out_trimmed_R2.fastq .temp/trim_out_unpaired_R2.fastq "
            "ILLUMINACLIP:./software/Trimmomatic-0.36/adapters/TruSeq2-PE.fa:2:30:10 "
            "LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 2> logs/trim_log.txt"
            %(R1, R2),
            "Error: Trimmomatic could not remove adapters")

    #Adapters removal (specifics from technology)
    def cutadapt(self, a, g):
        print('Cutadapt working...')
        self.micro_primers_system_call("cutadapt "
                  "-a %s "
                  "-g %s "
                  "-o .temp/cut_out_nolink_R1.fastq .temp/trim_out_trimmed_R1.fastq "
                  "> logs/cut_log_r1.txt"
                  %(a, g),
                  "Error: CutAdapt could not remove adapters from R1 sequence.")
        self.micro_primers_system_call("cutadapt "
                  "-a %s "
                  "-g %s "
                  "-o .temp/cut_out_nolink_R2.fastq .temp/trim_out_trimmed_R2.fastq "
                  "> logs/cut_log_r2.txt"
                  %(a, g),
                  "Error: CutAdapt could not remove adapters from R2 sequence.")

    # Fusion of R1 and R2 files
    def flash(self):
        print('Flash working...')
        self.micro_primers_system_call("software/FLASH-1.2.11/flash "
                  ".temp/cut_out_nolink_R1.fastq "
                  ".temp/cut_out_nolink_R2.fastq "
                  "-M 220 -o .temp/flash_out 2>&1 |"
                  " tee logs/flash.log "
                  "> logs/flash_log.txt",
                  "Error: FLASH couldn0t merge sequences.")

    # Selecion of fragments that start and ends with the pattern of the restriction enzyme
    def python_grep(self):
        print('Selecting sequences with restriction enzime patterns...')
        text_manip.python_grep(".temp/flash_out.extendedFrags.fastq", ".temp/grep_out.fasta")

    #Change id's and Length Calculation for later selection of valid microsatellites
    def ids_and_len(self):
        print('Adding ids...\nCalculating sequences lengths...')
        text_manip.change_ids_and_calc_len(".temp/grep_out.fasta", ".temp/ids_out.fasta", ".temp/length_calc_out.fasta")

    #Search Microssatelites
    def misa(self):
        print('Misa working...')
        self.micro_primers_system_call("perl software/scripts/misa.pl "
                  ".temp/ids_out.fasta "
                  "2> logs/misa_log.txt",
                  "Error: Misa failed")

    #Adds length to end of the sequences to misa output
    def length_merger(self):
        print('Adding length to misa output...')
        text_manip.length_merger(".temp/length_calc_out.fasta", ".temp/misa_out.misa", ".temp/length_add_out.misa")

    #Selection of microssatelites with enough space for primer
    def good_micros(self, MIN_FLANK_LEN, MIN_MOTIF_REP, EXC_MOTIF_TYPE):
        print('Selecting good microsatellites...')
        picker.matrix_picker(".temp/length_add_out.misa", ".temp/good_micros_out.fasta",
                    ".temp/good_micros_table_out.misa", MIN_FLANK_LEN, MIN_MOTIF_REP, EXC_MOTIF_TYPE)

    #Extraction of the microsatellite sequence from allignement of fragments with flanking regions
    def splitSSR(self):
        print('splitSSR working...')
        text_manip.split(".temp/good_micros_out.fasta", ".temp/ids_out.fasta", ".temp/split_out.fasta")

    #Removal of Redundacy
    def cdhit(self):
        print('CD-HIT working...')
        self.micro_primers_system_call("software/cdhit/cd-hit-est "
                  "-o .temp/cdhit_out.txt "
                  "-i .temp/split_out.fasta "
                  "-c 0.90 "
                  "-n 10 "
                  "-T 10 "
                  "> logs/cdhit_log.txt",
                  "Error: CD-HIT failed")

    #Cluster assignement
    def cluster(self):
        print('Calculating number of sequences for each cluster...')
        text_manip.cluster(".temp/cdhit_out.txt.clstr", ".temp/clusters_out.txt")

    #Adding cluster information to Microssatelites table
    def cluster_info(self):
        print('Adding information to the table of microsatellites...')
        text_manip.add_cluster_info(".temp/clusters_out.txt", ".temp/good_micros_table_out.misa", ".temp/cluster_info_out.txt")

    def cluster_filter(self, MIN_ALLELE_CNT, MIN_ALLELE_SPECIAL, MIN_ALLELE_SPECIAL_DIF):
        picker.allele(".temp/cluster_info_out.txt", ".temp/cluster_filter_out.txt", MIN_ALLELE_CNT, MIN_ALLELE_SPECIAL, MIN_ALLELE_SPECIAL_DIF)

    # Selecting one sequence per cluster
    def selected_micros(self):
        print('Selecting one sequence per cluster...')
        picker.selected_micros(".temp/cluster_filter_out.txt", ".temp/selected_micros_out_seqs.txt", ".temp/selected_micros_out_tabs.txt")

    #Creating input file for Primer3
    def primer3_input(self):
        print('Creating Primer3 input file...')
        pre_primer.pseudofasta(".temp/selected_micros_out_seqs.txt", ".temp/ids_out.fasta", ".temp/primer3_input_out.fasta")

    #Check if primer3 input is empty
    def size_check(self, SPECIAL_CASE):
        if os.path.getsize(".temp/primer3_input_out.fasta") < 1:
            print("Empty primer3 input file. \n")
            if not SPECIAL_CASE:
                sys.exit("No valid SSR's were selected. Try to use a broader search.")
            elif SPECIAL_CASE:
                sys.exit("No valid SSR's were selected.")


    #Primer design and creation
    def primer3(self, p3_settings):
        print('Creating Primers...')
        self.micro_primers_system_call("software/primer3/src/./primer3_core "
                  "-default_version=2 -p3_settings_file=%s "
                  ".temp/primer3_input_out.fasta "
                  "-output=.temp/primer3_out.primers "
                  %(p3_settings),
                  "Error: Primer3 failed")


    #Defining output name
    def name(self, file_name):
        output_name = file_name.split("_R")[0] + "_primers.txt"
        return output_name

    #Selection of primers following laboratory criteria and output formatting
    def output(self):
        print('Selecting best primers...')
        print('Creating final file...')
        pre_primer.final_primers(".temp/selected_micros_out_tabs.txt", ".temp/primer3_out.primers", self.name(r1), preffix)

    #Removal of .temp directory
    def junk(self):
        self.micro_primers_system_call("rm -r .temp/", "Error: could not remove .temp directory.")

    def micro_primers_system_call(self, cmd, erro):
        rvalue = os.system(cmd)  # returns the exit code
        if rvalue != 0:
            sys.exit(erro)

class AboutFrame(wx.Frame):
    def __init__(self,parent=None, title="About", id=-1):
        wx.Frame.__init__(self, parent, id, title, size=(450,250))
        #self.panel = MyPanel(self)

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

app = MyApp()
app.MainLoop()
