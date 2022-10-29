import kivy
from test import *
kivy.require('1.10.0')
 
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

class PortScan(App):
   
    # This returns the content we want in the window
    def build(self):
        self.layout = GridLayout(cols=2, row_force_default=True, row_default_height=40,
                            spacing=10, padding=20)
        self.ip_addr = TextInput(text='Enter IP address here')
        # Return a label widget with Hello Kivy
        # return Label(text ="{}".format(show_results(port_scan('192.168.2.1'))))
        button_port_scan = Button(text='Run port scan', on_press = self.run_port_scan) 
        self.layout.add_widget(self.ip_addr)
        self.layout.add_widget(button_port_scan)
        return self.layout
        # return text_input
    
    def run_port_scan(self, ip_addr):
        # port_scan(self.ip_addr.text)
        self.layout.add_widget(Label(text ="{}".format(show_results(port_scan(self.ip_addr.text)))))


   
portScan = PortScan()
portScan.run()