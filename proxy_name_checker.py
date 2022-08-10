# !/usr/bin/python
import os,glob
from bs4 import BeautifulSoup



skips=['shared-flows','modifyProxy','target-server', 'proxy-formatter','z-ctrl-java-policies']
subdir_skips=['proxies','targets', 'policies', 'resources']
def proxy_name_checker():
    for dir in glob.iglob(os.getcwd()+'/*', recursive=True):
        proxy_name=os.path.basename(dir).lower()
        if os.path.isdir(dir) and not dir.endswith(tuple(skips)):
            proxies_dir=dir+"/apiproxy/policies"
            for item in os.listdir(proxies_dir) :
                if item.endswith('.xml') :
                    # Get file path from file
                    file_name=item.split('.')[0]
                    # get file path to read from xml parser
                    file_path=proxies_dir+"/"+item
                    # Read the XML file
                    with open(file_path, 'r') as f:
                        # check for empty xml files and warn about them
                        if os.stat(file_path).st_size == 0:
                            print(f"WARNING!! The file {file_name}.xml is empty. Please fix it...")
                            # os.remove(file_path)
                            continue
                        file = f.read()
                        soup = BeautifulSoup(file, 'xml')
                        # //check if file contains both Path and ProxyEndpoint
                        if soup.find("ProxyEndpoint") and soup.find("ProxyEndpoint") in soup():
                            print(f"WARNING!! The proxy {dir.split('/')[-1]} has a file {file_name}.xml that contains both <Path> and <ProxyEndpoint> elements. Please fix it...")
                        names = soup.find().attrs
                        proxy_name=names.get('name')
            if file_name.lower()!=proxy_name.lower():
                print(f"{proxy_name} is different from {file_name}")
proxy_name_checker()
