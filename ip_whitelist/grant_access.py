import csv, os

whitelist_dict = {}

def fill_whitelist_dict():
    with open('./ip_whitelist/whitelist.csv', mode='r') as whitelist:
        whitelist_dict = csv.DictReader(whitelist)
        for row in whitelist_dict:
            print(row)
    if whitelist_dict:
        grant_access_to_whitelist()
    else:
        print("There is no ip's to register")

def grant_access_to_whitelist():
    for ip, port in whitelist_dict.items():
        command = f"sudo ufw allow from {ip} to any port {port}"
        os.system(command)
    command = "sudo ufw enable"
    os.system(command)