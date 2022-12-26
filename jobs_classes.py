# -*- coding: utf8 -*-
import json
import requests
from abc import abstractmethod


# from connector import Connector
# from engine_classes import SuperJob, HH


class Vacancy:
    """Базовый класс для создания объекта вакансий"""
    __slots__ = (
        'name_vacancy', 'link_vacancy', 'description_vacancy', 'salary_vacancy', 'experience_vacancy', 'salary_value')

    def __init__(self, name_vacancy, link_vacancy, description_vacancy, salary_vacancy, experience_vacancy,
                 salary_value):
        self.name_vacancy = name_vacancy
        self.link_vacancy = link_vacancy
        self.description_vacancy = description_vacancy
        self.salary_vacancy = salary_vacancy
        self.experience_vacancy = experience_vacancy
        self.salary_value = salary_value

    flag_description = True

    def __repr__(self):
        if self.flag_description:
            return f"Название вакансии: {self.name_vacancy}\n" \
                   f"Ссылка на вакансию: {self.link_vacancy}\n" \
                   f"Зарплата: {self.salary_vacancy} \n" \
                   f"Средняя зарплата после вычета налогов: {self.salary_value} \n" \
                   f"Требуемый опыт: {self.experience_vacancy} \n" \
                   f"Описание вакансии: \n{self.description_vacancy}"
        else:
            return f"Название вакансии: {self.name_vacancy}\n" \
                   f"Ссылка на вакансию: {self.link_vacancy}\n" \
                   f"Зарплата: {self.salary_vacancy} \n" \
                   f"Средняя зарплата после вычета налогов: {self.salary_value} \n" \
                   f"Требуемый опыт: {self.experience_vacancy} \n"

    # прописать проперки на всё из инита, не понял правда зачем, не сделал. Т.к. и без этого работает

    # прописаны магические методы для сравнегния по зп. но как ещё сранивать то... работают, ура
    # как сравниваем: в HH есть всегда нижняя планка, в SJ не всегда. Если есть обе границы, то делаем среднее
    # если, одна из границ только, то по ней будем сравнивать, если зп не указана, тогда считаем что значение "0"
    # так же зарплату сравниваем по чистой величине, после вычета всех налога в 13%
    # так же считаем, что зарплата у нас только у рублях везде указана, иначе это ещё можно кода расписать)
    def __eq__(self, other):
        return self.salary_value == other.salary_value

    def __ne__(self, other):
        return self.salary_value != other.salary_value

    def __gt__(self, other):
        return self.salary_value > other.salary_value

    def __ge__(self, other):
        return self.salary_value >= other.salary_value

    def __lt__(self, other):
        return self.salary_value < other.salary_value

    def __le__(self, other):
        return self.salary_value <= other.salary_value


class HHVacancy(Vacancy):  # add counter mixin
    """ HeadHunter Vacancy """
    __slots__ = ()


class SJVacancy(Vacancy):  # add counter mixin
    """ SuperJob Vacancy """
    __slots__ = ()


