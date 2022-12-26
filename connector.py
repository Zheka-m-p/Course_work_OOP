import json


class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None

    def __init__(self, df):
        self.__data_file = df
        self.__connect()

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        """
        try:  # Если нельзя прочитать, то создаём новый файл на запись c пустым списком
            with open(self.__data_file, 'r', encoding='UTF-8'):
                pass
        except FileNotFoundError:
            with open(self.__data_file, 'w', encoding='UTF-8') as file_write:
                json.dump([], file_write, indent=4)

    def insert(self, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        with open(self.__data_file, 'r+', encoding='UTF-8') as file_read:
            res = json.load(file_read)
        with open(self.__data_file, 'w', encoding='UTF-8') as file_write:
            res.append(data)
            json.dump(res, file_write, indent=4)

    def select(self, query):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        with open(self.__data_file, 'r', encoding='UTF-8') as file_for_read:
            all_data = json.load(file_for_read)
            if len(query) == 0:
                return list(all_data)
            else:
                res = []
                key_sort, *other_keys = query.keys()
                value_sort, *other_values = query.values()
                for dictionary in all_data:
                    for k, v in dictionary.items():
                        if k == key_sort and v == value_sort:
                            res.append(dictionary)
                return res

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select
        """
        with open(self.__data_file, 'r', encoding='UTF-8') as file_for_read:
            all_data = json.load(file_for_read)
        with open(self.__data_file, 'w', encoding='UTF-8') as file_for_write:
            if len(query) == 0:
                # json.dump([], file_for_write, indent=4)  # удаляет все данные, если словарь пустой
                json.dump(all_data, file_for_write, indent=4)  # оставляет все данные, если пустой словарь
            else:
                res = []
                key_sort, *other_keys = query.keys()
                value_sort, *other_values = query.values()
                for dictionary in all_data:
                    if key_sort in dictionary and dictionary[key_sort] != value_sort:
                        res.append(dictionary)
                    elif key_sort not in dictionary:
                        res.append(dictionary)
                json.dump(res, file_for_write, indent=4)


if __name__ == '__main__':
    df = Connector('df.json')

    data_for_file = {'id': 1, 'title': 'tet'}

    df.insert(data_for_file)
    data_from_file = df.select(dict())
    assert data_from_file == [data_for_file]

    df.delete({'title': 'tet'})
    data_from_file = df.select(dict())
    assert data_from_file == []
