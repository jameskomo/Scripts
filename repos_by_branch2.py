# !/usr/bin/python
from calendar import c
import os,glob
import pandas as pd
import json,csv

# all_branches=['master', 'conrad-nonprod-fastlane','conrad-nonprod-cloud', 'conrad-nonprod-cts']

# dir='/home/komo/Documents/Apigee/ApigeeProxies'
skips=['shared-flows','target-server', 'proxy-formatter']

def get_master_branches():
    master_all_dirs=[]

    for dir in glob.iglob('/home/komo/Documents/Apigee/branches/master/ApigeeProxies/*', recursive=True):
        if os.path.isdir(dir) and not dir.endswith(tuple(skips)):# filter dirs
            split_dir=dir.split('/')[-1]
            master_all_dirs.append(split_dir)
            continue
            # df = pd.DataFrame(columns=['Master_Repos'], data=master_all_dirs)
            # df.to_csv('master_repos.csv')
    return master_all_dirs
get_master_branches()

# conrad-nonprod-fastlane
def get_fastlane_branches():
    fastlane_all_dirs=[]

    for dir in glob.iglob('/home/komo/Documents/Apigee/branches/conrad-nonprod-fastlane/ApigeeProxies/*', recursive=True):
        if os.path.isdir(dir) and not dir.endswith(tuple(skips)):# filter dirs
            split_dir=dir.split('/')[-1]
            fastlane_all_dirs.append(split_dir)
            continue
            # df = pd.DataFrame(columns=['Fastlane'], data=fastlane_all_dirs)
            # df.to_csv('master_repos.csv')
    return fastlane_all_dirs
get_fastlane_branches()

# conrad-nonprod-cloud
def get_cloud_branches():
    cloud_all_dirs=[]

    for dir in glob.iglob('/home/komo/Documents/Apigee/branches/conrad-nonprod-cloud/ApigeeProxies/*', recursive=True):
        if os.path.isdir(dir) and not dir.endswith(tuple(skips)):# filter dirs
            split_dir=dir.split('/')[-1]
            cloud_all_dirs.append(split_dir)
            continue
            # df = pd.DataFrame(columns=['Cloud'], data=cloud_all_dirs)
            # df.to_csv('master_repos.csv')
    return cloud_all_dirs
get_cloud_branches()


# conrad-nonprod-cts
def get_cts_branches():
    cts_all_dirs=[]

    for dir in glob.iglob('/home/komo/Documents/Apigee/branches/conrad-nonprod-cts/ApigeeProxies/*', recursive=True):
        if os.path.isdir(dir) and not dir.endswith(tuple(skips)):# filter dirs
            split_dir=dir.split('/')[-1]
            # print(split_dir)
            cts_all_dirs.append(split_dir)
            # print(cts_all_dirs)
            continue
    return cts_all_dirs
            
            # df = pd.DataFrame(columns=['CTS'], data=cts_all_dirs)
            # df.to_csv('master_repos.csv')
get_cts_branches()

def create_dict():
    allproxies={}
    allproxies['Master']=get_master_branches()
    allproxies['Fastlane']=get_fastlane_branches()
    allproxies['Cloud']=get_cloud_branches()
    allproxies['CTS']=get_cts_branches()
create_dict()

def write_to_csv():

    # ['foo', 'bar']
    master=get_master_branches()
    # ['foo', 'wuz']
    fastlane=get_fastlane_branches()
    cloud=get_cloud_branches()
    cts=get_cts_branches()

    # {'foo': ('master', 'fastlane'), 'bar': ('master', ''), 'wuz': ('', 'fastlane')}

    allproxies = {}
    for proxy in master:
        if proxy not in allproxies.keys():
            allproxies[proxy] = ['', '', '', '', '', '', '', '']
        allproxies[proxy][0] = 'master'

    for proxy in fastlane:
        if proxy not in allproxies.keys():
            allproxies[proxy] = ['', '', '', '', '', '', '', '']
        allproxies[proxy][1] = 'fastlane'

    for proxy in cloud:
        if proxy not in allproxies.keys():
            allproxies[proxy] = ['', '', '', '', '', '', '', '']
        allproxies[proxy][2] = 'cloud'

    for proxy in cts:
        if proxy not in allproxies.keys():
            allproxies[proxy] = ['', '', '', '', '', '', '', '']
        allproxies[proxy][3] = 'cts'

    with open('deployed_proxies.json') as json_data:
        deployed_proxies = json.load(json_data)
        json_data.close()

    for proxyObject in deployed_proxies:
        proxy = proxyObject['name']
        if proxy not in allproxies.keys():
            allproxies[proxy] = ['', '', '', '', '', '', '', '']
        
        for envs in proxyObject['environment']:
            if envs['name'] == 'fastlane':
                allproxies[proxy][4] = 'fastlane'
            elif envs['name'] == 'cloud':
                allproxies[proxy][5] = 'cloud'
            elif envs['name'] == 'cts':
                allproxies[proxy][6] = 'cts'
            else:
                print(f"unknown env {envs['name']}")

    #df = pd.DataFrame(list(zip(master, fastlane, cloud, cts)), columns=['Master','Fastlane','Cloud','CTS'])
    df = pd.DataFrame.from_dict(allproxies, orient="index")
    df.to_csv('master_repos4.csv')

write_to_csv()


