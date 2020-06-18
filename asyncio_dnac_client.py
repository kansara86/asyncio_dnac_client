#!/usr/bin/env python

import asyncio
import aiohttp
import configparser
import json
import logging
import os


def get_root_dir():
    try:
        root_dir = os.path.dirname(os.path.dirname(__file__))
    except:
        raise RuntimeError('Failed to get the root directory')
    else:
        return root_dir


class DnacHttpSession:
    def __init__(self, host, username, password):
        # Default session parameters
        self.session = None

        if host.startswith('https://'):
            self.host_name = host
        else:
            self.host_name = f'https://{host}'

        if self.host_name.endswith('/'):
            self.host_name = self.host_name[:-1]

        loop = asyncio.get_event_loop()
        self.session = loop.run_until_complete(self.initialize_dnac_session(username, password))

    async def initialize_dnac_session(self, username, password):
        # Suppressing asyncio warnings for Unclosed client session/connector
        logging.getLogger('asyncio').setLevel(logging.CRITICAL)

        try:
            url = f'{self.host_name}/dna/system/api/v1/auth/token'
            async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(login=username, password=password),
                                             headers={'content-type': 'application/json', 'accept': 'application/json'}) as dnac_sess:
                async with dnac_sess.post(url=url, verify_ssl=False) as resp:
                    assert resp.status == 200
                    response = await resp.json()
                    token = response['Token']
        except:
            raise RuntimeError('Error in generating token in DNA-Center')
        else:
            dnac_headers = {
                'accept': 'application/json',
                'content-type': 'application/json',
                'x-auth-token': token
            }
            return aiohttp.ClientSession(headers=dnac_headers)

    async def rest_api_call(self, method, url, data):
        try:
            method = method.upper()

            if not url.startswith('https://'):
                url = self.host_name + url

            dnac_response = dict()
            if method not in ['GET', 'POST', 'DELETE', 'PUT']:
                raise RuntimeError('REST API Method not supported')

            resp = await self.session.request(method=method, url=url, data=data, ssl=False)
            dnac_response['status'] = resp.status
            dnac_response['body'] = await resp.json()
        except:
            raise RuntimeError('Error in DNA-Center REST API call')
        else:
            return dnac_response

    def create_rest_api_tasks(self, req_url_list):
        try:
            loop = asyncio.get_event_loop()

            for entry in req_url_list:
                if len(entry) == 2:
                    loop.create_task(self.rest_api_call(method=entry[0], url=entry[1], data=None))
                else:
                    loop.create_task(self.rest_api_call(method=entry[0], url=entry[1], data=json.dumps(entry[2])))

            pending_tasks = asyncio.Task.all_tasks()
            group = asyncio.gather(*pending_tasks, return_exceptions=True)
            results = loop.run_until_complete(group)
        except:
            raise
        else:
            return results


if __name__ == '__main__':
    try:
        config = configparser.ConfigParser()
        config_file = os.path.join(get_root_dir(), 'config.ini')
        config.read(config_file)

        dnac_sess = DnacHttpSession(host=config['DNAC']['Host'], username=config['DNAC']['Username'], password=config['DNAC']['Password'])
        project_resp = dnac_sess.create_rest_api_tasks([
            ('GET', '/dna/intent/api/v1/template-programmer/project'),
            ('POST', '/dna/intent/api/v1/template-programmer/project', {'name': 'Test Project', 'description': 'Test template project created using automation'})
        ])
    except:
        raise
    else:
        print(project_resp)
