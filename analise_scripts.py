from db.db import DB


"""
Скрипты для анализа таблицы результатов
Пункт 'определить количество объектов, для которых найденный адрес соответствует искомому' 
не до конца понял - если адрес найден, очевидно он соответствует искомому 
или подразумевается побуквенное совпадени(?)
"""


# count of found and not found:
db = DB()
print('Found: ', db.count_of_found())
print('Not found: ', db.count_of_not_found())


# group by square and region
results = db.get_all_results()
answ = {}
# в один проход заполняем словарь соответсвий кодов регионов, диапазонов площадей и количества объектов
for r in results:
    if r.square is None: continue
    if r.region_id not in answ:
        answ[r.region_id] = {}
    exist = False
    for region_id, _ in answ[r.region_id].items():
        if r.square > region_id[0] and r.square <= region_id[1]:
            answ[r.region_id][region_id] += 1
            exist = True
    if not exist:
        high = 0
        while high < r.square:
            high += 10
        low = high - 10
        answ[r.region_id][(low, high)] = 1

# словарь для отображени кодов в названия регионов
regions = db.get_all_regions()
code_name = {}
for r in regions:
    code_name[r.value] = r.name

# печать результата в удобочитаемом виде
for region_id, val in answ.items():
    print(code_name[region_id], ':')
    for range, count in val.items():
        print('\t', range, ': ', count)


