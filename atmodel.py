import wx
from excel import ExcelXWriter, ExcelReader
import cal
import const
import numpy as np
import file_refs
import time

class atmodel(wx.Frame):
    def __init__(self, parent , title):
        super(atmodel, self).__init__(parent, title=title, size=(700, 550))
        self.InitUI()
        self.Centre()
        self.Show()     
        
    def InitUI(self):  #create GUI
        
        # Creating Panel 
        panel = wx.Panel(self)
        
        # Set panel font
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(14)
        
        # Create main container structures
        content = wx.BoxSizer(wx.VERTICAL)

        top = wx.BoxSizer(wx.HORIZONTAL)
        top_left = wx.BoxSizer(wx.VERTICAL)
        top_right = wx.BoxSizer(wx.VERTICAL)

        bottom = wx.BoxSizer(wx.HORIZONTAL)
        bottom_left = wx.BoxSizer(wx.VERTICAL)
        bottom_right = wx.BoxSizer(wx.VERTICAL)
        
        # Top_left
        top_left_fgs = wx.FlexGridSizer(7, 2, 6, 6)  # declare FlexibleGridSizer
        
        # Top_left -> parameters
        parameters = ['Specify Parameters', 'Spectral Resolution:',
                      'Mirror Diameter(m):', 'Mirror Temperature(K):',
                      'Choose a Site:', 'Choose a Source:', 'Choose Backgrounds:',
                      'Specify Starting Frequency(THz)', 'Specify Ending Frequency(THz)', 'Signal to Noise Ratio',
                      'Specify Dependent Minimum: 10 to the', 'Specify Dependent Maximum: 10 to the']
        sites = ['13_7Km SOFIA', '30KmBalloon', '40KmBalloon', 'CCAT-0732g', 'CCAT-0978g', 'DomeA-01g', 'DomeA-014g', 'DomeC-015g',
                 'DomeC-024g', 'MaunaKea-1g', 'MaunaKea-15g', 'SantaBarbara-01g', 'SantaBarbara-30g', 'SouthPole-023g',
                 'SouthPole-032g', 'WhiteMountain-115g', 'WhiteMountain-175g', 'Space', 'Custom']
        
        sources = ['NGC958_z=1', 'ARP220_z=1', 'MRK231_z=1', 'Custom']
        
        backgrounds = ['Cosmic Infrared Background', 'Cosmic Microwave Background', 'Galactic Emission', 'Thermal Mirror Emission',
                       'Atmospheric Radiance', 'Zodiacal Emission', 'Cumulative']
        
        # Top_left -> Controls
        parameter_labels = [wx.StaticText(panel, label=parameters[i]) for i in range(12)]
        self.parameter_inputs = [wx.TextCtrl(panel) for i in range(8)]
        self.parameter_site_combo = wx.ComboBox(panel, choices=sites, style=wx.CB_READONLY) 
        self.parameter_source_combo = wx.ComboBox(panel, choices=sources, style=wx.CB_READONLY)

        self.dependent_limits_checkbox = wx.CheckBox(panel, label='Manually Input Range of Dependent Axis')
        
        # Top_left -> fill up contains 
        parameter_labels[0].SetFont(font)  # set a title font
        top_left_fgs.Add(parameter_labels[0], flag=wx.EXPAND | wx.BOTTOM, border=6)
        top_left_fgs.Add(wx.StaticText(panel), flag=wx.EXPAND)  # empty grid
        top_left_fgs.AddMany([(parameter_labels[1], 0, wx.EXPAND), (self.parameter_inputs[0], 0, wx.EXPAND),
                              (parameter_labels[2], 0, wx.EXPAND), (self.parameter_inputs[1], 0, wx.EXPAND),
                              (parameter_labels[3], 0, wx.EXPAND), (self.parameter_inputs[2], 0, wx.EXPAND),
                              (parameter_labels[4], 0, wx.EXPAND), (self.parameter_site_combo, 0, wx.EXPAND),
                              (parameter_labels[5], 0, wx.EXPAND), (self.parameter_source_combo, 0, wx.EXPAND),
                              (parameter_labels[7], 0, wx.EXPAND), (self.parameter_inputs[3], 0, wx.EXPAND),
                              (parameter_labels[8], 0, wx.EXPAND), (self.parameter_inputs[4], 0, wx.EXPAND),
                              (parameter_labels[9], 0, wx.EXPAND), (self.parameter_inputs[5], 0, wx.EXPAND),
                              self.dependent_limits_checkbox, (wx.StaticText(panel, label='')),
                              (parameter_labels[10], 0, wx.EXPAND), (self.parameter_inputs[6], 0, wx.EXPAND),
                              (parameter_labels[11], 0, wx.EXPAND), (self.parameter_inputs[7], 0, wx.EXPAND)])
                              #each line represents a row in interface
        top_left.Add(top_left_fgs, flag=wx.EXPAND)

        # Top_left -> Bind eventhandler
        # self.parameter_site_combo.Bind(wx.EVT_COMBOBOX, self.onCustom)

        # Top_right
        galactic_directions = ['g_long = 0, g_lat = 0', 'g_long = 0, g_lat = 45', 'g_long = 0, g_lat = +90', 'g_long = 0, g_lat = -90']
        zodiacal_directions = ['g_long = 0, g_lat = 0', 'g_long = 0, g_lat = 45', 'g_long = 0, g_lat = 90']
        thermal_mirror_materials = ['Be', 'Al', 'Au', 'Ag']
        
        # Top_right -> controls
        self.background_checkboxs = [wx.CheckBox(panel, label=backgrounds[i]) for i in range(len(backgrounds))]
        self.galactic_direction_combo = wx.ComboBox(panel, choices=galactic_directions, style=wx.CB_READONLY) 
        self.zodiacal_direction_combo = wx.ComboBox(panel, choices=zodiacal_directions, style=wx.CB_READONLY)
        self.thermal_mirror_material_combo = wx.ComboBox(panel, choices=thermal_mirror_materials, style=wx.CB_READONLY)
        
        # Top_right -> fill up contents
        top_right.Add(parameter_labels[6], flag=wx.BOTTOM, border=6)
        top_right.Add(self.background_checkboxs[0], flag=wx.BOTTOM, border=3)
        top_right.Add(self.background_checkboxs[1], flag=wx.BOTTOM, border=3)
        top_right.Add(self.background_checkboxs[2], flag=wx.BOTTOM, border=3)
        top_right.Add(self.galactic_direction_combo, flag=wx.LEFT, border=20)
        top_right.Add(self.background_checkboxs[3], flag=wx.BOTTOM | wx.TOP, border=3)
        top_right.Add(self.thermal_mirror_material_combo, flag=wx.LEFT, border=20)
        top_right.Add(self.background_checkboxs[4], flag=wx.BOTTOM | wx.TOP, border=3)
        top_right.Add(self.background_checkboxs[5], flag=wx.BOTTOM, border=3)
        top_right.Add(self.zodiacal_direction_combo, flag=wx.LEFT, border=20)
        top_right.Add(self.background_checkboxs[6], flag=wx.BOTTOM, border=3)
        

        # Bottom_left 
        # Bottom_left -> Controls
        generate_label = wx.StaticText(panel, label='Generates:')
        generate_label.SetFont(font)  # Title

        generates = ['Total Noise', 'Total Temperature', 'Total Signal', 'Limiting Flux', 'Integration time'] 
        self.generate_checkboxs = [wx.CheckBox(panel, label=generates[i]) for i in range(len(generates))]

        # Bottom_left -> Fill up contents
        bottom_left.Add(generate_label, flag=wx.BOTTOM, border=10)
        for i in range(len(generates)):
            bottom_left.Add(self.generate_checkboxs[i], flag=wx.BOTTOM, border=3)

        # Bottom_right
        # Bottom_right -> Output -> Controls
        output_sizer = wx.BoxSizer(wx.HORIZONTAL)
        output_label = wx.StaticText(panel, label='Output to:')
        self.output_input = wx.TextCtrl(panel, size=(200, 30))
        output_button = wx.Button(panel, size=(80, 30), label='Browse')
        
        # Bottom_right -> Output -> Fill up contents
        bottom_right.Add(output_label, flag=wx.TOP, border=20)
        output_sizer.Add(self.output_input, flag=wx.EXPAND)
        output_sizer.Add(output_button)
        bottom_right.Add(output_sizer, flag=wx.BOTTOM, border=8)

        # Bottom_right -> Buttons
        generate_button = wx.Button(panel, label='Generate')
        cancel_button = wx.Button(panel, label='Cancel')
        
        # Bottom_right -> Buttons -> Fill up
        bottom_right.Add(generate_button, flag=wx.EXPAND | wx.BOTTOM, border=3)
        bottom_right.Add(cancel_button, flag=wx.EXPAND)

        # Bottom_right -> Function Bindings
        output_button.Bind(wx.EVT_BUTTON, self.onBrowse)
        generate_button.Bind(wx.EVT_BUTTON, self.onGenerate)
        cancel_button.Bind(wx.EVT_BUTTON, self.onCancel)
        
        # Fill up contents
        top.Add(top_left, flag=wx.RIGHT | wx.BOTTOM, border=25)
        top.Add(top_right, flag=wx.TOP | wx.BOTTOM, border=25)
        bottom.Add(bottom_left, flag=wx.RIGHT, border=35)
        bottom.Add(bottom_right, flag=wx.LEFT, border=35)
        content.Add(top, flag=wx.TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        content.Add(bottom, flag=wx.TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        panel.SetSizer(content)

    def onCustom(self, e):
        # Generate frame and grid
        self.site_dialog = wx.Frame(self, title="Custom Site Files:", size=(300, 150)) 
        site_dialog_fgs = wx.FlexGridSizer(2, 3, 6, 6)  # declare FlexibleGridSizer

        # Generate
        self.site_dialog_labels = [wx.StaticText(self.site_dialog, label="Specify radiance file:"), wx.StaticText(self.site_dialog, label="specify transimission file:"), wx.StaticText(self.site_dialog, label=""), wx.StaticText(self.site_dialog, label="")]
        site_dialog_buttons = [wx.Button(self.site_dialog, label="Browse") for i in range(2)]
        site_dialog_ok = wx.Button(self.site_dialog, label="Ok")
        site_dialog_fgs.Add(self.site_dialog_labels[0], flag=wx.EXPAND | wx.TOP | wx.LEFT, border=20)
        site_dialog_fgs.Add(self.site_dialog_labels[2], flag=wx.EXPAND | wx.TOP, border=20)
        site_dialog_fgs.Add(site_dialog_buttons[0], flag=wx.EXPAND | wx.TOP | wx.RIGHT, border=20)
        site_dialog_fgs.Add(self.site_dialog_labels[1], flag=wx.EXPAND | wx.LEFT, border=20)
        site_dialog_fgs.Add(self.site_dialog_labels[3], flag=wx.EXPAND, border=20)
        site_dialog_fgs.Add(site_dialog_buttons[1], flag=wx.EXPAND | wx.RIGHT, border=20)
        site_dialog_fgs.AddMany([wx.StaticText(self.site_dialog, label="") for i in range(2)])
        site_dialog_fgs.Add(site_dialog_ok, flag=wx.EXPAND | wx.RIGHT, border=20)
        self.site_dialog.SetSizer(site_dialog_fgs)
        site_dialog_ok.Bind(wx.EVT_BUTTON, self.onDialogOk)

        self.site_dialog.Center()
        self.site_dialog.Show()

    def onRadianceBrowse(self, e):
        file_dialog = wx.FileDialog(self, style=wx.FD_SAVE)
        if file_dialog.ShowModal() == wx.ID_OK:  
            file_dialog.Destroy()      
        return
    def onTransmissionBrowse(self, e):
        return
    def onDialogOk(self, e):
        self.site_dialog.Destroy()

    def onBrowse(self, e):
        file_dialog = wx.FileDialog(self, style=wx.FD_OPEN)
        if file_dialog.ShowModal() == wx.ID_OK:
            self.path = file_dialog.GetPath()

            self.output_input.Clear()
            self.output_input.WriteText(self.path)  
        file_dialog.Destroy()        
        
    def onGenerate(self, e):
        
# initialization -> Parse inputs

        freq_start = float(self.parameter_inputs[3].GetValue())  #get starting frequency input as a float
        freq_end = float(self.parameter_inputs[4].GetValue())  #get ending frequency input as a float
        #The preceding lines requires there to be inputs for resolution, starting frequency, and ending frequency
            #so the other inputs are only required to have entries if they are needed in the calculation that is checked

        if self.generate_checkboxs[0].IsChecked() or self.generate_checkboxs[2].IsChecked() or self.generate_checkboxs[3].IsChecked() or self.generate_checkboxs[4].IsChecked():  #only need resolution if any option other than "Total Temperature" is checked
            resol = float(self.parameter_inputs[0].GetValue())  #get resolution input as a float

        path = self.output_input.GetValue()  #get input as name of file to be written
        site = self.parameter_site_combo.GetValue()  #get name of chosen site
        source = self.parameter_source_combo.GetValue()  #get name of chosen source


# Calculate BLING
        if self.generate_checkboxs[0].IsChecked() or self.generate_checkboxs[4].IsChecked():  #only do BLING calculations if "Total Noise" or "Integration Time" is checked
            start_time = time.time()  #begins clock for calculation time   
            bling_squared = 0  #checking boxes for different backgrounds will add values to this "bling_squared" array
                #the squares of BLINGs are added up since the final result is equal to BLINGs added in quadrature
            title_bling = []  #append names of which backgrounds are checked to put in title

#if "Cosmic Infrared Background" box or "Cumulative" is checked
            if self.background_checkboxs[0].IsChecked() or self.background_checkboxs[6].IsChecked():
                title_bling.append('Cosmic Infrared Background')
                cib_excel = file_refs.CIB_ref  #name excel file to read from
                cib = ExcelReader(cib_excel)
                cib.set_freq_range_Hz(freq_start * 1e12, freq_end * 1e12)  #set where in excel file to start/stop reading by converting input from THz to Hz
                print "Reading array from", cib_excel
                freqNoise = np.array(cib.read_from_col(1), dtype="float")  #create array of frequency(Hz) from 2nd column of excel file, reading as floats
                freqNoise_THz = freqNoise * 10 ** (-12)  #create array that converts "freqNoise" into THz
                print "len(freq)=", len(freqNoise)
                temp = np.array(cib.read_from_col(4), dtype="float")  #create array of temperature(K) from 5th column of excel file, reading as floats
                print "len(temp)=", len(temp)
                bling_squared += cal.bling_sub(freqNoise, temp, resol)  #calculate and add BLING(squared) of Cosmic Infrared Background to "bling_squared"

#if "Cosmic Microwave Background" or "Cumulative" box is checked
            if self.background_checkboxs[1].IsChecked() or self.background_checkboxs[6].IsChecked():
                title_bling.append('Cosmic Microwave Background')
                cmb_excel = file_refs.CMB_ref  #name excel file to read from
                cmb = ExcelReader(cmb_excel)
                cmb.set_freq_range_Hz(freq_start * 1e12, freq_end * 1e12)  #set where in excel file to start/stop reading by converting input from THz to Hz
                print "Reading array from", cmb_excel
                freqNoise = np.array(cmb.read_from_col(1), dtype="float")  #create array of frequency(Hz) from 2nd column of excel file, reading as floats
                freqNoise_THz = freqNoise * 10 ** (-12)  #create array that converts "freqNoise" into THz
                bling_squared += cal.bling_CMB(freqNoise, resol)  #calculate and add BLING(squared) of Cosmic Microwave Background to "bling_squared"

#if "Galactic Emission" box or "Cumulative" is checked
            if self.background_checkboxs[2].IsChecked() or self.background_checkboxs[6].IsChecked():
                index = self.galactic_direction_combo.GetCurrentSelection()  #creates "index"=0, 1, 2, or 3 depending on which ecliptic coordinates are selected 
                if index == 0:  #if (g_long=0, g_lat=0) is selected
                    title_bling.append('Galactic Emission(g_long=0, g_lat=0)')
                elif index == 1:  #if (g_long=0, g_lat=45) is selected
                    title_bling.append('Galactic Emission(g_long=0, g_lat=45)')
                elif index == 2:  #if (g_long=0, g_lat=90) is selected
                    title_bling.append('Galactic Emission(g_long=0, g_lat=90)')
                elif index == 3:  #if (g_long=0, g_lat=-90) is selected
                    title_bling.append('Galactic Emission(g_long=0, g_lat=-90)')
                ge = ExcelReader(file_refs.Galatic_Emission_refs[index])  #name excel file to read from
                ge.set_freq_range_Hz(freq_start * 1e12, freq_end * 1e12)  #set where in excel file to start/stop reading by converting input from THz to Hz
                freqNoise = np.array(ge.read_from_col(1), dtype='float')  #create array of frequency(Hz) from 2nd column of excel file, reading as floats
                freqNoise_THz = freqNoise * 10 ** (-12)  #create array that converts "freqNoise" into THz
                temp = np.array(ge.read_from_col(8), dtype='float')  #create array of temperature(K) from 9th column of excel file, reading as floats
                bling_squared += cal.bling_sub(freqNoise, temp, resol)  #calculate and add BLING(squared) of Galactic Emission to "bling_squared"

#if "Thermal Mirror Emission" or "Cumulative" box is checked 
            if self.background_checkboxs[3].IsChecked() or self.background_checkboxs[6].IsChecked():
                mirror_temp = float(self.parameter_inputs[2].GetValue())  #only need mirror temperature input if "Thermal Mirror Emission" is checked
                index = self.thermal_mirror_material_combo.GetCurrentSelection()  #creates "index"=0, 1, 2, or 3 depending on which material is selected
                if index == 0:  #if "Be" is selected
                    title_bling.append('Thermal Mirror Emission(Beryllium)')
                if index == 1:  #if "Al" is selected
                    title_bling.append('Thermal Mirror Emission(Aluminum)')
                if index == 2:  #if "Au" is selected
                    title_bling.append('Thermal Mirror Emission(Gold)')
                if index == 3:  #if "Ag" is selected
                    title_bling.append('Thermal Mirror Emission(Silver)')
                tme = ExcelReader(file_refs.TME_ref)  #name excel file to read from
                tme.set_freq_range_Hz(freq_start * 1e12, freq_end * 1e12)  #set where in excel file to start/stop reading by converting input from THz to Hz
                freqNoise = np.array(tme.read_from_col(1), dtype = 'float')  #create array of frequency(Hz) from 2nd column of excel file, reading as floats
                freqNoise_THz = freqNoise * 10 ** (-12)  #create array that converts "freqNoise" into THz
                sigma = const.sigma[index]  #from file "const", get "Material Constant" depending on which material is selected
                wavelength = np.array(tme.read_from_col(3), dtype = 'float')  #create array of wavelengths(microns)
                bling_squared += cal.bling_TME(freqNoise, resol, sigma, mirror_temp, wavelength)  #calculate and add BLING(squared) of Thermal Mirror Emission to "bling_sqared"

#if "Atmospheric Radiance" or "Cumulative" box is checked
            if self.background_checkboxs[4].IsChecked() or self.background_checkboxs[6].IsChecked():
                title_bling.append('Atmospheric Radiance') #title depends on name of site chosen
                if site == "Custom":  #find transmission file from custom site
                    file_dialog = wx.FileDialog(self, style=wx.FD_OPEN)  #open browser to select file
                    if file_dialog.ShowModal() == wx.ID_OK:
                        self.site_rad = file_dialog.GetPath()
                        ar = ExcelReader(self.site_rad)
                    file_dialog.Destroy()
                else:  #if site not custom, find file
                    ar = ExcelReader(file_refs.atm_rad_refs[site])  #name excel file to read from, depending on site chosen
                ar.set_freq_range_Hz(freq_start * 1e12, freq_end * 1e12)  #set where in excel file to start/stop reading by converting input from THz to Hz
                freqNoise = np.array(ar.read_from_col(1), dtype='float')  #create array of frequency(Hz) from 2nd column of excel file, reading as floats
                freqNoise_THz = freqNoise * 10 ** (-12)  #create array that converts "freqNoise" into THz
                rad = np.array(ar.read_from_col(4), dtype='float')  #create array of radiance(W/cm^2/st/cm^-1) from 5th column of excel file, reading as floats
                bling_squared += cal.bling_AR(freqNoise, rad, resol)  #calculate and add BLING(squared) of Atmospheric Radiance to "bling_squared"

#if "Zodiacial Emission" or "Cumulative" box is checked
            if self.background_checkboxs[5].IsChecked() or self.background_checkboxs[6].IsChecked():
                index = self.zodiacal_direction_combo.GetCurrentSelection()  #creates "index"=0, 1, 2, or 3 depending on which ecliptic coordinates are selected
                if index == 0:  #if (g_long=0,g_lat=0) is selected
                    title_bling.append('Zodiacal Emission(g_long=0,g_lat=0)')
                if index == 1:  #if (g_long=0,g_lat=45) is selected
                    title_bling.append('Zodiacal Emission(g_long=0,g_lat=45)')
                if index == 2:  #if (g_long=0,g_lat=90) is selected
                    title_bling.append('Zodiacal Emission(g_long=0,g_lat=90)')
                ze = ExcelReader(file_refs.ZODI_refs[index])  #name excel file to read from, depending on site chosen
                ze.set_freq_range_Hz(freq_start * 1e12, freq_end * 1e12)  #set where in excel file to start/stop reading by converting input from THz to Hz
                freqNoise = np.array(ze.read_from_col(1), dtype='float')  #create array of frequency(Hz) from 2nd column of excel file, reading as floats
                freqNoise_THz = freqNoise * 10 ** (-12)  #create array that converts "freqNoise" into THz
                temp = np.array(ze.read_from_col(4), dtype='float')  #create array of temperature(K) from 5th column of excel file, reading as floats
                bling_squared += cal.bling_sub(freqNoise, temp, resol)  #calculate and add BLING(squared) of Zodiacal Emission to "bling_squared"
            
            bling_TOT = (bling_squared) ** 0.5  #"bling_squared" is the sum of the squared bling of each background so "bling_TOT" is the radical of "bling_squared" since the result is the BLINGS added in quadrature
            end_time = time.time()  #stops clock for calculation time
            print "BLING calculation DONE"
            print bling_TOT
            print "Time used for BLING calculation: ", end_time - start_time, " seconds"

            if self.background_checkboxs[6].IsChecked():  #setting title to 'Noise[Total]' if all BLINGs are checked
                title_bling = '[Total]'


# Calculate Antenna Temperature
        if self.generate_checkboxs[1].IsChecked():
            start_time = time.time()  #begins clock for calculation time   
            temperature = 0  #checking boxes for different backgrounds will add values to this "temperature" array
            title_temp = []  #append names of which backgrounds are checked to put in title

#if "Cosmic Infrared Background" box is checked
            if self.background_checkboxs[0].IsChecked() or self.background_checkboxs[6].IsChecked():
                title_temp.append('Cosmic Infrared Background')
                cib_excel = file_refs.CIB_ref  #name excel file to read from
                cib = ExcelReader(cib_excel)
                cib.set_freq_range_Hz(freq_start * 1e12, freq_end * 1e12)  #set where in excel file to start/stop reading by converting input from THz to Hz
                print "Reading array from", cib_excel
                freqNoise = np.array(cib.read_from_col(1), dtype="float")  #create array of frequency(Hz) from 2nd column of excel file, reading as floats
                freqNoise_THz = freqNoise * 10 ** (-12)  #create array that converts "freqNoise" into THz
                temp = np.array(cib.read_from_col(4), dtype="float")  #create array of temperature(K) from 5th column of excel file, reading as floats
                temperature += temp  #no calculations are needed to add temperature of Cosmic Infrared Background to "temperature"

#if "Cosmic Microwave Background" box is checked
            if self.background_checkboxs[1].IsChecked() or self.background_checkboxs[6].IsChecked():
                title_temp.append('Cosmic Microwave Background')
                cmb_excel = file_refs.CMB_ref  #name excel file to read from
                cmb = ExcelReader(cmb_excel)
                cmb.set_freq_range_Hz(freq_start * 1e12, freq_end * 1e12)  #set where in excel file to start/stop reading by converting input from THz to Hz
                print "Reading array from", cmb_excel
                freqNoise = np.array(cmb.read_from_col(1), dtype="float")  #create array of frequency(Hz) from 2nd column of excel file, reading as floats
                freqNoise_THz = freqNoise * 10 ** (-12)  #create array that converts "freqNoise" into THz
                temperature += cal.temp_CMB(freqNoise)  #calculate and add temperature of Cosmic Microwave Background to "temperature"

#if "Galactic Emission" box is checked
            if self.background_checkboxs[2].IsChecked() or self.background_checkboxs[6].IsChecked():
                index = self.galactic_direction_combo.GetCurrentSelection()  #creates "index"=0, 1, 2, 3, or 4 depending on which ecliptic coordinates are selected 
                if index == 0:  #if (g_long=0, g_lat=0) is selected
                    title_temp.append('Galactic Emission(g_long=0, g_lat=0)')
                elif index == 1:  #if (g_long=0, g_lat=45) is selected
                    title_temp.append('Galactic Emission(g_long=0, g_lat=45)')
                elif index == 2:  #if (g_long=0, g_lat=90) is selected
                    title_temp.append('Galactic Emission(g_long=0, g_lat=90)')
                elif index == 3:  #if (g_long=0, g_lat=-90) is selected
                    title_temp.append('Galactic Emission(g_long=0, g_lat=-90)')
                ge = ExcelReader(file_refs.Galatic_Emission_refs[index])  #name excel file to read from
                ge.set_freq_range_Hz(freq_start * 1e12, freq_end * 1e12)  #set where in excel file to start/stop reading by converting input from THz to Hz
                freqNoise = np.array(ge.read_from_col(1), dtype='float')  #create array of frequency(Hz) from 2nd column of excel file, reading as floats
                freqNoise_THz = freqNoise * 10 ** (-12)  #create array that converts "freqNoise" into THz
                temp = np.array(ge.read_from_col(8), dtype='float')  #create array of temperature(K) from 9th column of excel file, reading as floats
                temperature += temp  #no calculations are needed to add temperature of Galactic Emission to "temperature"

#if "Thermal Mirror Emission" box is checked 
            if self.background_checkboxs[3].IsChecked() or self.background_checkboxs[6].IsChecked():
                mirror_temp = float(self.parameter_inputs[2].GetValue())  #only need mirror temperature input if "Thermal Mirror Emission" is checked
                index = self.thermal_mirror_material_combo.GetCurrentSelection()  #creates "index"=0, 1, 2, or 3 depending on which material is selected
                if index == 0:  #if "Be" is selected
                    title_temp.append('Thermal Mirror Emission(Beryllium)')
                if index == 1:  #if "Al" is selected
                    title_temp.append('Thermal Mirror Emission(Aluminum)')
                if index == 2:  #if "Au" is selected
                    title_temp.append('Thermal Mirror Emission(Gold)')
                if index == 3:  #if "Ag" is selected
                    title_temp.append('Thermal Mirror Emission(Silver)')
                tme = ExcelReader(file_refs.TME_ref)  #name excel file to read from
                tme.set_freq_range_Hz(freq_start * 1e12, freq_end * 1e12)  #set where in excel file to start/stop reading by converting input from THz to Hz
                freqNoise = np.array(tme.read_from_col(1), dtype = 'float')  #create array of frequency(Hz) from 2nd column of excel file, reading as floats
                freqNoise_THz = freqNoise * 10 ** (-12)  #create array that converts "freqNoise" into THz
                sigma = const.sigma[index]  #from file "const", get "Material Constant" depending on which material is selected
                wavelength = np.array(tme.read_from_col(3), dtype = 'float')  #create array of wavelengths(microns)
                temperature += cal.temp_TME(freqNoise, sigma, mirror_temp, wavelength)  #calculate and add temperature of Thermal Mirror Emission to "temperature"

#if "Atmospheric Radiance" box is checked
            if self.background_checkboxs[4].IsChecked() or self.background_checkboxs[6].IsChecked():
                title_temp.append('Atmospheric Radiance') #title depends on name of site chosen
                if site == "Custom":  #find transmission file from custom site
                    file_dialog = wx.FileDialog(self, style=wx.FD_OPEN)  #open browser to select file
                    if file_dialog.ShowModal() == wx.ID_OK:
                        self.site_rad = file_dialog.GetPath()
                        ar = ExcelReader(self.site_rad)
                    file_dialog.Destroy()
                else:  #if site not custom, find file
                    ar = ExcelReader(file_refs.atm_rad_refs[site])  #name excel file to read from, depending on site chosen
                ar.set_freq_range_Hz(freq_start * 1e12, freq_end * 1e12)  #set where in excel file to start/stop reading by converting input from THz to Hz
                freqNoise = np.array(ar.read_from_col(1), dtype='float')  #create array of frequency(Hz) from 2nd column of excel file, reading as floats
                freqNoise_THz = freqNoise * 10 ** (-12)  #create array that converts "freqNoise" into THz
                rad = np.array(ar.read_from_col(4), dtype='float')  #create array of radiance(W/cm^2/st/cm^-1) from 5th column of excel file, reading as floats
                temperature += cal.temp_AR(freqNoise, rad)  #calculate and add temperature of Atmospheric Radiance to "temperature"

#if "Zodiacial Emission" box is checked
            if self.background_checkboxs[5].IsChecked() or self.background_checkboxs[6].IsChecked():
                index = self.zodiacal_direction_combo.GetCurrentSelection()  #creates "index"=0, 1, 2, or 3 depending on which ecliptic coordinates are selected
                if index == 0:  #if (g_long=0,g_lat=0) is selected
                    title_temp.append('Zodiacal Emission(g_long=0,g_lat=0)')
                if index == 1:  #if (g_long=0,g_lat=45) is selected
                    title_temp.append('Zodiacal Emission(g_long=0,g_lat=45)')
                if index == 2:  #if (g_long=0,g_lat=90) is selected
                    title_temp.append('Zodiacal Emission(g_long=0,g_lat=90)')
                ze = ExcelReader(file_refs.ZODI_refs[index])  #name excel file to read from, depending on site chosen
                ze.set_freq_range_Hz(freq_start * 1e12, freq_end * 1e12)  #set where in excel file to start/stop reading by converting input from THz to Hz
                freqNoise = np.array(ze.read_from_col(1), dtype='float')  #create array of frequency(Hz) from 2nd column of excel file, reading as floats
                freqNoise_THz = freqNoise * 10 ** (-12)  #create array that converts "freqNoise" into THz
                temp = np.array(ze.read_from_col(4), dtype='float')  #create array of temperature(K) from 5th column of excel file, reading as floats
                temperature += temp  #no calculations are needed to add temperature of Zodiacal Emission to "temperature"
            
            end_time = time.time()  #stops clock for calculation time
            print "Temperature calculation DONE"
            print "Time used for temperature calculation: ", end_time - start_time, " seconds"

            if self.background_checkboxs[6].IsChecked():  #setting title to 'Temperature[Total]' if all backgrounds are checked
                title_temp = '[Total]'


        if self.generate_checkboxs[2].IsChecked() or self.generate_checkboxs[4].IsChecked():  #only do signal calculation if "Total Signal" or "Integration Time" is checked
# Calculate Source Intensity
            d = float(self.parameter_inputs[1].GetValue())  #only need mirror diameter input if "Total Signal" is checked
            if source == "Custom":  #find file of custom source
                file_dialog = wx.FileDialog(self, style=wx.FD_OPEN)  #open browser to select file
                if file_dialog.ShowModal() == wx.ID_OK:
                    self.source = file_dialog.GetPath()
                    at = ExcelReader(self.source)
                file_dialog.Destroy()
            else:  #if source not custom, find file
                si = ExcelReader(file_refs.source_refs[source])  #find file of source galaxy
            si.set_freq_range_Hz(freq_start*10**12, freq_end*10**12)  #set where in excel file to start/stop reading by converting input from THz to Hz
            freq = np.array(si.read_from_col(1), dtype='float')  #create list of frequency(Hz) from 2nd column of excel file
            inte = np.array(si.read_from_col(5), dtype='float')  #create list of intensity(Jy) from 6th column of excel file, reading as floats
            print "Reading from source. DONE"
            
# Calculate Total Signal
            if site == "Custom":  #find transmission file from custom site
                file_dialog = wx.FileDialog(self, style=wx.FD_OPEN)  #open browser to select file
                if file_dialog.ShowModal() == wx.ID_OK:
                    self.site_trans = file_dialog.GetPath()
                    at = ExcelReader(self.site_trans)
                file_dialog.Destroy()
            else:  #if site not custom, find file
                at = ExcelReader(file_refs.atm_tran_refs[site])
            at.set_freq_range_Hz(freq_start*10**12, freq_end*10**12)  #set where in excel file to start/stop reading by converting input from THz to Hz
            
            tau = np.array(at.read_from_col(4), dtype='float')  #create array of transmission from 5th column of excel file, reading as floats
            print "Reading from Atmosphere Transmission. DONE"

            print "Calculating Total Signal.."
            start_time = time.time()  #begins clock for calculation time
            ts = cal.TS(freq, inte, tau, d, resol)  #returns array of total signal from inputs
            end_time = time.time()  #stops clock for calculation time
            print "Total Signal calculation DONE"
            print "Time used for Total Signal calculation: ", end_time - start_time, " seconds"
            freq_THz = freq * 10 ** (-12)  #create array that converts "freq" into THz


# plotting and writing file
# instead of having a plotter module, a plotting function is defined here so labels and titles are changeable
        def loglogplot(x, y):
            print "Start plotting..."
##            pos = np.where(np.abs(np.diff(y)) >= .0015)[0] + 1  #jumps over .0015 THz(1.5 GHz) are not connected
##            x = np.insert(x, pos, np.nan)  #replace values in "x" that correspond to nonpositives in "y" with "not a number"s
##            y = np.insert(y, pos, np.nan)  #replace nonpositives in "y" with "not a number"s
            pylab.plot(x, y)
            pylab.xscale('log')
            pylab.yscale('log')
            pylab.xlim(freq_start, freq_end)  #define x-axis range by inputs
            if self.dependent_limits_checkbox.IsChecked():  #if "Manually Input Range of Dependent Axis" box is checked, values must be input for following 2 boxes
                start_magnitude = float(self.parameter_inputs[6].GetValue())  #get order of magnitude for y-axis minumum
                dep_start = 10 ** start_magnitude  #turn order of magnitude into value of minimum
                end_magnitude = float(self.parameter_inputs[7].GetValue())  #get order of magnitude for y-axis maximum
                dep_end = 10 ** end_magnitude  #turn order of magnitude into value of maximum
                pylab.ylim(dep_start, dep_end)


#if "Total Noise" is checked
        if self.generate_checkboxs[0].IsChecked():
            # write file
            xw = ExcelXWriter(path)  #create xlsx file named after the input
            #each of the following adds a new column
            xw.write_col('freq(cm^-1)', freqNoise / (3 * 10**10))
            xw.write_col('freq(Hz)', freqNoise)
            xw.write_col('freq(THz)', freqNoise_THz)
            xw.write_col('wavelength(um)', (3 * 10**8) / freqNoise * 10**6) 
            xw.write_col('Total Noise_BLING(W Hz^(-1/2))', bling_TOT)

            # draw plot
            loglogplot(freqNoise_THz, bling_TOT)  #plot of BLING is log(base 10)-scaled
            pylab.ylabel("BLING(W*Hz^(-1/2))")
            pylab.xlabel("Frequency(THz)")
            title = "Noise" + str(title_bling) + " vs. Frequency at Spectral Resolution of " + str(resol) + ".\nFrequency is from " + str(freq_start) + " to " + str(freq_end) + "THz.  "
            if self.background_checkboxs[3].IsChecked() or self.background_checkboxs[6].IsChecked():  #if "Thermal Mirror Emission" is included, add "mirror_temp" to the title
                title = title + "Mirror has temperature " + str(mirror_temp) + "K.  "
            if self.background_checkboxs[4].IsChecked() or self.background_checkboxs[6].IsChecked():  #if "Atmospheric" is included, add the site to the title
                title = title + str(site) + " is the site."
            pylab.suptitle(title, fontsize=10)            
            pylab.show()


#if "Total Temperature" is checked
        if self.generate_checkboxs[1].IsChecked():
            # write file
            xw = ExcelXWriter(path)  #create xlsx file named after the input
            #each of the following adds a new column
            xw.write_col('freq(cm^-1)', freqNoise / (3 * 10**10))
            xw.write_col('freq(Hz)', freqNoise)
            xw.write_col('freq(THz)', freqNoise_THz)
            xw.write_col('wavelength(um)', (3 * 10**8) / freqNoise * 10**6) 
            xw.write_col('Total Temperature(K)', temperature)

            # draw plot
            loglogplot(freqNoise_THz, temperature)  #plot of Temperature is log(base 10)-scaled
            pylab.ylabel("Temperature(Kelvin)")
            pylab.xlabel("Frequency(THz)")
            title = "Temperature" + str(title_temp) + " vs. Frequency.\nFrequency is from " + str(freq_start) + " to " + str(freq_end) + "THz.  "
            if self.background_checkboxs[3].IsChecked() or self.background_checkboxs[6].IsChecked():  #if "Thermal Mirror Emission" is included, add "mirror_temp" to the title
                title = title + "Mirror has temperature " + str(mirror_temp) + "K.  "
            if self.background_checkboxs[4].IsChecked() or self.background_checkboxs[6].IsChecked():  #if "Atmospheric" is included, add the site to the title
                title = title + str(site) + " is the site."
            pylab.suptitle(title, fontsize=10)            
            pylab.show()


#if "Total Signal" is checked
        if self.generate_checkboxs[2].IsChecked():
            # draw plot
            loglogplot(freq_THz, ts)  #plot of signal is log(base 10)-scaled
            pylab.ylabel("Signal(W)")
            pylab.xlabel("Frequency(THz)")
            pylab.suptitle("Total Signal vs. Frequency at " + str(site) + " from " + str(source) + ".\nSpectral Resolution is " + str(resol) + " and frequency is from " + str(freq_start) + " to " + str(freq_end) + "THz.\nMirror has diameter " + str(d) + "m.", fontsize=10)
            pylab.show()

            # write file
            xw = ExcelXWriter(path)  #creates xlsx file with the name inputted
            #each of the following adds a new column
            xw.write_col('freq(cm^-1)', freq / (3 * 10**10))
            xw.write_col('freq(Hz)', freq)
            xw.write_col('freq(THz)', freq_THz)
            xw.write_col('wavelength(um)', (3 * 10**8) / freq * 10**6)
            xw.write_col('Total signal(W)', ts)


#if "Limiting Flux" is checked            
        if self.generate_checkboxs[3].IsChecked():
        #    xw.write_col('Limiting Flux(W)', limiting_flux)
            loglogplot(freq_THz, limiting_flux)


#if "Integration Time" is checked
        if self.generate_checkboxs[4].IsChecked():
            ratio = float(self.parameter_inputs[5].GetValue())  #only need signal to noise ratio input if "Integration Time" is checked

            # draw plot
            integration_time = cal.IT(bling_TOT, ratio, ts)  #returns array of integration time after signal and BLING are calculated
            loglogplot(freq_THz, integration_time)  #plot of integration time is log(base 10)-scaled
            pylab.ylabel("Integration Time(sec)")
            pylab.xlabel("Frequency(THz)")
            title = "Integration time vs. Frequency at " + str(site) + " from " + str(source) + ".\nSpectral Resolution is " + str(resol) + " and frequency is from " + str(freq_start) + " to " + str(freq_end) + "THz.\nSignal to Noise ratio is " + str(ratio) + " and mirror diameter is " + str(d) + "m."
            if self.background_checkboxs[3].IsChecked() or self.background_checkboxs[6].IsChecked():  #if "Thermal Mirror Emission" is included, add "mirror_temp" to the title
                title = title + "  Mirror has temperature " + str(mirror_temp) + "K."
            pylab.suptitle(title, fontsize=10)
            pylab.show()
            
            # write file
            xw = ExcelXWriter(path)  #creates xlsx file with the name inputted
            #each of the following adds a new column
            xw.write_col('freq(cm^-1)', freq / (3 * 10**10))
            xw.write_col('freq(Hz)', freq)
            xw.write_col('freq(THz)', freq_THz)
            xw.write_col('wavelength(um)', (3 * 10**8) / freq * 10**6)
            xw.write_col('Integration Time(s)', integration_time)
            
        # xw.save()
        print "Plotting. DONE"
        
       
        # message box alert
        message_dialog = wx.MessageDialog(self, message='Successfully Generated!')
        message_dialog.SetTitle("Successful!")
        if message_dialog.ShowModal() == wx.ID_OK:
            message_dialog.Destroy()

    def onCancel(self, e):
        self.Destroy()
        
if __name__ == '__main__':
  
    app = wx.App()
    atmodel(None, title='Atmosphere Modeling for Telescope')
    app.MainLoop()

