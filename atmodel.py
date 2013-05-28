import wx
from excel import ExcelWriter,ExcelReader
import plotter
import cal
import const
 
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
        sites = ['Balloon 30', 'Balloon 40', 'CCAT-0732g','CCAT-0978g','DomeA-01g','DomeA-014g','DomeC-015g',
                 'DomeC-024g','MaunaKea-1g','MaunaKea-15g','SantaBarbara-01g','SantaBarbara-30g','SOFIA','SouthPole-023g',
                 'SouthPole-032g','WhiteMountain-115g','WhiteMountain-175g','Space', 'Custom..']
        sources = ['SED', 'ARP220', 'NGC 958', 'Custom..']
        backgrounds = ['Cosmic Infrared Background', 'Cosmic Microwave Background', 'Galactic Emission', 'Thermal Mirror Emission', 
                       'Atmospheric Radiance', 'Zodiacal Emission']
        
        #Top_left -> Controls
        parameter_labels = [wx.StaticText(panel, label = parameters[i]) for i in range(10)]
        self.parameter_inputs = [wx.TextCtrl(panel) for i in range(6)]
        parameter_site_combo = wx.ComboBox(panel, choices = sites, style = wx.CB_READONLY) 
        parameter_source_combo = wx.ComboBox(panel, choices = sources, style = wx.CB_READONLY)
        
        #Top_left -> fill up contains 
        parameter_labels[0].SetFont(font)   #set a title font
        top_left_fgs.Add(parameter_labels[0], flag = wx.EXPAND | wx.BOTTOM, border = 6)
        top_left_fgs.Add(wx.StaticText(panel), flag = wx.EXPAND)    #empty grid
        top_left_fgs.AddMany([(parameter_labels[1], 0, wx.EXPAND), (self.parameter_inputs[0], 0, wx.EXPAND),
                              (parameter_labels[2], 0, wx.EXPAND), (self.parameter_inputs[1], 0, wx.EXPAND),
                              (parameter_labels[3], 0, wx.EXPAND), (self.parameter_inputs[2], 0, wx.EXPAND),
                              (parameter_labels[4], 0, wx.EXPAND), (parameter_site_combo, 0, wx.EXPAND),
                              (parameter_labels[5], 0, wx.EXPAND), (parameter_source_combo, 0, wx.EXPAND),
                              (parameter_labels[7], 0, wx.EXPAND), (self.parameter_inputs[3], 0, wx.EXPAND),
                              (parameter_labels[8], 0, wx.EXPAND), (self.parameter_inputs[4], 0, wx.EXPAND),
                              (parameter_labels[9], 0, wx.EXPAND), (self.parameter_inputs[5], 0, wx.EXPAND)])
                                #each row represents a row in interface
        top_left.Add(top_left_fgs, flag = wx.EXPAND)

        #Top_right
        galactic_directions = ['g_long = 0, g_lat = 0', 'g_long = 0, g_lat = 45','g_long = 0, g_lat = +90','g_long = 0, g_lat = -90',
                               'g_long = 180, g_lat = 90']
        zodiacal_directions = ['g_long = 0, g_lat = 90','g_long = 0, g_lat = 45','g_long = 0, g_lat = 0']
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
        generate_checkboxs = [wx.CheckBox(panel, label = generates[i]) for i in range(len(generates))]

	#Bottom_left -> Fill up contents
        bottom_left.Add(generate_label, flag = wx.BOTTOM, border = 10)
        for i in range(len(generates)):
            bottom_left.Add(generate_checkboxs[i], flag = wx.BOTTOM, border = 3)

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
        top.Add(self.top_right, flag = wx.TOP | wx.BOTTOM, border = 25)
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
        t = float(self.parameter_inputs[2].GetValue()) 		#mirror temperature
        freq_start = float(self.parameter_inputs[3].GetValue())	#starting frequency
        freq_end = float(self.parameter_inputs[4].GetValue())	#ending frequency
        ratio = float(self.parameter_inputs[5].GetValue())	#signal to noise ratio
        
	#Calculate bling
        bling = 0

        if self.background_checkboxs[0].IsChecked():
            cib = ExcelReader("/home/dave/Cosmology_Infrared_Background.xlsx")
            cib.set_freq_range(freq_start, freq_end)
            freq = cib.read_from_col(1)
            temp = cib.read_from_col(8)
            bling += cal.bling_CIB(freq, temp, resol)
            
        if self.background_checkboxs[1].IsChecked():
            cmb = ExcelReader("/home/dave/Cosmology_Microwave_Background.xlsx")
            cmb.set_freq_range(freq_start, freq_end)
            bling += cal.bling_CMB(freq, resol)
            
        if self.background_checkboxs[2].IsChecked():
            index = self.galactic_direction_combo.GetCurrentSelection()
            ge = ExcelReader("/home/dave/Galactic_Emission.xlsx")
            ge.set_freq_range(freq_start, freq_end)
            freq = ge.read_from_col(1)
            if index == 0:
                temp = ge.read_from_col(8)
            if index == 4:
                temp = ge.read_from_col(13)
            bling += cal.bling_GE(freq, temp, resol)
            
        if self.background_checkboxs[3].IsChecked():
            index = self.thermal_mirror_material_combo.GetCurrentSelection()
            sigma = const.sigma[index]
            bling += cal.bling_TME(freq, resol, sigma, t)

        if self.background_checkboxs[4].IsChecked(): 
            index = self.site.GetCurrentSelection()
            ar = ExcelReader(file_sites[index])
            ar.set_freq_range(freq_start, freq_end)
            freq = ar.read_from_col(1)
            rad = ar.read_from_col(4)
            bling += cal.bling_AR(freq, rad, resol)
            
        if self.background_checkboxs[5].IsChecked():
            index = self.zodiacal_direction_combo.GetCurrentSelection()
            ze = ExcelReader("file_zodiacal[index]")
            ze.set_freq_range(freq_start, freq_end)
            freq = ze.read_from_col(1)
            temp = ze.read_from_col(8)
            bling += cal.bling_ZE(freq, temp, resol)

        bling_TOT = bling**(0.5)
            
        #writing
        xw.write_col('freq/THz', freq)
        xw.write_col('Bling', bling_TOT)
        xw.save()
        
        #message box alert
        message_dialog = wx.MessageDialog(self, message='Successfully Generated!')
        message_dialog.SetTitle("Successful!")
        if message_dialog.ShowModal() == wx.ID_OK:
            message_dialog.Destroy()
        
        #plot
        plotter.loglogplot(freq, bling_TOT)

    def onCancel(self, e):
        self.Destroy()
        
    def onBg_Galatic_Emission(self, e):
        source = e.GetEventObject()
        
        if source.IsChecked():
            test = wx.StaticText(self.panel, label = "test")
            self.top_right.Insert(0, test, flag = wx.EXPAND)
            self.top_right.Layout()
        else:
            test.Destroy()
            self.top_right.Layout()
     

if __name__ == '__main__':
  
    app = wx.App()
    atmodel(None, title='Atmosphere Modeling for Telescope')
    app.MainLoop()
