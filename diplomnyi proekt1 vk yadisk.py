import requests
from pprint import pprint
import json
from tqdm import tqdm


class VkPhotos:
    URL = 'https://api.vk.com/method/photos.get'


    def __init__(self, owner_id):
        self.params = {
            'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
            'v': '5.131',
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'count': '17'
        }


    def photos_get_max(self, url_ph_get):  # метод получает максимально нужную информацию по фото в формате json
        photos = requests.get(url_ph_get, params=self.params).json()
        photos = photos['response']['items']
        new_list = []
        list_likes = []
        for i in photos:
            count_likes = str(i['likes']['count'])
            filename_data = ''
            if count_likes not in list_likes:
                list_likes.append(count_likes)
            else:
                filename_data = f"_{i['date']}"
            filename = f'{count_likes}{filename_data}.jpg'
            type_size = i['sizes'][-1]
            new_list.append({'file_name': filename, 'size': type_size['type'], 'url': type_size['url'], 'likes_count': count_likes})

        return new_list


    def photos_get(self, url_ph_get):  # метод получает информацию, заданную в условии по фото в формате json
            new_list = ph.photos_get_max(url_ph_get)
            info_list = []
            for info in new_list:
                info_list.append({'file_name': info['file_name'], 'size': info['size']})

            return info_list


ph = VkPhotos('34445487')

# pprint(ph.photos_get_max('https://api.vk.com/method/photos.get'))
# pprint(ph.photos_get('https://api.vk.com/method/photos.get'))


class Yadisk:

    def __init__(self, TOKEN_YA):
        self.TOKEN_YA = TOKEN_YA

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.TOKEN_YA)
        }

    def create_folder(self, disk_file_path):  # метод создает отдельную папку для загрузки фото, вводим путь и новую паку
        url_folder = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': disk_file_path}
        response_folder = requests.put(url_folder, headers=headers, params=params)
        if response_folder.status_code == 201:
            return "Success"
        if response_folder.status_code == 409:
            return 'Папка существует'

    def upload_file_to_disk(self, disk_file_path, comp_file_path):
        global response
        url_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        url_list = ph.photos_get_max('https://api.vk.com/method/photos.get')
        for urls in tqdm(url_list):
            filename = urls['file_name']
            params = {'url': urls['url'], "path": f'{disk_file_path}{filename}'}
            response = requests.post(url_upload, headers=headers, params=params)
        if response.status_code == 202:
            photos_list = ph.photos_get('https://api.vk.com/method/photos.get')
            with open(comp_file_path, 'w') as file:
                json.dump(photos_list, file)
                return 'Фото скопированы на яндекс диск'


ya = Yadisk('')
# pprint(ya.create_folder('/Netology/VKphotos/'))
pprint(ya.upload_file_to_disk('/Netology/VKphotos/', r'''D:\Study\Pycharm\Netology\Дипломный проект Основы python\Photos_list.json'''))