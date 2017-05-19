import requests

token = 'bot376718798:AAHmKK35FP0zDvKNlZ4EEAo7fTC2ro8dx94'
url = 'https://api.telegram.org/'
x = requests.get('https://api.telegram.org/bot376718798:AAHmKK35FP0zDvKNlZ4EEAo7fTC2ro8dx94/getMe')
parsed = (requests.get(url+token+'/getUpdates').json())

photo_ids = []
video_ids = []

username = (input('enter telegram id: ')).lower()

for message in parsed['result']:
    if(message['message']['from']['username'].lower() == username and ('photo' in message['message'])):
        #for j in message['message']['photo']:
        photo_ids.append(message['message']['photo'][-1]['file_id'])
    if(message['message']['from']['username'].lower() == username and ('video' in message['message'])):
        # for j in message['message']['photo']:
        video_ids.append(message['message']['video']['file_id'])

print(len(photo_ids), ' photos')
print(len(video_ids), ' videos')

for (idx,i) in enumerate(photo_ids):
    params2 = {
        'file_id': i,
    }
    tmp = requests.get(url=url + token + '/getFile', params=params2).json()
    path = tmp['result']['file_path']
    name = path[7:len(path)]
    r = requests.get(url=url + 'file/' + token + '/'+path)
    with open(name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    f.close()
    print('photo '+ str(idx+1)+' saved!')


for (idx,i) in enumerate(video_ids):
    params2 = {
        'file_id': i,
    }
    tmp = requests.get(url=url + token + '/getFile', params=params2).json()
    #print(tmp)
    path = tmp['result']['file_path']
    name = path[7:len(path)]
    print('Downloading %.2f MB video...' % (tmp['result']['file_size']/2**20))
    r = requests.get(url=url + 'file/' + token + '/'+path)
    with open(name, 'wb') as f:
        for (idx2,chunk) in enumerate(r.iter_content(chunk_size=1024)):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    f.close()
    print('video '+ str(idx+1)+' saved!')