import csv, os

whitelist_dict = {}

def fill_whitelist_dict():
    with open('./ip_whitelist/whitelist.csv', mode='r') as whitelist:
        reader = csv.DictReader(whitelist)
        for row in reader:
            ip = row.get("ip")
            port = row.get("port")
            whitelist_dict[ip] = port
    if whitelist_dict:
        grant_access_to_whitelist()
    else:
        print("There is no ip's to register")

def grant_access_to_whitelist():
    os.system("sudo ufw reset")
    print(whitelist_dict)
    for ip, port in whitelist_dict.items():
        os.system(f"sudo ufw allow from {ip} to any port {port}")
    os.system("sudo ufw enable")    
    os.system("sudo ufw status")