import json, logging, sys, os
from dotenv import load_dotenv

def get_from_file(path):
    logging.info(f"Fetching apps from file {'/'.join(path.split('/')[-3:])}")
    with open(path, "r") as apps_file:
        all_apps = json.load(apps_file)
        return all_apps

def main():
    load_dotenv()
    load_dotenv('./default.env')
    logging.basicConfig(format='%(levelname)s:%(message)s', level=os.getenv('LOG_LEVEL'))

    edge_apps=get_from_file('./scripts/comparison/apigee_edge/apigee_edge_files/all_apps.txt')
    x_apps=get_from_file('./scripts/comparison/apigee_x/apigee_x_files/all_apps.txt')

    # fetch developers and put them into a neat dictionary to translate developerIds to emails
    edge_devs_raw=get_from_file('./scripts/comparison/apigee_edge/apigee_edge_files/all_developers.txt')
    x_devs_raw=get_from_file('./scripts/comparison/apigee_x/apigee_x_files/all_developers.txt')
    edge_devs={dev['developerId']: dev['email'] for dev in edge_devs_raw['developer']}
    x_devs={dev['developerId']: dev['email'] for dev in x_devs_raw['developer']}

    all_apps_are_similar = apps_match(edge_apps, x_apps, edge_devs, x_devs)

    # if there are no differences return status code 0 (successful), otherwise 1
    sys.exit(0 if all_apps_are_similar else 1)

def apps_match(edge_apps: list, x_apps: list, edge_devs: dict, x_devs: dict):
    apps_with_different_keys=[]

    # compare app names + developer emails (together: unique) to find those which only exist in one instance
    edge_app_names=list(map(lambda app: app['name'] + edge_devs[app['developerId']], edge_apps['app']))
    x_app_names=list(map(lambda app: app['name'] + x_devs[app['developerId']], x_apps['app']))
    only_on_edge=[app for app in edge_app_names if app not in x_app_names]
    only_on_x=[app for app in x_app_names if app not in edge_app_names]

    # compare the api keys of apps that have the same name + developer email in both instances
    for edge_app in edge_apps['app']:
        for x_app in x_apps['app']:
            if edge_app['name']==x_app['name'] and edge_devs[edge_app['developerId']]==x_devs[x_app['developerId']]:
                if not credentials_match(edge_app['name'], edge_app['credentials'], x_app['credentials']):
                    apps_with_different_keys.append(edge_app['name'])

    all_apps_are_similar = len(only_on_edge) == 0 and len(only_on_x) == 0 and len(apps_with_different_keys) == 0

    if not all_apps_are_similar:
        if len(only_on_edge) > 0:
            logging.warning('Apps that exist only on Apigee edge:')
            logging.warning(only_on_edge)
        if len(only_on_x) > 0:
            logging.warning('Apps that exist only on Apigee X:')
            logging.warning(only_on_x)
        if len(apps_with_different_keys) > 0:
            logging.warning('Apps where API Keys don\'t match:')
            logging.warning(apps_with_different_keys)

    return all_apps_are_similar

def credentials_match(app_name: str, edge_credentials: list, x_credentials: list):
    in_edge_not_in_x=[
        credential for credential in edge_credentials
        if len([x for x in x_credentials if credential_match(x, credential)]) == 0
    ]
    in_x_not_in_edge=[
        credential for credential in x_credentials
        if len([x for x in edge_credentials if credential_match(credential, x)]) == 0
    ]

    if len(in_edge_not_in_x) > 0:
        logging.debug(f'App {app_name} has following API Keys on Apigee Edge only:')
        logging.debug(list(map(lambda credential: credential['consumerKey'], in_edge_not_in_x)))
    if len(in_x_not_in_edge) > 0:
        logging.debug(f'App {app_name} has following API Keys on Apigee X only:')
        logging.debug(list(map(lambda credential: credential['consumerKey'], in_x_not_in_edge)))

    return len(in_edge_not_in_x) == 0 and len(in_x_not_in_edge) == 0

def credential_match(edge_credential: dict, x_credential: dict):
    return edge_credential['consumerKey'] == x_credential['consumerKey']

if __name__ == "__main__":
    main()
