# !/usr/bin/python
import os,glob
import pandas as pd
import json,csv

# all_branches=['master', 'conrad-nonprod-fastlane','conrad-nonprod-cloud', 'conrad-nonprod-cts']

# dir='/home/komo/Documents/Apigee/ApigeeProxies'
skips=['shared-flows','target-server', 'proxy-formatter']

def get_master_branches():
    all_dirs=[]

    for dir in glob.iglob('/home/komo/Documents/Apigee/branches/master/ApigeeProxies/*', recursive=True):
        if os.path.isdir(dir) and not dir.endswith(tuple(skips)):# filter dirs
            split_dir=dir.split('/')[-1]
            all_dirs.append(split_dir)
            df = pd.DataFrame(columns=['Master_Repos'], data=all_dirs)
            df.to_csv('master_repos.csv')
get_master_branches()

# # conrad-nonprod-fastlane
def get_fastlane_branches():
    all_dirs=[]

    for dir in glob.iglob('/home/komo/Documents/Apigee/branches/conrad-nonprod-fastlane/ApigeeProxies/*', recursive=True):
        if os.path.isdir(dir) and not dir.endswith(tuple(skips)):# filter dirs
            split_dir=dir.split('/')[-1]
            all_dirs.append(split_dir)
            df = pd.DataFrame(columns=['Fastlane'], data=all_dirs)
            df.to_csv('fastlane_repos.csv')
get_fastlane_branches()

# # conrad-nonprod-cloud
def get_cloud_branches():
    all_dirs=[]

    for dir in glob.iglob('/home/komo/Documents/Apigee/branches/conrad-nonprod-cloud/ApigeeProxies/*', recursive=True):
        if os.path.isdir(dir) and not dir.endswith(tuple(skips)):# filter dirs
            split_dir=dir.split('/')[-1]
            all_dirs.append(split_dir)
            df = pd.DataFrame(columns=['Cloud'], data=all_dirs)
            df.to_csv('cloud_repos.csv')
get_cloud_branches()


# conrad-nonprod-cts
def get_cts_branches():
    all_dirs=[]

    for dir in glob.iglob('/home/komo/Documents/Apigee/branches/conrad-nonprod-cts/ApigeeProxies/*', recursive=True):
        if os.path.isdir(dir) and not dir.endswith(tuple(skips)):# filter dirs
            split_dir=dir.split('/')[-1]
            # print(split_dir)
            all_dirs.append(split_dir)
            df = pd.DataFrame(columns=['CTS'], data=all_dirs)
            df.to_csv('cts_repos.csv')
get_cts_branches()

