from threading import main_thread
import kivy
from functions import *
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
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
import ipaddress

# from functool import partial


class MyLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)

        self.orientation = "horizontal"
        self.spacing = 20
        # self.padding = 50
        self.current_clicked_fun = None

        self.popup_validate_ip = Popup(title='Validation of IP address', content=Label(text='Wrong IP address'), size_hint=(0.5, 0.5))
        self.popup_validate_port_range = Popup(title='Validation of Port range', content=Label(text='Wrong port range'), size_hint=(0.5, 0.5))

        # horizontal_box = BoxLayout(orientation='horizontal')
        vertical_box = BoxLayout(orientation='vertical', spacing=20)

        vertical_box.add_widget(Label(text='Enter IP address', size_hint=(1, 0.2)))
        self.ip_addr = TextInput(multiline=False, size_hint=(1, 0.2))
        vertical_box.add_widget(self.ip_addr)

        vertical_box.add_widget(Label(text='Enter port range for port scan, eg. "100-200"', size_hint=(1, 0.2)))
        self.port_range = TextInput(multiline=False, size_hint=(1, 0.2))
        vertical_box.add_widget(self.port_range)

        self.submit = Button(text='Run port scan', font_size=32, size_hint=(1, 0.3))
        buttoncallback = lambda *args:self.change_label(fun=self.run_port_scan, *args)
        self.submit.bind(on_press=buttoncallback)
        vertical_box.add_widget(self.submit)

        self.submit = Button(text='Run os scan', font_size=32, size_hint=(1, 0.3))
        buttoncallback = lambda *args:self.change_label(fun=self.run_os_scan, *args)
        self.submit.bind(on_press=buttoncallback)
        vertical_box.add_widget(self.submit)

        self.submit = Button(text='Run ICMP ping', font_size=32, size_hint=(1, 0.3))
        buttoncallback = lambda *args:self.change_label(fun=self.run_icmp_ping, *args)
        self.submit.bind(on_press=buttoncallback)
        vertical_box.add_widget(self.submit)

        self.submit = Button(text='Run traceroute', font_size=32, size_hint=(1, 0.3))
        buttoncallback = lambda *args:self.change_label(fun=self.run_traceroute, *args)
        self.submit.bind(on_press=buttoncallback)
        vertical_box.add_widget(self.submit)

        self.submit = Button(text='Create PDF report', font_size=32, size_hint=(1, 0.3))
        buttoncallback = lambda *args:self.change_label(fun=self.create_pdf_report, *args)
        self.submit.bind(on_press=buttoncallback)
        vertical_box.add_widget(self.submit)

        self.add_widget(vertical_box)

        self.scroll_view = ScrollView(scroll_type=['bars', 'content'], bar_width=10)
        self.output = Label(text='Output', size_hint=(1, None), halign='center')
        self.scroll_view.add_widget(self.output)
        self.add_widget(self.scroll_view)
        

    def stop_running_fun(self):
        self.stop = threading.Event()
        self.stop.set()
        self.output.text = 'Function canceled'

    def validate_ip_address(self):
        try:
            ip_addr = self.ip_addr.text.split('/')
            ip_addr_without_mask = ip_addr[0]
            if len(ip_addr) == 2 and not (int(ip_addr[1]) >= 8 and int(ip_addr[1]) <= 32):
                raise ValueError
            ip = ipaddress.ip_address(ip_addr_without_mask)
            print("IP address {} is valid. The object returned is {}".format(ip_addr_without_mask, ip))
            return True
        except ValueError:
            print("IP address {} is not valid".format(ip_addr_without_mask))
            self.popup_validate_ip.open()
            return False

    def validate_port_range(self):
        try:
            port_r = self.port_range.text.split('-')
            if int(port_r[0]) >= int(port_r[1]):
                raise ValueError
            return True
            
        except ValueError:
            print("Port range {} is not valid".format(port_r))
            self.popup_validate_port_range.open()
            return False

    def adjust_scroll(self, results):
        self.output.text = results
        self.output.size_hint=(1, self.output.text.count('\n')/11)

    def run_port_scan(self):
        print('Button has been pressed')
        port_scan_results = port_scan(self.ip_addr.text, self.port_range.text)
        results = show_results(port_scan_results)
        self.adjust_scroll(results)

    def run_os_scan(self):
        print('Button has been pressed')
        os_scan_results = os_scan(self.ip_addr.text)
        results = show_results(os_scan_results)
        self.output.text = results
        self.adjust_scroll(results)

    def run_icmp_ping(self):
        print('Button has been pressed')
        results = icmp_ping(self.ip_addr.text)
        self.output.text = results
        self.adjust_scroll(results)

    def run_traceroute(self):
        print('Button has been pressed')
        results = tracert(self.ip_addr.text)
        self.output.text = results
        print(results)
        self.adjust_scroll(results)

    def change_label(self, instance,  fun):
        if self.validate_ip_address() == True and self.validate_port_range() == True:
            self.scroll_view.remove_widget(self.output)
            self.output = Label(text='Loading ...', size_hint=(1, 1))
            self.scroll_view.add_widget(self.output)
            threading.Thread(target=self.updating_gui(fun)).start()

    def updating_gui(self, fun):
        print('Starting GUI update')
        print('Finished GUI update')
        self.thread = threading.Thread(target=fun)
        self.thread.start()

    def create_pdf_report(self):
        print('Button has been pressed')

        pdf = FPDF()
        pdf.add_page()

        start_time = datetime.now()
        
        start_time_formatted = start_time.strftime("%d-%m-%Y %H:%M:%S")

        results_icmp_ping = icmp_ping(self.ip_addr.text)

        results_traceroute = tracert(self.ip_addr.text)

        port_scan_results = port_scan(self.ip_addr.text, self.port_range.text)
        results_port_scan = show_results(port_scan_results)
        print(results_port_scan)

        os_scan_results = os_scan(self.ip_addr.text)
        results_os_scan = show_results(os_scan_results)
        print(results_os_scan)

        end_time = datetime.now()

        end_time_formatted = end_time.strftime("%d-%m-%Y %H:%M:%S")

        pdf.set_font('Arial', 'B', 18)
        pdf.cell(0, 10, 'Scan information', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, 'Start time: {}'.format(start_time_formatted), 0, 'J')
        pdf.multi_cell(0, 10, 'End time: {}'.format(end_time_formatted), 0, 'J')
        pdf.multi_cell(0, 10, 'IP: {}'.format(self.ip_addr.text), 0, 'J')
        if self.port_range.text:
            pdf.multi_cell(0, 10, 'Port range: {}'.format(self.port_range.text), 0, 'J')
        else:
            pdf.multi_cell(0, 10, 'Port range: Default', 0, 'J')
        
        pdf.set_font('Arial', 'B', 18)
        pdf.cell(0, 10, 'Hosts responding to ICMP Ping', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, results_icmp_ping, 0, 'J')

        pdf.set_font('Arial', 'B', 18)
        pdf.cell(0, 10, 'Traceroute for discovered Hosts', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, results_traceroute, 0, 'J')
        
        pdf.set_font('Arial', 'B', 18)
        pdf.cell(0, 10, 'Port Scan', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, results_port_scan, 0, 'J')

        
        pdf.set_font('Arial', 'B', 18)
        pdf.cell(0, 10, 'Operating System Scan', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, results_os_scan, 0, 'J')

        pdf_generate_time = datetime.now()
        pdf_generate_time_formatted = pdf_generate_time.strftime("%d-%m-%Y %H:%M:%S")
        pdf.output('report-{}.pdf'.format(pdf_generate_time_formatted), 'F')

        self.output.text = 'PDF report created'

class PortScan(App):
   
    def build(self):
        self.title = "Simple auditor"
        return MyLayout()
        
   
   
if __name__ == '__main__':
    PortScan().run()