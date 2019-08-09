
default_protocol = ["ftp", "ssh", "telnet", "smtp", "pop3", "http", "fox", "bacnet",
                    "dnp3", "imap", "ipp", "modbus", "mongodb", "mssql", "mysql", "ntp",
                    "oracle", "postgres", "redis", "siemens", "smb", "amqp", "vnc", "dns",
                    "ipmi", "ldap", "rdp", "rpc", "rsync", "sip", "snmp", "tftp"]

us_ports = [21, 22, 23, 25, 80, 110, 137, 139, 161, 443, 445, 515, 1433, 1900, 3306,
            3389, 6379, 7547, 8080, 9200, 22105, 37777]


normal_ports = [13, 21, 22, 23, 25, 26, 53, 69, 80, 81, 88, 110, 111, 123, 135, 137,
                139, 161, 179, 264, 389, 443, 445, 465, 515, 520, 623, 636, 873, 902,
                992, 993, 995, 1234, 1241, 1433, 1521, 1604, 1701, 1900, 1967, 2181,
                3000, 3128, 3260, 3306, 3307, 3388, 3389, 4000, 4730, 5000, 5001,
                5060, 5353, 5357, 5400, 5555, 5672, 5900, 5938, 5984, 6000, 6379,
                6665, 6666, 6667, 6668, 6669, 7474, 7547, 7777, 8000, 8080, 8081, 8087,
                8089, 8834, 9200, 9999, 10000, 12345, 14000, 22105, 27017, 37777, 50000, 50100, 61613]


# portmap暂未实现, decrpc未实现, netbios未实现, bgp未实现,
# firewall-1未实现, lpd未实现, rip未实现, l2tv未实现, upnp未实现,
# zookeeper未实现, iscsi未实现, gearman未实现, mdns未实现, elastic未实现
# teamviewer未实现, x11未实现, irc未实现, dahua-dvr未实现, upnp未实现
# db2未实现, stomp, rifa-dvr, vmware_authentication_daemon
unfinished = ["bgp", "lpd", "rip", "l2tv", "iscsi", "db2", "stomp"]

foreign_protocols = {
    21: ["ftp", "http", "ssh"],
    22: ["ssh", "http", "ftp"],
    23: ["telnet", "http", "ssh"],
    25: ["smtp", "http", "ftp"],
    80: ["http", "ssh", "ftp"],
    137: ["nbns", "http", "ssh"],
    139: ["nbss", "http", "ssh"],
    161: ["snmp", "http", "ssh"],
    443: ["http", "ssh"],
    445: ["smb", "http"],
    515: ["lpd", "http", "ssh"],
    1433: ["mssql", "http", "ssh"],
    1900: ["http", "upnp", "ssh"],
    3306: ["mysql", "http", "ssh"],
    3389: ["rdp", "http", "ssh"],
    6379: ["redis", "http", "ssh"],
    7547: ["http", "ssh", "ftp"],
    8080: ["http", "ssh", "ftp"],
    9200: ["http", "ssh", "elastic"],
    22105: ["http", "ssh"],
    37777: ["http", "ssh", "dahua_dvr"],
}

