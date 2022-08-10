# !/usr/bin/python
import os
import glob
from bs4 import BeautifulSoup
import json



class TargetServerLinter():

    def __init__(self):
        self.proxy_folder = os.getcwd()

    def get_target_servers(self):
        """
        returns all json files inside the apigeeproxies's /z-ctrl-target-server folder,
        ignoring files that start with . or _
        """
        target_folder = (f"{self.proxy_folder}/z-ctrl-target-server")
        target_server_names = []
        # read name attribute instead of target server file name
        for json_file in glob.iglob(target_folder+'/*.json', recursive=True):
            with open(json_file, 'r') as cur_file:
                target_server_json_file= json.load(cur_file)
                for _, config in enumerate(dict['config'] for dict in target_server_json_file): 
                    if config['name'] not in target_server_names:
                        target_server_names.append(config['name'])
        return target_server_names

    def get_xml_files(self):
        target_environment = "fastlane"
        server_name_in_proxies = []
        for xml_file in glob.iglob(os.getcwd()+'/*/apiproxy/targets/*.xml', recursive=True):
            proxy_name=xml_file.split('/')[-4]
            
            with open(xml_file, 'r') as f:
                file = f.read()
                soup = BeautifulSoup(file, 'xml')
                try:
                    server_names = soup.find('Server').attrs
                    server_name = server_names.get('name')
                    
                    if server_name not in self.get_target_servers():
                        print('---------------------------------')
                        print(
                            f"WARNING!! {proxy_name} would be deployed to environment {target_environment}, but references a target server {server_name} that does not exist in that environment.")
                        print('---------------------------------')
                    target_server_file_content = {}
                    target_server_path = (
                        f"{self.proxy_folder}/z-ctrl-target-server/{server_name}.json")
                    with open(target_server_path, 'r') as cur_file:
                        target_server_file_content = json.load(cur_file)
                        found = next(
                            (item for item in target_server_file_content if target_environment in item["environments"]), None)
                        if not found:
                            print(
                            f"This target server {server_name.upper()} does not include the assigned target env {target_environment}")
                except:
                    continue
            server_name_in_proxies.append(server_name)
            
        return target_environment
proxies = TargetServerLinter()
print(proxies.get_xml_files())

