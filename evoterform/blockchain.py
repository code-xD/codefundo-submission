from adal import AuthenticationContext
import requests

AUTHORITY = 'https://login.microsoftonline.com/shivansh586gmail.onmicrosoft.com'
WORKBENCH_API_URL = 'https://hack-ucqyga-api.azurewebsites.net'
RESOURCE = '2c949b1d-0722-493d-bb18-234af0ac2b70'
CLIENT_APP_Id = '928837dc-23d8-4e6c-8098-f6c27b7dbbae'
CLIENT_SECRET = 'aAPeRY[]fDTSZB:4R-CLq5TtHgvJ03Kl'

auth_context = AuthenticationContext(AUTHORITY)


def ContractPOSTData(data, dataset):
    token = auth_context.acquire_token_with_client_credentials(
        RESOURCE, CLIENT_APP_Id, CLIENT_SECRET)
    headers = {'Authorization': 'Bearer ' + token['accessToken']}
    contractData = {
        "workflowFunctionId": 17,
        "workflowActionParameters": [
            {
                "name": "v_name",
                "value": data['voter_name']
            },
            {
                "name": "v_name_t",
                "value": dataset['voter_name']

            },
            {
                "name": "gnd",
                "value": data['gender']
            },
            {
                "name": "gnd_t",
                "value": dataset['gender']

            },
            {
                "name": "long_no",
                "value": f"[{data['age']},{data['s_code']},{data['c_code']},{data['d_code']},{dataset['age']},{dataset['s_code']},{dataset['c_code']},{dataset['d_code']}]"

            },
            {
                "name": "main_data",
                "value": f"[{data['aadhar_no']},{data['pin']},{dataset['aadhar_no']},{dataset['pin']}]"

            },
            {
                "name": "add1",
                "value": data['aLine1']

            },
            {
                "name": "add2",
                "value": data['aLine2']

            },
            {
                "name": "add1_t",
                "value": dataset['aLine1']

            },
            {
                "name": "add2_t",
                "value": dataset['aLine2']

            }
        ]
    }
    response = requests.post(
        WORKBENCH_API_URL + '/api/v2/contracts?workflowId=8&contractCodeId=6&connectionId=1', headers=headers, json=contractData)
    contractID = response.text
    length = 0
    data['contractProperties'] = []

    while(length == 0):
        if len((data['contractProperties'])) == 0:
            response = requests.get(
                WORKBENCH_API_URL + f'/api/v2/contracts/{contractID}', headers=headers)
            data = response.json()
        else:
            break

    return contractID


def contractVerify(contractID):
    token = auth_context.acquire_token_with_client_credentials(
        RESOURCE, CLIENT_APP_Id, CLIENT_SECRET)
    headers = {'Authorization': 'Bearer ' + token['accessToken']}

    functionData = {
        "workflowFunctionId": 18,
        "workflowActionParameters": []
    }

    response = requests.post(
        WORKBENCH_API_URL + f'/api/v2/contracts/{contractID}/actions', headers=headers, json=functionData)
    # print(response.status_code)


def getContractState(contractID):
    token = auth_context.acquire_token_with_client_credentials(
        RESOURCE, CLIENT_APP_Id, CLIENT_SECRET)
    headers = {'Authorization': 'Bearer ' + token['accessToken']}
    response = requests.get(
        WORKBENCH_API_URL + f'/api/v2/contracts/{contractID}', headers=headers)
    data = response.json()
    contractState = data['contractProperties'][0]['value']
    while contractState == '0':
        response = requests.get(
            WORKBENCH_API_URL + f'/api/v2/contracts/{contractID}', headers=headers)
        data = response.json()
        contractState = data['contractProperties'][0]['value']
    return data['contractProperties'][0]['value']


def runblockchain(contestant, template):
    try:
        contractID = ContractPOSTData(contestant, template)
        contractVerify(contractID)
        return getContractState(contractID)
    except Exception as error:
        return error


if __name__ == '__main__':

    contestant = {
        'voter_name': "Shivansh",
        'age': 19,
        'gender': 0,
        'aadhar_no': 123456781234,
        'pin': 400706,
        'd_code': 5,
        'c_code': 6,
        's_code': 1,
        'aLine1': '302,Neelkanth Pride',
        'aLine2': 'Sector-42/A,Plot No:35/36'
    }
    template = {
        'voter_name': "Shivansh",
        'age': 19,
        'gender': 0,
        'aadhar_no': 123456781234,
        'pin': 400706,
        'd_code': 5,
        'c_code': 6,
        's_code': 1,
        'aLine1': '302,Neelkanth Pride',
        'aLine2': 'Sector-42/A,Plot No:35/36'
    }

    try:
        contractID = ContractPOSTData(contestant, template)
        contractVerify(contractID)
        print(getContractState(contractID))
    except Exception as error:
        print(error)
