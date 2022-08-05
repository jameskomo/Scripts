# !/usr/bin/python
import os,glob
import json,csv

# all_branches=['master', 'conrad-nonprod-fastlane','conrad-nonprod-cloud', 'conrad-nonprod-cts']

# dir='/home/komo/Documents/Apigee/ApigeeProxies'
skips=['shared-flows','modifyProxy','target-server', 'proxy-formatter','z-ctrl-java-policies']

def get_cloud_branches():
    cloud_repos=[]

    for dir in glob.iglob(os.getcwd()+'/*', recursive=True):
        if os.path.isdir(dir) and not dir.endswith(tuple(skips)):
            proxy_name=os.path.basename(dir)
            print(proxy_name)
            file_path=dir+"/meta.json"
            if not os.path.isfile(file_path):
                print(f"WARNING! The proxy {proxy_name} does not contain a meta.json")
                with open(file_path, 'w') as f:
                    json.dump({}, f, indent=2)

            with open('./modifyProxy/proxy-to-envPrefix.json', 'r') as f:
                data = json.load(f)
                # proxy_from_json = next((item for item in data if item['proxie'] == proxy_name), None)
                env_prefix=None
                for prefix in data:
                    json_proxy=prefix.get('proxie')
                    if proxy_name==json_proxy:
                        env_prefix=prefix.get('envPrefix')
                if env_prefix==None:
                    print(f"WARNING! The proxy {proxy_name} does not have an environment prefix")
                    continue
                with open(file_path, 'r+') as f:
                    data=json.load(f)
                    f.seek(0)
                    data['envPrefix']=env_prefix
                    json.dump(data, f, indent=2)
                    f.write('\n')
    return cloud_repos
get_cloud_branches()
