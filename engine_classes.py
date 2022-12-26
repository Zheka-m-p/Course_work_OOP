import json
from abc import ABC, abstractmethod
from connector import Connector
import requests


class Engine(ABC):
    per_page = 20
    word_for_tmp_result = 'items'

    def get_request(self, search_word, count_vacancies):
        page = 0
        result = []
        while self.per_page * page < count_vacancies:
            tmp_result = self.make_request(search_word, page)
            if tmp_result:
                result += tmp_result.get(self.word_for_tmp_result)
                page += 1
            else:
                break
        return result

    @abstractmethod
    def make_request(self, search_word, page):
        raise NotImplementedError

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        return Connector(file_name)


class HH(Engine):
    base_URL = 'https://api.hh.ru'

    def make_request(self, search_word, page):
        print(f"Try to get page number: {page + 1}")
        response = requests.get(f"{self.base_URL}/vacancies?text={search_word}&page={page}")
        if response.status_code == 200:
            return response.json()
        return None


class SuperJob(Engine):
    word_for_tmp_result = 'objects'
    base_url = 'https://api.superjob.ru/2.0'
    secret_key = 'v3.r.133140039.721b65a4c1521cf8f9844a2d6683ee2190574bfb.515cb7c7cc95ced90c5e2002f57268a2960b8efe'

    def make_request(self, search_word, page):
        print(f"Try to get page number: {page + 1}")
        url = f"{self.base_url}/vacancies/?page={page}&keyword={search_word}"
        headers = {
            'X-Api-App-Id': self.secret_key,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.get(
            url=url,
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
        return None


if __name__ == '__main__':
    hh_engine = HH()
    search_word = 'Java'
    count_vacancies = 10

    result = hh_engine.get_request(search_word, count_vacancies)
    print(len(result))

    with open('HH_res.json', 'w', encoding='utf-8') as res_file:
        json.dump(result, res_file, ensure_ascii=False, indent=4)

    with open('HH_res.json', encoding='utf-8') as res_file:  # это чтобы красиво выводить из списка
        # но так же ещё нужно проверить про зп. её может не быть или же вилка зарплат может быть
        res_data = json.load(res_file)
        for item in res_data:
            print(f"{item.get('name')}, {item.get('salary', 'не указана')}, {item['area'].get('name')}")
    sj_engine = SuperJob()
    search_word = 'Java'
    count_vacancies = 100

    result = sj_engine.get_request(search_word, count_vacancies)
    print(len(result))
    with open('SJ_res.json', 'w', encoding='utf-8') as res_file:
        json.dump(result, res_file, ensure_ascii=False, indent=4)

    with open('SJ_res.json', encoding='utf-8') as res_file:  # это чтобы красиво выводить из списка
        res_data = json.load(res_file)
        for item in res_data:
            if item.get("payment_from") == 0 and item.get("payment_to") == 0:
                print(f"{item.get('profession')}, {item['town'].get('title')}, по договоренности")
            elif item.get("payment_from") == 0 and item.get("payment_to") != 0:
                print(
                    f"{item.get('profession')}, {item['town'].get('title')}, до {item.get('payment_to')} рублей/мес.")
            elif item.get("payment_from") != 0 and item.get("payment_to") == 0:
                print(
                    f"{item.get('profession')}, {item['town'].get('title')}, от {item.get('payment_from')} рублей/мес.")
            elif item.get("payment_from") != 0 and item.get("payment_to") != 0:
                print(
                    f"{item.get('profession')}, {item['town'].get('title')}, от {item.get('payment_from')} до {item.get('payment_to')} рублей/мес.")
