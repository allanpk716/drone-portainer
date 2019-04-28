import os
import sys

import requests


if __name__ == '__main__':
    url = (os.getenv('PLUGIN_URL') or '') + '/api'
    username = os.getenv('PLUGIN_USERNAME') or ''
    password = os.getenv('PLUGIN_PASSWORD') or ''
    stack = os.getenv('PLUGIN_STACK') or ''
    endpoint = os.getenv('PLUGIN_ENDPOINT') or 'primary'

    print('debug')
    print(username)
    print(password)
    print('debug')

    print('*** Portainer Stack Update')
    print('*** URL: ' + url)
    print('*** Stack: ' + stack)

    try:
        jwt = requests.post(
            url + '/auth',
            json={
                'Username': username,
                'Password': password
            }
        ).json()['jwt']

        headers = {
            'Authorization': 'Bearer ' + jwt
        }

        for e in requests.get(url + '/endpoints', headers=headers).json():
            if e['Name'] == endpoint:
                endpointId = str(e['Id'])

        for s in requests.get(url + '/stacks', headers=headers).json():
            if s['Name'] == stack:
                id = str(s['Id'])

        env = requests.get(
            url + '/stacks/' + id,
            headers=headers).json()['Env']
        stackfilecontent = requests.get(
            url + '/stacks/' + id + '/file',
            headers=headers).json()['StackFileContent']

        r = requests.put(
            url + '/stacks/' + id + '?endpointId=' + endpointId,
            headers=headers,
            json={
                'StackFileContent': stackfilecontent,
                'Env': env,
                'Prune': False
            }
        )
    except (KeyError, requests.exceptions.RequestException) as e:
        print('*** Stack update failed.')
        print(e)
        sys.exit(1)

    print('*** Stack update succeeded.')
