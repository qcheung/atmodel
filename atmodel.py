import wx
from excel import ExcelXWriter,ExcelReader
import plotter
import cal
import const
import numpy as np
import file_refs
 
class atmodel(wx.Frame):
    def __init__(self, parent , title):
        super(atmodel, self).__init__(parent, title=title, size = (700, 500))
            
        self.InitUI()
        self.Centre()
        self.Show()     
        
    def InitUI(self):
        
        #Creating Panel 
        panel = wx.Panel(self)
        
        #Set panel font
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(14)
        
        #Create main container structures
        content = wx.BoxSizer(wx.VERTICAL)

        top = wx.BoxSizer(wx.HORIZONTAL)
        top_left = wx.BoxSizer(wx.VERTICAL)
        top_right = wx.BoxSizer(wx.VERTICAL)

        bottom = wx.BoxSizer(wx.HORIZONTAL)
        bottom_left = wx.BoxSizer(wx.VERTICAL)
        bottom_right = wx.BoxSizer(wx.VERTICAL)
        
        #Top_left
        top_left_fgs = wx.FlexGridSizer(7, 2, 6, 6) #declare FlexibleGridSizer
        
        #Top_left -> parameters
        parameters = ['Specify Parameters', 'Spectral Resolution:', 
                      'Mirror Diameter(m):', 'Mirror Temperature(K):',
                      'Choose a Site:', 'Choose a source:', 'Choose backgrounds', 
                      'Specify starting frequency(cm^-1)', 'Specify ending frequency(cm^-1)','Signal to noise ratio' ]
        sites = ['13_7Km SOFIA','30KmBalloon', '40KmBalloon', 'CCAT-0732g','CCAT-0978g','DomeA-01g','DomeA-014g','DomeC-015g',
                 'DomeC-024g','MaunaKea-1g','MaunaKea-15g','SantaBarbara-01g','SantaBarbara-30g','SouthPole-023g',
                 'SouthPole-032g','WhiteMountain-115g','WhiteMountain-175g','Space', 'Custom..']
        sources = ['NGC958_z=1', 'ARP220_z=1', 'MRK231_z=1', 'Custom..']
        backgrounds = ['Cosmic Infrared Background', 'Cosmic Microwave Background', 'Galactic Emission', 'Thermal Mirror Emission', 
                       'Atmospheric Radiance', 'Zodiacal Emission']
        
        #Top_left -> Controls
        parameter_labels = [wx.StaticText(panel, label = parameters[i]) for i in range(10)]
        self.parameter_inputs = [wx.TextCtrl(panel) for i in range(6)]
        self.parameter_site_combo = wx.ComboBox(panel, choices = sites, style = wx.CB_READONLY) 
        self.parameter_source_combo = wx.ComboBox(panel, choices = sources, style = wx.CB_READONLY)
        
        #Top_left -> fill up contains 
        parameter_labels[0].SetFont(font)   #set a title font
        top_left_fgs.Add(parameter_labels[0], flag = wx.EXPAND | wx.BOTTOM, border = 6)
        top_left_fgs.Add(wx.StaticText(panel), flag = wx.EXPAND)    #empty grid
        top_left_fgs.AddMany([(parameter_labels[1], 0, wx.EXPAND), (self.parameter_inputs[0], 0, wx.EXPAND),
                              (parameter_labels[2], 0, wx.EXPAND), (self.parameter_inputs[1], 0, wx.EXPAND),
                              (parameter_labels[3], 0, wx.EXPAND), (self.parameter_inputs[2], 0, wx.EXPAND),
                              (parameter_labels[4], 0, wx.EXPAND), (self.parameter_site_combo, 0, wx.EXPAND),
                              (parameter_labels[5], 0, wx.EXPAND), (self.parameter_source_combo, 0, wx.EXPAND),
                              (parameter_labels[7], 0, wx.EXPAND), (self.parameter_inputs[3], 0, wx.EXPAND),
                              (parameter_labels[8], 0, wx.EXPAND), (self.parameter_inputs[4], 0, wx.EXPAND),
                              (parameter_labels[9], 0, wx.EXPAND), (self.parameter_inputs[5], 0, wx.EXPAND)])
                                #each row represents a row in interface
        top_left.Add(top_left_fgs, flag = wx.EXPAND)

        #Top_right
        galactic_directions = ['g_long = 0, g_lat = 0', 'g_long = 0, g_lat = 45','g_long = 0, g_lat = +90','g_long = 0, g_lat = -90',
                               'g_long = 180, g_lat = 90']
        zodiacal_directions = ['g_long = 0, g_lat = 0','g_long = 0, g_lat = 45','g_long = 180, g_lat = 90']
        thermal_mirror_materials = ['Be', 'Al', 'Au', 'Ag']
        
        #Top_right -> controls
        self.background_checkboxs =[wx.CheckBox(panel,label = backgrounds[i]) for i in range(len(backgrounds))]
        self.galactic_direction_combo = wx.ComboBox(panel, choices = galactic_directions, style = wx.CB_READONLY) 
        self.zodiacal_direction_combo = wx.ComboBox(panel, choices = zodiacal_directions, style = wx.CB_READONLY)
        self.thermal_mirror_material_combo = wx.ComboBox(panel, choices = thermal_mirror_materials, style = wx.CB_READONLY)
        
        #Top_right -> fill up contents
        top_right.Add(parameter_labels[6], flag = wx.BOTTOM, border = 6)
        top_right.Add(self.background_checkboxs[0], flag = wx.BOTTOM, border = 3)
        top_right.Add(self.background_checkboxs[1], flag = wx.BOTTOM, border = 3)
        top_right.Add(self.background_checkboxs[2], flag = wx.BOTTOM, border = 3)
        top_right.Add(self.galactic_direction_combo, flag = wx.LEFT, border = 20)
        top_right.Add(self.background_checkboxs[3], flag = wx.BOTTOM | wx.TOP, border = 3)
        top_right.Add(self.thermal_mirror_material_combo, flag = wx.LEFT, border = 20)
        top_right.Add(self.background_checkboxs[4], flag = wx.BOTTOM | wx.TOP, border = 3)
        top_right.Add(self.background_checkboxs[5], flag = wx.BOTTOM, border = 3)
        top_right.Add(self.zodiacal_direction_combo, flag = wx.LEFT, border = 20)
        

        #Bottom_left 
        #Bottom_left -> Controls
        generate_label = wx.StaticText(panel, label = 'Generates:')
        generate_label.SetFont(font) #Title

        generates = ['Total Noise', 'Total Signal', 'Limiting Flux', 'Integration time'] 
        self.generate_checkboxs = [wx.CheckBox(panel, label = generates[i]) for i in range(len(generates))]

        #Bottom_left -> Fill up contents
        bottom_left.Add(generate_label, flag = wx.BOTTOM, border = 10)
        for i in range(len(generates)):
            bottom_left.Add(self.generate_checkboxs[i], flag = wx.BOTTOM, border = 3)

        #Bottom_right
        #Bottom_right -> Output -> Controls
        output_sizer = wx.BoxSizer(wx.HORIZONTAL)
        output_label = wx.StaticText(panel, label = 'Output to:')
        self.output_input = wx.TextCtrl(panel, size = (200,30))
        output_button = wx.Button(panel, size = (80,30), label = 'Browse')
	
        #Bottom_right -> Output -> Fill up contents
        bottom_right.Add(output_label, flag = wx.TOP, border = 20)
        output_sizer.Add(self.output_input, flag = wx.EXPAND)
        output_sizer.Add(output_button)
        bottom_right.Add(output_sizer, flag = wx.BOTTOM, border = 8)

        #Bottom_right -> Buttons
        generate_button = wx.Button(panel, label = 'Generate')
        cancel_button = wx.Button(panel, label = 'Cancel')
        
        #Bottom_right -> Buttons -> Fill up
        bottom_right.Add(generate_button, flag = wx.EXPAND | wx.BOTTOM, border = 3)
        bottom_right.Add(cancel_button, flag = wx.EXPAND)
	
        #Bottom_right -> Function Bindings
        output_button.Bind(wx.EVT_BUTTON, self.onBrowse)
        generate_button.Bind(wx.EVT_BUTTON, self.onGenerate)
        cancel_button.Bind(wx.EVT_BUTTON, self.onCancel)
        
        #Fill up contents
        top.Add(top_left, flag = wx.RIGHT | wx.BOTTOM, border = 25)
        top.Add(top_right, flag = wx.TOP | wx.BOTTOM, border = 25)
        bottom.Add(bottom_left, flag = wx.RIGHT, border = 35)
        bottom.Add(bottom_right, flag = wx.LEFT, border = 35)
        content.Add(top, flag = wx.TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM, border = 10)
        content.Add(bottom, flag = wx.TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM, border = 10)
        panel.SetSizer(content)
        
           
    def onBrowse(self, e):
        file_dialog = wx.FileDialog(self, style = wx.FD_SAVE)
        if file_dialog.ShowModal() == wx.ID_OK:
            self.path = file_dialog.GetPath()
            self.output_input.Clear()
            self.output_input.WriteText(self.path)  
        file_dialog.Destroy()        
        
    def onGenerate(self, e):
        
        #initialization
        
        #initialization -> Parse inputs
        resol = float(self.parameter_inputs[0].GetValue()) 	#resolution
        d = float(self.parameter_inputs[1].GetValue())		#mirror diameters
        mirror_temp = float(self.parameter_inputs[2].GetValue()) 		#mirror temperature
        freq_start = float(self.parameter_inputs[3].GetValue())	#starting frequency
        freq_end = float(self.parameter_inputs[4].GetValue())	#ending frequency
        ratio = float(self.parameter_inputs[5].GetValue())	#signal to noise ratio
        path = self.output_input.GetValue()
        site = self.parameter_site_combo.GetValue()
        source = self.parameter_source_combo.GetValue()
        
        #Calculate bling   
        bling = 0
        
        #CIB
        if self.background_checkboxs[0].IsChecked():
            cib_excel = file_refs.CIB_ref
            cib = ExcelReader(cib_excel)
            cib.set_freq_range(freq_start, freq_end)
            freq = cib.read_from_col(1)
            temp = cib.read_from_col(4)
            bling += cal.bling_sub(freq, temp, resol)
            
        
        #CMB
        if self.background_checkboxs[1].IsChecked():
            cmb_excel = file_refs.CMB_ref
            cmb = ExcelReader(cmb_excel)
            cmb.set_freq_range(freq_start, freq_end)
            freq = cmb.read_from_col(1)
            bling += cal.bling_CMB(freq, resol)
        
        #Galactic Emission    
        if self.background_checkboxs[2].IsChecked():
            index = self.galactic_direction_combo.GetCurrentSelection()
            ge = ExcelReader(file_refs.Galatic_Emission_refs[index])
            ge.set_freq_range(freq_start, freq_end)
            freq = ge.read_from_col(1)
            temp = ge.read_from_col(8)
            bling += cal.bling_sub(freq, temp, resol)
            
        
        #Thermal Mirror Emission    
        if self.background_checkboxs[3].IsChecked():
            index = self.thermal_mirror_material_combo.GetCurrentSelection()
            tme = ExcelReader(file_refs.TME_ref)
            tme.set_freq_range(freq_start, freq_end)
            freq = tme.read_from_col(1)
            sigma = const.sigma[index]
            bling += cal.bling_TME(freq, resol, sigma, mirror_temp)
        
        #Atmospheric Radiance
        if self.background_checkboxs[4].IsChecked(): 
            ar = ExcelReader(file_refs.atm_rad_refs[site])
            ar.set_freq_range(freq_start, freq_end)
            freq = ar.read_from_col(1)
            rad = ar.read_from_col(4)
            bling += cal.bling_AR(freq, rad, resol)
        
        #Zodiacal Emission
        if self.background_checkboxs[5].IsChecked():
            index = self.zodiacal_direction_combo.GetCurrentSelection()
            ze = ExcelReader(file_refs.ZODI_refs[index])
            ze.set_freq_range(freq_start, freq_end)
            freq = ze.read_from_col(1)
            temp = ze.read_from_col(4)
            bling += cal.bling_sub(freq, temp, resol)
        
        bling_TOT = bling ** 0.5
        
        #Source Intensity
        si = ExcelReader(file_refs.source_refs[source])
        si.set_freq_range(freq_start, freq_end)
        freq = si.read_from_col(1)
        inte = si.read_from_col(5)
        
        #Source_Total Signal
        at = ExcelReader(file_refs.atm_tran_refs[site])
        at.set_freq_range(freq_start, freq_end)
        tau = at.read_from_col(4)
        ts = cal.TS(freq, inte, tau, d, resol)
        
        #Limiting Flux
        limiting_flux = cal.LF(freq, d, resol, ts)
        
        #Integration Time
        integration_time = cal.IT(freq, bling_TOT, ratio, ts)
        
        
        #writing
        freq = np.array(freq)
        #xw = ExcelXWriter(path)
        #xw.write_col('freq(cm^-1)', freq / (3 * 10**10))
        #xw.write_col('freq(Hz)', freq)
        freq_THz = freq*10**(-12)
        #xw.write_col('freq(THz)', freq_THz)
        #xw.write_col('wavelength(um)', (3 * 10**8) / freq * 10**6)
         
        #plot
        if self.generate_checkboxs[0].IsChecked():
            #xw.write_col('Total Noise_BLING(W Hz^(-1/2))', bling_TOT)
            plotter.loglogplot(freq_THz, bling_TOT)
        if self.generate_checkboxs[1].IsChecked():
            #xw.write_col('Total signal(W/m^2/sr/Hz)', ts)
            plotter.loglogplot(freq_THz, ts)
        if self.generate_checkboxs[2].IsChecked():
            #xw.write_col('Limiting Flux(W)', limiting_flux)
            plotter.loglogplot(freq_THz, limiting_flux)
        if self.generate_checkboxs[3].IsChecked():
            #xw.write_col('Integration Time(s)', integration_time)
            plotter.loglogplot(freq_THz, integration_time)
        #xw.save()
        
        
       
        #message box alert
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