port_protocols = {
    13: ["daytime", "ssh", "http"],
    21: ["ftp", "http", "ssh"],
    22: ["ssh", "http", "ftp"],
    23: ["telnet", "http", "ssh"],
    25: ["smtp", "http", "ftp"],
    26: ["smtp", "http", "ssh"],
    53: ["dns", "http", "ssh"],
    69: ["tftp", "http", "ssh"],
    80: ["http", "ssh", "ftp"],
    81: ["http", "ssh", "ftp"],
    88: ["http", "ssh", "ftp"],
    110: ["pop3", "http", "ssh"],
    111: ["portmap", "ssh", "http"],
    123: ["ntp", "http", "ssh"],
    135: ["dcerpc", "http", "ssh"],
    137: ["nbns", "http", "ssh"],
    139: ["nbss", "http", "ssh"],
    161: ["snmp", "http", "ssh"],
    179: ["bgp", "http", "ssh"],
    264: ["cpfw", "http", "ssh"],
    389: ["ldap", "http", "ssh"],
    443: ["http", "ssh"],
    445: ["smb", "http"],
    465: ["smtp", "http"],
    515: ["lpd", "http", "ssh"],
    520: ["rip", "http", "ssh", "ftp"],
    623: ["ipmi", "http", "ssh", "ftp"],
    636: ["ldap", "http", "ssh"],
    873: ["rsync", "http", "ssh"],
    902: ["vmware", "http", "ftp"],
    992: ["http", "telnet", "ssh", "ftp"],
    993: ["imap", "http", "ssh", "ftp"],
    995: ["pop3", "http", "ssh"],
    1234: ["http", "ssh", "ftp"],
    1241: ["http", "ssh", "ftp"],
    1433: ["mssql", "http", "ssh"],
    1521: ["oracle", "http", "ftp"],
    1604: ["http", "ssh", "ftp"],
    1701: ["l2tv", "http", "ssh", "ftp"],
    1900: ["http", "upnp", "ssh"],
    1967: ["http", "ssh", "ftp"],
    2181: ["zookeeper", "http", "ssh"],
    3000: ["http", "ssh", "ftp"],
    3128: ["http", "ssh", "ftp"],
    3260: ["iscsi", "http", "ssh"],

    # 3306: ["mysql", "http", "ssh"],
    # 3307: ["mysql", "http", "ssh"],
    # 3388: ["rdp", "http", "ssh"],
    # 3389: ["rdp", "http", "ssh"],
    # 4000: ["http", "ssh", "ftp"],
    # 4730: ["http", "ssh", "gearman"],
    # 5000: ["http", "ssh"],
    # 5001: ["http", "ssh", "ftp"],
    # 5060: ["sip", "http", "ssh"],
    # 5353: ["mdns", "http", "ssh"],
    # 5357: ["http", "ssh", "ftp"],
    # 5400: ["http", "ssh", "ftp"],
    # 5555: ["http", "ssh"],
    # 5672: ["amqp", "http", "ssh"],
    # 5900: ["vnc", "http", "ssh"],
    # 5938: ["http", "teamviewer", "ssh"],
    # 5984: ["http", "ssh", "ftp"],
    # 6000: ["http", "ssh", "x11"],
    # 6379: ["redis", "http", "ssh"],
    # 6665: ["http", "ssh", "irc"],
    # 6666: ["http", "ssh", "irc"],
    # 6667: ["http", "ssh", "irc"],
    # 6668: ["http", "ssh", "irc"],
    # 6669: ["http", "ssh", "irc"],
    # 7474: ["http", "ssh", "ftp"],
    # 7547: ["http", "ssh", "ftp"],
    # 7777: ["http", "ssh", "ftp"],
    # 8000: ["http", "ssh"],
    # 8080: ["http", "ssh", "ftp"],
    # 8081: ["http", "ssh", "mysql"],
    # 8087: ["http", "ssh", "ftp"],
    # 8089: ["http", "ssh", "ftp"],
    # 8834: ["http", "ssh", "ftp"],
    # 9200: ["http", "ssh", "elastic"],
    # 9999: ["http", "ssh"],
    # 10000: ["http", "ssh"],
    # 12345: ["http", "ssh", "ftp"],
    # 14000: ["http", "ssh", "ftp"],
    # 22105: ["http", "ssh"],
    # 27017: ["http", "ssh", "mongodb"],
    # 37777: ["http", "ssh", "dahua_dvr"],
    # 50000: ["http", "ssh", "db2"],
    # 50100: ["http", "rifatron", "ftp"],
    # 61613: ["http", "ssh", "stomp"]
}


ztag_command = {
    'ftp': '-P ftp -S banner',
    'ssh': '-P ssh -S v2',
    'telnet': '-P telnet -S banner',
    'smtp': '-P smtp -S starttls',
    'http': '-P http -S get',
    'pop3': '-P pop3 -S starttls',
    'smb': '-P smb -S banner',
    'imap': '-P imap -S starttls',
    'modbus': '-P modbus -S device_id',
    'mssql': '-P mssql -S banner',
    'oracle': '-P oracle -S banner',
    'fox': '-P fox -S device_id',
    'mysql': '-P mysql -S banner',
    'postgres': '-P postgres -S banner',
    'mongodb': '-P mongodb -S banner',
    'bacnet': '-P bacnet -S device_id',
    'dnp3': '-P dnp3 -S status',
}
