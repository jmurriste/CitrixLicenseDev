import requests
import logging
import json
import urllib3
from pprint import pprint

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

psw_url = 'https://psw.neutrona.com:9119/api/passwords/'
mcn_passwordListID = '5121'
mcn_psw_querystring = {"APIKey": "2a347fcdb85e39679adf38254bec3653", "QueryAll": ""}
customers_passwordListID = '6139'
customers_psw_querystring = {"APIKey": "6483cdb9e23fa75df8b45c73a3e2696e", "QueryAll": ""}


headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"}


def get_inventory(querystring, passwordListId):
    '''
    Gets Citrix inventory from PSW
    :param psw_querystring(mcn_psw_querystring) or psw_querystring(customers_psw_querystring)
    :return: array of equipment
    '''
    logger.info('Getting inventory')
    response = requests.get(psw_url+passwordListId, headers=headers, params=querystring, verify=False)
    password_list = json.loads(response.content.decode('UTF-8'))
    equipment_list = []

    for i in password_list:
        if 'center' not in i['Title'].lower():  # Avoids to add SD-WAN Center to the inventory
            equipment = {}
            equipment['name'] = i['Title']
            equipment['username'] = i['UserName']
            equipment['ip'] = i['URL'].strip('https://')
            equipment['password'] = i['Password']
            equipment['Description'] = i['Description']
            equipment['Country'] = i['GenericField1']
            equipment['City'] = i['GenericField2']
            equipment['POP'] = i['GenericField3']
            equipment['SID'] = i['GenericField4']
            equipment_list.append(equipment)


    return equipment_list


def citrix_login(name, ip, user, password):
    '''
    Login into Citrix MCN
    :param ip:
    :param user:
    :param password:
    :return: session established with all corresponding parameters including cookies

    '''
    mcn_session = requests.session()
    login_url = 'https://' + ip + '/sdwan/nitro/v1/config/login'
    payload = '{"login":{"username":"' + user + '","password":"' + password + '"}}'

    logger.info('Trying to login to %s', name)
    mcn_session.post(login_url, data=payload, headers=headers, verify=False)
    logger.info('Successfully logged in into %s', name)

    return mcn_session


def license_info(mcn_session, ip, mcn_name):
    '''

    :param mcn_session:
    :param ip:
    :param mcn_name:
    :return:
    '''
    equipment_data = {}

    url = 'https://'+ip+'/sdwan/nitro/v1/config/license_info'

    logger.info('Getting license info from %s', mcn_name)

    response = mcn_session.get(url, headers=headers, verify=False)
    data = json.loads(response.content.decode('UTF-8'))
    equipment_data['license_type'] = data['license_info']['license_type']
    equipment_data['local_license_server_hostid'] = data['license_info']['local_license_server_hostid']
    equipment_data['license_expiry'] = data['license_info']['license_expiry']
    equipment_data['max_bw'] = data['license_info']['max_bw']
    equipment_data['model'] = data['license_info']['model']
    equipment_data['state'] = data['license_info']['state']
    equipment_data['system_patform'] = data['license_info']['system_patform']

    return equipment_data


def system_info(mcn_session, ip, mcn_name):
    '''

    :param mcn_session:
    :param ip:
    :param mcn_name:
    :return:
    '''

    equipment_data = {}

    url = 'https://'+ip+'/sdwan/nitro/v1/config/system_options'

    logger.info('Getting system info from %s', mcn_name)
    response = mcn_session.get(url, headers=headers, verify=False)
    data = json.loads(response.content.decode('UTF-8'))


    equipment_data['name'] = mcn_name
    equipment_data['license_state'] = data['system_options']['license_state']
    equipment_data['model'] = data['system_options']['model']
    equipment_data['serial_no'] = data['system_options']['serial_no']
    equipment_data['product'] = data['system_options']['product']
    equipment_data['license_info'] = license_info(mcn_session, ip, mcn_name)

    return equipment_data


def main(psw_querystring, passwordListId):

    # Getting the inventory
    mcn_inventory = get_inventory(psw_querystring, passwordListId)

    all_equipment_data = []

    for mcn in mcn_inventory:
        try:
            mcn_session = citrix_login(mcn['name'], mcn['ip'], mcn['username'], mcn['password'])
            all_equipment_data.append(system_info(mcn_session, mcn['ip'], mcn['name']))
        except Exception as ee:
            logger.info(ee)
            equipment_data = {'name': mcn['name'], 'error': str(ee)}
            all_equipment_data.append(equipment_data)

    return all_equipment_data


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    with open('SDWAN_Centers&Concentrators.json', 'w') as f:
        json.dump(main(mcn_psw_querystring, mcn_passwordListID), f)
    with open('SDWAN_Customer_devices.json', 'w') as f:
        json.dump(main(customers_psw_querystring, customers_passwordListID), f)
    '''
    Original ROD
    '''
