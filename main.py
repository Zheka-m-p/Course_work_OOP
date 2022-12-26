# import json
# from connector import Connector
from engine_classes import HH, SuperJob
from jobs_classes import sorting, get_top, ListHHVacancies, ListSJVacancies, Vacancy, get_vacancy_without_exp

if __name__ == '__main__':
    print('Работает файл main')
    print(f"Введите номер сайта на котором будем искать: {HH.base_URL} {SuperJob.base_url} 1 или 2 соответственно: ")
    website_number = int(input())
    # website_number = 1
    print(f"Введите ключевое слово, по которому будем искать")
    search_word = input()
    # search_word = 'Python'
    print(f"Введите сколько вакансий хотите найти: ")
    count_vacancies = int(input())
    # count_vacancies = 100
    if website_number == 1:
        L = ListHHVacancies()  # создаем экземпляр класса, где будем хранить наши вакансии с HH, имя файла можем указать
        hh_engine = HH()
        result = hh_engine.get_request(search_word, count_vacancies)
    else:
        L = ListSJVacancies()
        sj_engine = SuperJob()
        result = sj_engine.get_request(search_word, count_vacancies)

    L.write_in_file(result)  # записываем в наш файл результаты запроса
    L.fill_vacancy_list()  # заполняем список вакансиями с HH
    print(L.get_count_of_vacancy)
    for i in range(len(L.data)):  # Выводим все вакансии с их описанием, описание пришлось искать через другой запрос
        print()
        print(L.data[i])
    Vacancy.flag_description = False  # убираем описание вакансии, чтобы лишний раз не загромождать вывод
    sorting(L.data)
    print('СОРТИРОВКА ПО ВОЗРАСТАНИЮ: ')
    print()
    print(*sorting(L.data), sep='\n')  # делаем сортировку по возрастанию и выводим работы, где указана зп
    # print(L.data) # подтверждение тому, что сортирует правильно(на месте)
    print('ТОП N ВАКАНСИЙ ПО ЗАРПЛАТЕ')
    print()
    for vacancy_ in get_top(L.data, 5):  # выводим топ вакансий по зарплате
        print(vacancy_)
    print('СПИСОК ВАКАНСИЙ ГДЕ НЕ НУЖЕН ОПЫТ: ')
    print()
    print(*get_vacancy_without_exp(L.data), sep='\n')  # список вакасний где не нужен опыт, не легко было найти на HH
    L.print_in_file('HH.txt')  # запись всех данных в файл txt
