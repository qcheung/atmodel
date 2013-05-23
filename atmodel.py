import wx
from excel import ExcelWriter,ExcelReader
import plotter
import cal
 
class atmodel(wx.Frame):
    output_input = 0
    def __init__(self, parent , title):
        super(atmodel, self).__init__(parent, title=title, size = (650, 500))
            
        self.InitUI()
        self.Centre()
        self.Show()     
        
    def InitUI(self):

        'Panel' 
        panel = wx.Panel(self)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(14)
        content = wx.BoxSizer(wx.VERTICAL)
        
        'TOP'
        top = wx.BoxSizer(wx.HORIZONTAL)
        top_left = wx.BoxSizer(wx.VERTICAL)
        top_right = wx.BoxSizer(wx.VERTICAL)
        
        'TOP_LEFT'
        top_left_fgs = wx.FlexGridSizer(7, 2, 6, 6)
        parameters = ['Specify Parameters', 'Spectral Resolution:', 
                      'Mirror Diameter(m):', 'Mirror Temperature(K):',
                      'Choose a Site:', 'Choose a source:', 'Choose backgrounds', 
                      'Specify starting frequency(cm^-1)', 'Specify ending frequency(cm^-1)','Signal to noise ratio' ]
        sites = ['South Pole', 'DomeA', 'DomeC', 'WhiteMo','Santa Barbara',
                  'Chili', 'Sofia', 'Balloon 30', 'Balloon 40', 'Space', 'Custom..']
        sources = ['SED', 'ARP220', 'NGC 958', 'Custom..']
        backgrounds = ['Cosmic Infrared Background', 'Cosmic Microwave Background', 'Galaxtic Emission', 'Thermal Mirror Emission', 
                       'Atmospheric Radiance', 
                       'Zodiacal Emission']

        parameter_labels = [wx.StaticText(panel, label = parameters[i]) for i in range(10)]
        self.parameter_inputs = [wx.TextCtrl(panel) for i in range(6)]
        parameter_site_combo = wx.ComboBox(panel, choices = sites, style = wx.CB_READONLY) 
        parameter_source_combo = wx.ComboBox(panel, choices = sources, style = wx.CB_READONLY)

        parameter_labels[0].SetFont(font)
        top_left_fgs.Add(parameter_labels[0], flag = wx.EXPAND | wx.BOTTOM, border = 6)
        top_left_fgs.Add(wx.StaticText(panel), flag = wx.EXPAND)
        top_left_fgs.AddMany([(parameter_labels[1], 0, wx.EXPAND), (self.parameter_inputs[0], 0, wx.EXPAND),
                              (parameter_labels[2], 0, wx.EXPAND), (self.parameter_inputs[1], 0, wx.EXPAND),
                              (parameter_labels[3], 0, wx.EXPAND), (self.parameter_inputs[2], 0, wx.EXPAND),
                              (parameter_labels[4], 0, wx.EXPAND), (parameter_site_combo, 0, wx.EXPAND),
                              (parameter_labels[5], 0, wx.EXPAND), (parameter_source_combo, 0, wx.EXPAND),
                              (parameter_labels[7], 0, wx.EXPAND), (self.parameter_inputs[3], 0, wx.EXPAND),
                              (parameter_labels[8], 0, wx.EXPAND), (self.parameter_inputs[4], 0, wx.EXPAND),
                              (parameter_labels[9], 0, wx.EXPAND), (self.parameter_inputs[5], 0, wx.EXPAND)])
        
        top_left.Add(top_left_fgs, flag = wx.EXPAND)

        'TOP_RIGHT'
        top_right.Add(parameter_labels[6], flag = wx.BOTTOM, border = 6)
        background_checkboxs =[wx.CheckBox(panel,label = backgrounds[i]) for i in range(len(backgrounds))]
        for i in range(len(backgrounds)):
            top_right.Add(background_checkboxs[i], flag = wx.BOTTOM, border = 3)
        
        'BOTTOM'
        bottom = wx.BoxSizer(wx.HORIZONTAL)
        bottom_left = wx.BoxSizer(wx.VERTICAL)
        bottom_right = wx.BoxSizer(wx.VERTICAL)
        
        'BOTTOM_LEFT'
        generate_label = wx.StaticText(panel, label = 'Generates:')
        generate_label.SetFont(font)
        bottom_left.Add(generate_label, flag = wx.BOTTOM, border = 10)

        generates = ['Total Noise', 'Total Signal', 'Limiting Flux', 'Integration time'] 
        generate_checkboxs = [wx.CheckBox(panel, label = generates[i]) for i in range(len(generates))]
        for i in range(len(generates)):
            bottom_left.Add(generate_checkboxs[i], flag = wx.BOTTOM, border = 3)

        'BOTTOM_RIGHT'
        output_sizer = wx.BoxSizer(wx.HORIZONTAL)
        output_label = wx.StaticText(panel, label = 'Output to:')
        self.output_input = wx.TextCtrl(panel, size = (200,30))
        output_button = wx.Button(panel, size = (80,30), label = 'Browse')
        output_button.Bind(wx.EVT_BUTTON, self.onBrowse)

        bottom_right.Add(output_label, flag = wx.TOP, border = 20)
        output_sizer.Add(self.output_input, flag = wx.EXPAND)
        output_sizer.Add(output_button)
        
        bottom_right.Add(output_sizer, flag = wx.BOTTOM, border = 8)

        generate_button = wx.Button(panel, label = 'Generate')
        generate_button.Bind(wx.EVT_BUTTON, self.onGenerate)
        '''
        plot_button = wx.Button(panel, label = 'Plot')
        plot_button.Bind(wx.EVT_BUTTON, self.onPlot)
        '''
        cancel_button = wx.Button(panel, label = 'Cancel')
        cancel_button.Bind(wx.EVT_BUTTON, self.onCancel)
        
        bottom_right.Add(generate_button, flag = wx.EXPAND | wx.BOTTOM, border = 3)
        '''
        bottom_right.Add(plot_button, flag = wx.EXPAND)
        '''
        bottom_right.Add(cancel_button, flag = wx.EXPAND)
        
        'Finishing'
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
        xw = ExcelWriter(self.path)
        xr = ExcelReader("/home/dave/test.xlsx")
        
        #get values
        freq_start = float(self.parameter_inputs[3].GetValue())
        freq_end = float(self.parameter_inputs[4].GetValue())
        resol = float(self.parameter_inputs[0].GetValue())
        
        #set frequency range
        xr.set_freq_range(freq_start, freq_end)
        
        #read frequency and temperature
        freq = xr.read_from_col(2)
        temp = xr.read_from_col(8)
        
        #Calculation

        bling = cal.bling_Galactic_Emission(freq, temp, resol)
        
        #writing
        xw.write_col('freq/THz', freq)
        xw.write_col('Bling', bling)
        xw.save()
        message_dialog = wx.MessageDialog(self, message='Successfully Generated!')
        message_dialog.SetTitle("Successful!")
        if message_dialog.ShowModal() == wx.ID_OK:
            message_dialog.Destroy()
        plotter.loglogplot(freq, bling)
    def onCancel(self, e):
        self.Destroy()
    '''
    def onPlot(self, e):
        xr = ExcelReader("/home/dave/test.xlsx")
        freq_start = float(self.parameter_inputs[3].GetValue())
        freq_end = float(self.parameter_inputs[4].GetValue())
        xr.set_freq_range(freq_start, freq_end)
        x = xr.read_from_col(2)
        y = xr.read_from_col(8)
        
        
    '''
if __name__ == '__main__':
  
    app = wx.App()
    atmodel(None, title='Atmosphere Modeling for Telescope')
    app.MainLoop()
