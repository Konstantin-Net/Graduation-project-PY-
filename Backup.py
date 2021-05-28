import requests
import json


class VKFoto:
    url = "https://api.vk.com/method/"
    token = "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008"
    version = 5.131

    def __init__(self, id_vk):
        self.id = id_vk

    def upload_foto(self):      # Функция возвращае словарь с ссылками на фото и из размером
        params = {"access_token": self.token,
                  "v": self.version,
                  "user_id": self.id,
                  "album_id": "profile",
                  "extended": 1
                  }
        requests_test = requests.get(self.url + "photos.get", params).json()    # Получение от ВК json-ответа c ссылками на фото
        dict_foto = {}      # В этот словарь добавляются необходимые данные (ссылки на фото и их размер)
        for i in requests_test['response']['items']:    # Парсинг ответа ВК с добавлением данных в словарь
            if str(i["likes"]["count"]) not in dict_foto:
                dict_foto[str(i["likes"]["count"])] = [i['sizes'][-1]['url']]
                dict_foto[str(i["likes"]["count"])].append(i['sizes'][-1]['type'])
            else:
                dict_foto[f"{i['likes']['count']}_{i['date']}"] = [i['sizes'][-1]['url']]
                dict_foto[f"{i['likes']['count']}_{i['date']}"].append(i['sizes'][-1]['type'])
        return dict_foto


class YandexDisk:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _creating_folder(self):     # Функции создаёт папку на яндекс диске
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {"path": "Photo_VK"}
        response = requests.put(url, headers=headers, params=params)
        return response.json()

    def creating_info_file(self, file_link):       # Функции создаётся json-файл c параметрами запысанных фоток
        info_file = list()
        for i in file_link:
            info_file.append(dict([("file_name", i), ("size", file_link[i][1])]))
        with open("info_file.json", "w") as f:
            json.dump(info_file, f)
        return f"Создан json-файл 'info_file.json'. Содержание:\n{info_file}"

    def upload_file_link_to_disk(self, file_link):      # Функция записывает фотографии из ссылок на яндекс диск
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        self._creating_folder()
        headers = self.get_headers()
        progress_bar = 1    # Cчётчик для прогресс-бара
        for i in file_link:     # Последовательная запись фоток на яндекс диск и прогресс-бар
            params = {"url": file_link[i][0], "path": f"Photo_VK/{i}.jpg"}
            response = requests.post(upload_url, headers=headers, params=params)
            print(f"Загружено {progress_bar} фото из {len(file_link)} ---- Ответ сервера - {response.status_code} ")
            progress_bar += 1
        print("Все фото загружены! \n")
        return self.creating_info_file(file_link)


if __name__ == "__main__":
    vk = VKFoto(str(input("Введите id пользователя VK ")))
    ya = YandexDisk(str(input("Введите токен с Полигона Яндекс.Диска ")))
    print(ya.upload_file_link_to_disk(vk.upload_foto()))

