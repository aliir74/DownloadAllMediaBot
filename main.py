from os.path import join as join_path
from secrets import bot_token
import requests

base_url = f'https://api.telegram.org'


@property
def url_with_token() -> str:
    return join_path(base_url, bot_token)


def gather_media_ids(data, photo_ids, video_ids):
    for message in data['result']:
        message_username = message['message']['from']['username'].lower()
        if message_username == username and ('photo' in message['message']):
            photo_ids.append(message['message']['photo'][-1]['file_id'])
        if message_username == username and ('video' in message['message']):
            video_ids.append(message['message']['video']['file_id'])


def get_videos(ids):
    for (idx, id) in enumerate(ids):
        params = {
            'file_id': id,
        }
        resp = requests.get(url=join_path(url_with_token, 'getFile'), params=params).json()
        path = resp['result']['file_path']
        name = path[7:len(path)]
        print('Downloading %.2f MB video...' % (resp['result']['file_size'] / 2 ** 20))
        file_resp = requests.get(url=join_path(base_url, 'file', bot_token, path))
        with open(name, 'wb') as f:
            for (idx2, chunk) in enumerate(file_resp.iter_content(chunk_size=1024)):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        print('video ' + str(idx + 1) + ' saved!')


def get_photos(ids):
    for (idx, id) in enumerate(ids):
        params = {
            'file_id': id,
        }
        resp = requests.get(url=join_path(url_with_token, 'getFile'), params=params).json()
        path = resp['result']['file_path']
        name = path[7:len(path)]
        file_resp = requests.get(url=join_path(base_url, 'file', bot_token, path))
        with open(name, 'wb') as f:
            for chunk in file_resp.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        print('photo ' + str(idx + 1) + ' saved!')


if __name__ == "__main__":
    parsed_response = requests.get(join_path(url_with_token, 'getUpdates')).json()
    username = (input('enter telegram id: ')).lower()

    photo_ids = []
    video_ids = []

    gather_media_ids(parsed_response, photo_ids, video_ids)

    print(len(photo_ids), ' photos found!')
    print(len(video_ids), ' videos found!')

    get_photos(photo_ids)
    get_videos(video_ids)
