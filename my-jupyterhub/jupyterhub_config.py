from tornado.httpclient import AsyncHTTPClient
import json

c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'
c.DummyAuthenticator.password = ""
c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'


async def foo(spawner, auth_state):
    spawner.log.error("auth state hook: here")
    api_url = 'https://jsonplaceholder.typicode.com/todos/1'

    response = await AsyncHTTPClient().fetch(api_url)
    data = json.loads(response.body.decode('utf8', 'replace'))
    spawner.log.error("le data" + str(data))
    spawner.login_allowed = True
    spawner.profile_list = [
            {
                'display_name': 'Training Env - Datascience',
                'slug': 'training-datascience',
                'kubespawner_override': {
                        'image' :'jupyterhub/singleuser:latest',
                        'cpu_limit': 0.3,
                        'mem_limit': '64M',
                    }, },
                {
                    'display_name': 'Training Env - Python',
                    'slug': 'training-python',
                    'default': True,
                    'kubespawner_override': {
                        'image' :'jupyterhub/singleuser:latest',
                        'cpu_limit': 0.1,
                        'mem_limit': '64M',
                        }
                    }
                ]

    # raise Exception(str(spawner) + "\n" + str(auth_state))
c.Spawner.auth_state_hook = foo


c.Authenticator.admin_users = ['jovyan']
