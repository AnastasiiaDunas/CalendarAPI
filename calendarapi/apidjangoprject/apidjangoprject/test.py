import requests


def test_user_signup():
    url = 'http://127.0.0.1:8000/api/user/signup/'
    data = {'username': 'newuser', 'name': 'New', 'surname': 'User', 'password': 'newpassword'}
    response = requests.post(url=url, params=data)
    if response.status_code == 200:
        print(url + ': passed')
    else:
        print(str(response.status_code) + ': ERROR')

def test_user_login():
    url = 'http://127.0.0.1:8000/api/user/login/'
    data = {'username': 'newuser', 'password': 'newpassword'}
    response = requests.post(url=url, params=data)
    token = response.json()['token']
    if response.status_code == 200:
        print(url + ': passed')
    else:
        print(str(response.status_code) + ': ERROR')
    return token

def test_create_event(token):
    url = f'http://127.0.0.1:8000/api/events/{token}/create/'
    data = {'title': 'Test Event', 'description': 'Event Description', 'event_date': '2023-01-01'}
    response = requests.post(url=url, params=data)
    if response.status_code == 200:
        print(url + ': passed')
    else:
        print(str(response.status_code) + ': ERROR')

def test_user_events(token):
    url = f'http://127.0.0.1:8000/api/events/{token}/list'
    response = requests.get(url=url)
    if response.status_code == 200:
        print(url + ': passed')
    else:
        print(str(response.status_code) + ': ERROR')

def test_update_event(token):
    url = f'http://127.0.0.1:8000/api/events/{token}/Test Event/update/'
    data = {'title': 'Updated Event', 'description': 'Updated Description', 'event_date': '2023-01-02'}
    response = requests.put(url=url, params=data)
    if response.status_code == 200:
        print(url + ': passed')
    else:
        print(str(response.status_code) + ': ERROR')

def test_delete_event(token):
    url = f'http://127.0.0.1:8000/api/events/{token}/Updated Event/delete/'
    response = requests.delete(url=url)
    if response.status_code == 200:
        print(url + ': passed')
    else:
        print(str(response.status_code) + ': ERROR')

def test_invite_user(token):
    url = f'http://127.0.0.1:8000/api/events/{token}/Updated Event/invite/'
    data = {'username': 'dunas'}
    response = requests.post(url=url, params=data)
    if response.status_code == 200:
        print(url + ': passed')
    else:
        print(str(response.status_code) + ': ERROR')

def test_event_invited_users(token):
    url = f'http://127.0.0.1:8000/api/events/Updated Event/users/'
    response = requests.get(url=url)
    if response.status_code == 200:
        print(url + ': passed')
    else:
        print(str(response.status_code) + ': ERROR')

def test_user_invitations(token):
    url = f'http://127.0.0.1:8000/api/user/{token}/invitations/'
    response = requests.get(url=url)
    if response.status_code == 200:
        print(url + ': passed')
    else:
        print(str(response.status_code) + ': ERROR')


test_user_signup()
token = test_user_login()
test_create_event(token)
test_user_events(token)
test_update_event(token)
test_invite_user(token)
test_event_invited_users(token)
test_user_invitations(token)
test_delete_event(token)
