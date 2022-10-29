class Port:
    def __init__(self, port, state, service, product, version, extra_info):
        self.port = port
        self.state = state
        self.service = service
        self.product = product
        self.version = version
        self.extra_info = extra_info

class Host_port_scan:
    def __init__(self, address, state, open_port):
        self.address = address 
        self.state = state
        self.open_port = open_port
    # def __str__(self):
    #         return "-----------\nHost: {}\nState of host: {}\nPort: {}\nState of port: {}\nService: {}\nProduct: {}\nVersion: {}\nExtra info: {}".format(
    #                                 self.address, self.state, self.open_port.port, 
    #                                 self.open_port.state, self.open_port.service, self.open_port.product, 
    #                                 self.open_port.version, self.open_port.extra_info)
    def __str__(self):
        return """---------------------------------------------------------------------------------
        Host: {} 
        State of host: {} 
        Port: {}
        State of port: {}
        Service: {}
        Product: {}
        Version: {}
        Extra info: {}""".format(self.address, self.state, self.open_port.port, 
                                self.open_port.state, self.open_port.service, self.open_port.product, 
                                self.open_port.version, self.open_port.extra_info)


    # def __str__(self):
    #     return '-----------\n Host: {} \n State: {} \n Port info: {}'.format(self.address, self.state, vars(self.open_ports))


class Host_os_scan:
    def __init__(self, address, state=None, os_family=None):
        self.address = address 
        self.state = state
        self.os_family = os_family
    
    def __str__(self):
        return """---------------------------------------------------------------------------------
        Host: {}
        State: {} 
        OS family: {}""".format(self.address, self.state, self.os_family)

class Host_icmp_ping:
    def __init__(self, address, state):
        self.address = address
        self.state = state

    def __str__(self):
        return self.summary()