class ListVacancies:
    """Базовый класс для списка куда будем складывать вакансии (объекты других классов)"""

    def __init__(self, file_name='Pusto.json'):
        self.file_name = file_name
        self.value = -1
        self.data = []

    def __iter__(self):
        self.value = -1
        return self

    def __next__(self):  # для моей реализации пришлось ещё __len__ определять
        if self.value >= len(self.data) - 1:
            raise StopIteration('А всё. Элементы кончились')
        self.value += 1
        return self.data[self.value]

    @property
    def get_count_of_vacancy(self):
        """
        Вернуть количество вакансий от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        return len(self.data)

    def write_in_file(self, data_from_site):
        """Записывает наши данные с запроса в файл """
        with open(self.file_name, 'w', encoding='utf-8') as res_file:
            json.dump(data_from_site, res_file, ensure_ascii=False, indent=4)

    def print_in_file(self, file_name):
        """Записывает красиво в тхт файл краткое описание по каждой вакансии"""
        with open(file_name, 'w', encoding='utf-8') as res_file:
            count = 1
            for item in self.data:
                add_value = f"Название вакансии: {item.name_vacancy}\n" \
                            f"Ссылка на вакансию: {item.link_vacancy}\n" \
                            f"Зарплата: {item.salary_vacancy} \n" \
                            f"Средняя зарплата после вычета налогов: {item.salary_value} \n" \
                            f"Требуемый опыт: {item.experience_vacancy} \n"
                print(count, file=res_file)
                print(add_value, file=res_file)
                count += 1

    @abstractmethod
    def fill_vacancy_list(self):
        """ Заполняет список объектами вакансий конкретного класса
            Так же определяет для каждого экемпляра его атрибуты"""
        raise NotImplementedError('А ну давай переопределяй метод!')


class ListHHVacancies(ListVacancies):
    """ Класс для содержания объектов HHvacancy """

    def __init__(self, file_name='HH_res.json'):
        self.file_name = file_name
        self.value = -1
        self.data = []

    def fill_vacancy_list(self):
        # заполняю список объектами класса HHVacancy
        with open('HH_res.json', encoding='utf-8') as res_file:
            res_data = json.load(res_file)
            for work in res_data:
                name_vacancy = work.get('name')
                # link_vacancy = work.get('apply_alternate_url')
                # и смех и грех)))при переходе на ссылку автоматом делает отклик)))
                link_vacancy = work.get('alternate_url')
                salary_value = 0
                check_value = 0  # временная переменная, чтобы правильно посчитать итоговую зп для сравнения
                if work.get('salary'):
                    salary_vacancy = ''
                    if str(work['salary'].get('from')).isdigit():
                        salary_vacancy += f"от {work['salary'].get('from')}"
                        salary_value = work['salary'].get('from')
                        check_value = 1
                    if str(work['salary'].get('to')).isdigit():
                        salary_vacancy += f" до {work['salary'].get('to')}"
                        if check_value:
                            salary_value = (salary_value + work['salary'].get('to')) / 2
                        else:
                            salary_value = salary_value + work['salary'].get('to')
                    salary_vacancy += f" {work['salary'].get('currency')}"
                    if work['salary'].get('gross'):
                        salary_vacancy += f" до вычета налогов"
                        salary_value *= 0.87
                    else:
                        salary_vacancy += f" на руки"

                else:
                    salary_vacancy = 'не указана'
                url = work.get('url')
                response = requests.get(url)
                experience_vacancy = response.json()['experience'].get('name')
                html_description = response.json().get('description')  # описание вакансии, но с тэгами html
                # чуть ниже избавляюсь от тегов с помощью "костыля" какого смог придумать)
                tuple_for_clear_teg = (
                    ('<p><strong>', ''), ('</strong></p>', '\n'), ('<p>', ''), ('</p>', '\n'), ('</strong>', ''),
                    ('<strong>', ''),
                    ('<ul>', ''), ('</ul>', '\n'), ('<li>', ''), ('</li>', '\n'), ('<br />', '\n'), ('<br>', '\n'),
                    ('<ol>', ''),
                    ('</ol>', '\n'))
                for item in tuple_for_clear_teg:
                    html_description = html_description.replace(item[0], item[1])
                description_vacancy = html_description

                vacancy = HHVacancy(name_vacancy, link_vacancy, description_vacancy, salary_vacancy, experience_vacancy,
                                    salary_value)
                self.data.append(vacancy)


class ListSJVacancies(ListVacancies):
    def __init__(self, file_name='SJ_res.json'):
        self.file_name = file_name
        self.value = -1
        self.data = []

    def fill_vacancy_list(self):  # ВОТ ЭТО ПЕРЕДЕЛАТЬ. ОСТАЛЬНОЕ ВРОДЕ +- ТАКОЕ ЖЕ
        # заполняю список объектами класса HHVacancy
        with open('SJ_res.json', encoding='utf-8') as res_file:
            res_data = json.load(res_file)
            for work in res_data:
                name_vacancy = work.get('profession')
                link_vacancy = work.get('link')
                salary_value = 0
                salary_vacancy = ''
                if work.get('agreement'):
                    salary_vacancy = 'По договоренности'
                else:
                    if work.get('payment_from') == work.get('payment_to') and work.get('payment_from') != 0:
                        salary_value = work.get('payment_from')
                        salary_vacancy = str(work.get('payment_from'))
                    elif work.get('payment_from') != 0 and work.get('payment_to') == 0:
                        salary_value = work.get('payment_from')
                        salary_vacancy += f"от {work.get('payment_from')}"
                    elif work.get('payment_to') != 0 and work.get('payment_from') == 0:
                        salary_value = work.get('payment_to')
                        salary_vacancy += f"до {work.get('payment_to')}"
                    elif work.get('payment_from') != 0 and work.get('payment_to') != 0:
                        salary_value = (work.get('payment_from') + work.get('payment_to')) / 2
                        salary_vacancy += f"от {work.get('payment_from')} до {work.get('payment_to')}"
                    print(type(salary_vacancy))
                    salary_vacancy += " Р/в месяц"

                experience_vacancy = work['experience'].get('title')
                description_vacancy = work.get('candidat')
                if work.get('languages'):
                    description_vacancy += f"\nНавыки: \n"
                    for lang in work.get('languages'):
                        description_vacancy += f"\n{lang[0].get('title')}({lang[1].get('title')})"
                vacancy = HHVacancy(name_vacancy, link_vacancy, description_vacancy, salary_vacancy, experience_vacancy,
                                    salary_value)
                self.data.append(vacancy)


def sorting(vacancies, reverse_=False):
    """ Сортирует переданный список (НА МЕСТЕ) по возрастанию(по умолчанию) ежемесячной оплате (gt, lt magic methods)
        А так же возврращает список, в котором убраны значения, в которых зарплата не указана"""
    vacancies.sort(reverse=reverse_)  # надо использовать sort, c sorted не сработало...
    return [vac for vac in vacancies if vac.salary_value != 0]


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods)
        Убирает вакансии, где не указана зарплата, поэтому могут быть выведены не все вакансии,
        при условии, что top_count будет приближен к длине списка vacancies"""
    sorting(vacancies, reverse_=True)
    return [vacancies[x] for x in range(top_count) if vacancies[x].salary_value != 0]


def get_vacancy_without_exp(vacancies):
    """ Возвращает список вакансий, в которых не требуется опыт """
    return [work for work in vacancies if
            work.experience_vacancy == 'Не имеет значения' or work.experience_vacancy == 'Нет опыта']


if __name__ == '__main__':
    pass
