import kivy
from test import *
kivy.require('1.10.0')
 
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView


class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)
        
        self.cols = 2
        # self.row_force_default=True
        # self.row_default_height=40

        self.add_widget(Label(text='Enter IP address'))
        self.ip_addr = TextInput(multiline=False)
        self.add_widget(self.ip_addr)

        self.submit = Button(text='Run port scan', font_size=32)
        self.submit.bind(on_press=self.run_port_scan)
        self.add_widget(self.submit)

        self.submit = Button(text='Run os scan', font_size=32)
        self.submit.bind(on_press=self.run_os_scan)
        self.add_widget(self.submit)

        self.submit = Button(text='Run ICMP ping', font_size=32)
        self.submit.bind(on_press=self.run_icmp_ping)
        self.add_widget(self.submit)

        self.submit = Button(text='Run traceroute', font_size=32)
        self.submit.bind(on_press=self.run_traceroute)
        self.add_widget(self.submit)

        # self.scroll_view = ScrollView(scroll_type=['bars', 'content'], bar_width=10)
        self.scroll_view = ScrollView(scroll_type=['bars', 'content'], bar_width=10)
        self.output = Label(text='Output')
        self.scroll_view.add_widget(self.output)
        self.add_widget(self.scroll_view)

    def adjust_scroll(self, results, instance):
        self.output.text = results
        self.output.size_hint=(1, self.output.text.count('\n')/8)

    def run_port_scan(self, instance):
        print('Button has been pressed')
        port_scan_results = port_scan(self.ip_addr.text)
        results = show_results(port_scan_results)
        # self.add_widget(Label(text ="{}".format(results)))
        # self.output.text = results
        # self.output.size_hint=(1, self.output.text.count('\n')/10)
        self.adjust_scroll(results, instance)

    def run_os_scan(self, instance):
        print('Button has been pressed')
        os_scan_results = os_scan(self.ip_addr.text)
        results = show_results(os_scan_results)
        # self.add_widget(Label(text ="{}".format(results)))
        self.output.text = results
        self.adjust_scroll(results, instance)

    def run_icmp_ping(self, instance):
        print('Button has been pressed')
        results = icmp_ping(self.ip_addr.text)
        # self.add_widget(Label(text ="{}".format(results)))
        self.output.text = results
        self.adjust_scroll(results, instance)

    def run_traceroute(self, instance):
        print('Button has been pressed')
        results = tracert(self.ip_addr.text)
        # self.add_widget(Label(text ="{}".format(results)))
        self.output.text = results
        self.adjust_scroll(results, instance)

class PortScan(App):
   
    # This returns the content we want in the window
    def build(self):
        return MyGridLayout()
        
   
   
if __name__ == '__main__':
    PortScan().run()