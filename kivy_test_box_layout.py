from threading import main_thread
import kivy
from test import *
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from fpdf import FPDF
from datetime import datetime
# from functool import partial


class MyLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)

        self.orientation = "vertical"
        self.spacing = 20
        # self.padding = 50
        self.current_clicked_fun = None

        self.add_widget(Label(text='Enter IP address', size_hint=(1, 0.2)))
        self.ip_addr = TextInput(multiline=False, size_hint=(1, 0.2))
        self.add_widget(self.ip_addr)

        self.submit = Button(text='Run port scan', font_size=32, size_hint=(0.8, 0.3), pos_hint={'center_x': 0.5})
        buttoncallback = lambda *args:self.change_label(fun=self.run_port_scan, *args)
        self.submit.bind(on_press=buttoncallback)
        self.add_widget(self.submit)

        self.submit = Button(text='Run os scan', font_size=32, size_hint=(0.8, 0.3), pos_hint={'center_x': 0.5})
        buttoncallback = lambda *args:self.change_label(fun=self.run_os_scan, *args)
        self.submit.bind(on_press=buttoncallback)
        self.add_widget(self.submit)

        self.submit = Button(text='Run ICMP ping', font_size=32, size_hint=(0.8, 0.3), pos_hint={'center_x': 0.5})
        buttoncallback = lambda *args:self.change_label(fun=self.run_icmp_ping, *args)
        self.submit.bind(on_press=buttoncallback)
        self.add_widget(self.submit)

        self.submit = Button(text='Run traceroute', font_size=32, size_hint=(0.8, 0.3), pos_hint={'center_x': 0.5})
        buttoncallback = lambda *args:self.change_label(fun=self.run_traceroute, *args)
        self.submit.bind(on_press=buttoncallback)
        self.add_widget(self.submit)

        self.submit = Button(text='Create PDF report', font_size=32, size_hint=(0.8, 0.3), pos_hint={'center_x': 0.5})
        buttoncallback = lambda *args:self.change_label(fun=self.create_pdf_report, *args)
        self.submit.bind(on_press=buttoncallback)
        self.add_widget(self.submit)

        # self.scroll_view = ScrollView(scroll_type=['bars', 'content'], bar_width=10)
        self.scroll_view = ScrollView(scroll_type=['bars', 'content'], bar_width=10)
        self.output = Label(text='Output', size_hint=(1, None), halign='center')
        self.scroll_view.add_widget(self.output)
        self.add_widget(self.scroll_view)

    def adjust_scroll(self, results, instance):
        self.output.text = results
        self.output.size_hint=(1, self.output.text.count('\n')/8)

    def run_port_scan(self, instance):
        print('Button has been pressed')
        port_scan_results = port_scan(self.ip_addr.text)
        results = show_results(port_scan_results)
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

    def change_label(self, instance,  fun):
        self.scroll_view.remove_widget(self.output)
        self.output = Label(text='Loading ...', size_hint=(1, 1))
        self.scroll_view.add_widget(self.output)
        # self.output.text=(1, 1)
        # self.output.text = 'Loading ...'
        threading.Thread(target=self.updating_gui(fun)).start()

    def updating_gui(self, fun):
        print('Starting GUI update')
        time.sleep(2)
        print('Finished GUI update')
        # Clock.schedule_once(self.create_pdf_report)
        Clock.schedule_once(fun)

    def create_pdf_report(self, instance):
        #self.change_label('Loading ...', instance)
        print('Button has been pressed')

        pdf = FPDF()
        pdf.add_page()
        
        results = icmp_ping(self.ip_addr.text)

        pdf.set_font('Arial', 'B', 18)
        pdf.cell(0, 10, 'Hosts responding to ICMP Ping', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, results, 0, 'J')

        port_scan_results = port_scan(self.ip_addr.text)
        results = show_results(port_scan_results)
        print(results)
        
        pdf.set_font('Arial', 'B', 18)
        pdf.cell(0, 10, 'Port Scan', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, results, 0, 'J')

        os_scan_results = os_scan(self.ip_addr.text)
        results = show_results(os_scan_results)
        print(results)

        pdf.set_font('Arial', 'B', 18)
        pdf.cell(0, 10, 'Operating System Scan', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, results, 0, 'J')

        now = datetime.now()
        now_formated = now.strftime("%d-%m-%Y-%H%M%S")
        pdf.output('report-{}.pdf'.format(now_formated), 'F')

        self.output.text = 'Done'

class PortScan(App):
   
    # This returns the content we want in the window
    def build(self):
        return MyLayout()
        
   
   
if __name__ == '__main__':
    PortScan().run()