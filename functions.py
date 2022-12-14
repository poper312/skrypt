from classes import Port, Host_port_scan, Host_os_scan, Host_icmp_ping
import nmap
from scapy.all import *
import sys
from io import StringIO
import subprocess

def os_scan(destination):
    nm = nmap.PortScanner()
    os_detection = nm.scan(destination, arguments="-O")
    hosts = []
    for host in nm.all_hosts():
        state = nm[host].state()
        if os_detection['scan'][host]['osmatch'] == []:
            os = 'Could not find os'
        else:
            os = os_detection['scan'][host]['osmatch'][0]['name']
        hosts.append(Host_os_scan(host, state, os))
    
    return hosts

def port_scan(destination, port_range):
    nm = nmap.PortScanner()
    if port_range:
        nm.scan(destination, port_range)
    else:
        nm.scan(destination)
    hosts = []
    for host in nm.all_hosts(): 
        for protocol in nm[host].all_protocols():
            open_ports = nm[host][protocol].keys()
            sorted(open_ports)
            for port in open_ports:
                host_state = nm[host].state()
                current_port = nm[host][protocol][port]
                hosts.append(
                    Host_port_scan(
                    host, 
                    host_state,
                    Port(
                            port, 
                            current_port['state'], 
                            current_port['name'], 
                            current_port['product'], 
                            current_port['version'], 
                            current_port['extrainfo']
                        )
                    )
                )

    return hosts


# umozliwia przeskanowanie sieci w ktorej jest urzadzenie wysylajace pakiety

def icmp_ping(destination):
    conf.L3socket = L3RawSocket 
    results = ''
    nm = nmap.PortScanner()
    nm.scan(destination)
    for host in nm.all_hosts():
        ans, unans = sr(IP(dst=host)/ICMP(), timeout=3)
        capture = StringIO()
        save_stdout = sys.stdout
        sys.stdout = capture
        ans.summary(lambda s,r: r.sprintf("%IP.src% is alive"))
        sys.stdout = save_stdout
        alive_ip = capture.getvalue()
        results = results + alive_ip
    
    return results

def tracert(destination):
    end_result = ''
    nm = nmap.PortScanner()
    nm.scan(destination)
    for host in nm.all_hosts():
        result = subprocess.run(['traceroute', host], stdout=subprocess.PIPE)
        end_result = end_result + result.stdout.decode('utf-8') + '\n'
    
    return end_result 

# def tracert(destination):
#     nm = nmap.PortScanner()
#     nm.scan(destination)
#     capture = StringIO()
#     save_stdout = sys.stdout
#     sys.stdout = capture
#     for host in nm.all_hosts():
#         print(host)
#         traceroute(host, maxttl=10)
#         print('\n')
#     sys.stdout = save_stdout

#     results = capture.getvalue()
    
#     return results



def show_results(scan):
    results = ''
    for host in scan:
        host_str = str(host)
        results = results + host_str + '\n'
    return results
    
# os_scan("192.168.48.12")

# for host in os_scan("192.168.48.0/24"):
#     print(host)

# for host in port_scan("192.168.2.0/24"):
#     print(host)

# tracert('192.168.2.0/24')

# icmp_ping("192.168.2.0/24")
# print(show_results(port_scan('192.168.1.254')))

# print(conf.L3socket)