from classes import Port, Host_port_scan, Host_os_scan, Host_icmp_ping
import nmap
from scapy.all import *
import sys
from io import StringIO

def os_scan(destination):
    print("hejo")
    nm = nmap.PortScanner()
    os_detection = nm.scan(destination, arguments="-O")
    # print(os_detection)
    hosts = []
    for host in nm.all_hosts():
        # print(os_detection['scan'][host].keys())
        # print(os_detection['scan'])
        state = nm[host].state()
        if os_detection['scan'][host]['osmatch'] == []:
            os = 'Could not find os'
        else:
            os = os_detection['scan'][host]['osmatch'][0]['name']
        # if 'os_match' in nm[host]:
        #     os = os_detection['scan'][host]['osmatch'][0]['name']
        # else:
        #     os = 'Could not find os'
        # os = os_detection['scan'][host]['osmatch'][0]['name']
        hosts.append(Host_os_scan(host, state, os))
    
    return hosts

def port_scan(destination, port_range):
    nm = nmap.PortScanner()
    # nm.scan(destination, port_range)
    if port_range:
        nm.scan(destination, port_range) # przedzial od 1 do 65535 aby wykryc wszystkie porty
    else:
        nm.scan(destination)
    # nm.scan(destination)
    hosts = []
    for host in nm.all_hosts(): 
        for protocol in nm[host].all_protocols():

            # TU MOZNABY DAC WARUNEK CO JESLI NIE MA ZADNEGO OTWARTEGO PORTU

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

# def save_portscan_results(destination):
#     hosts = []
#     for host in port_scan(destination):
#         hosts.append(str(host))
#     return hosts

def icmp_ping(destination):
    hosts = []
    # print(conf.L3socket)
    conf.L3socket = L3RawSocket # umozliwia przeskanowanie sieci w kotrej jest urzadzenie wysylajace pakiety
    # print(conf.L3socket)
    ans, unans = sr(IP(dst=destination)/ICMP(), timeout=3)
    capture = StringIO()
    save_stdout = sys.stdout
    sys.stdout = capture
    ans.summary(lambda s,r: r.sprintf("%IP.src% is alive"))
    # ans_ips = [a[1].src for a in ans]
    # print(ans_ips)
    sys.stdout = save_stdout

    results = capture.getvalue()
    
    return results

def tracert(destination):
    nm = nmap.PortScanner()
    nm.scan(destination)
    capture = StringIO()
    save_stdout = sys.stdout
    sys.stdout = capture
    # print(type(sys.stdout))
    for host in nm.all_hosts():
        print(host)
        traceroute(host, maxttl=10)
        print('\n')
    sys.stdout = save_stdout

    results = capture.getvalue()
    
    return results



def show_results(scan):
    results = ''
    for host in scan:
        host_str = str(host)
        results = results + host_str + '\n'
    # print(results.splitlines())
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