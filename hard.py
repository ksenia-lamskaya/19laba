# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from datetime import datetime

from jsonschema import validate
from jsonschema.exceptions import ValidationError


def validation(instance):
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name1": {"type": "string"},
                "name2": {"type": "string"},
                "number": {"type": "number"},
                },
            },
            "required": ["name1", "name2", "number"],
        }

    try:
        validate(instance, schema=schema)
        return True
    except ValidationError as err:
        print(err.message)
        return False


def help():
    """"
    Функция для вывода списка команд
    """
    # Вывести справку о работе с программой.
    print("Список команд:\n")
    print("add - добавить маршрут;")
    print("list - вывести список маршрутов;")
    print("select <тип> - вывод на экран пунктов маршрута, используя номер маршрута;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")
    print("load - загрузить данные из файла;")
    print("save - сохранить данные в файл;")

def load_point(file_name):
    with open(file_name, "r") as f:
        point = json.load(f)
    
    if validation(point):
        return point


def save_point(file_name, point_list):
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(point_list, f, ensure_ascii=False, indent=4)


def add():
    """"
    Функция для добавления информации о новых маршрутах
    """
    # Запросить данные о маршруте.
    name = input("Название начального пункта маршрута:  ")
    name2 = input("Название конечного пункта маршрута: ")
    number = int(input("Номер маршрута: "))

    # Создать словарь.
    i = {'name': name, 'name2': name2, 'number': number}

    return i


def error(command):
    """"
    функция для неопознанных команд
    """
    print(f"Неизвестная команда {command}")


def list(point):
    """"
    Функция для вывода списка добавленных маршрутов
    """
    # Заголовок таблицы.
    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
    '-' * 4,
    '-' * 30,
    '-' * 20,
    '-' * 8
    )
    print(line)
    print(
        '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
            "№",
            "Начальный пункт.",
            "Конечный пункт",
            "№ маршрута"
        )
    )
    print(line)

    # Вывести данные о всех маршрутах.
    for idx, i in enumerate(point, 1):
        print(
            '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                idx,
                i.get('name', ''),
                i.get('name2', ''),
                i.get('number', '')
            )
    )
    print(line)


def select(point):
    """""
    Функция для получения маршрута по его номеру
    """
    # Разбить команду на части для выделения номера маршрута.
    parts = input("Введите значение: ")
    # Проверить сведения работников из списка.

    # Проверить сведения.
    flag = True
    for i in point:
        if i['number'] == int(parts):
            print("Начальный пункт маршрута - ", i["name"])
            print("Конечный пункт маршрута - ", i["name2"])
            flag = False
            break
    if flag:
        print("Маршрут с таким номером не найден")


def main():
    """"
    Главная функция программы.
    """
    print("Список команд:\n")
    print("add - добавить маршрут;")
    print("list - вывести список маршрутов;")
    print("select <тип> - вывод на экран пунктов маршрута, используя номер маршрута;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")
    print("load - загрузить данные из файла;")
    print("save - сохранить данные в файл;")

    point = []

    while True:
        command = (
            input("Введите команду (add, info, list, load, save, exit, help): ")
            .strip()
            .lower()
            .split(maxsplit=1)
        )

        match command:
            case ["exit"]:
                break

            case ["load", file_name]:
                new_point_list = load_point(file_name)
                if new_point_list:
                    point = new_point_list

            case ["save", file_name]:
                save_point(file_name, point)

            case ["add"]:
                # Добавить словарь в список.
                i = add()
                point.append(i)
                # Отсортировать список в случае необходимости.
                if len(point) > 1:
                    point.sort(key=lambda item: item.get('number', ''))

            case ["list"]:
                list(point)

            case ["select"]:
                select(point)

            case ["help"]:
                help()

            case _:
                print(f"Неизвестная команда {command[0]}", file=sys.stderr)


if __name__ == '__main__':
    main()