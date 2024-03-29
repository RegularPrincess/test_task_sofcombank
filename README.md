# test_task_sofcombank

Имеется интернет-ресурс https://egrp365.ru/ ( https://egrp365.ru/extra/ )
Необходимо реализовать поиск информации об объекте недвижимости
(многоквартирный дом, квартира).

Входные параметры для поиска должны задаваться в виде параметров
функций/класса.
Входной параметр поиска: Адрес объекта.
Адрес объекта может подаваться как одной строкой для простого поиска, так и
отдельными параметрами (Регион, город, улица, дом) для расширенного поиска.

Выходные данные должны содержать:
Кадастровый номер объекта,
найденный адрес объекта,
ссылку на кадастровую карту объекта (при поиске дома),
этаж, площадь (при поиске квартиры)
географические координаты объекта (при поиске на главной странице),
полный json ответа при поиске (при поиске на главной странице)
Из результатов поиска в разделе Мой дом / Паспорт / Общие сведения.
Из полученных результатов формируем данные для записи в БД.

2. Использование БД (SQL)
Создать таблицу, которая будет являться источником для поиска информации об
объекте недвижимости. Т.е. подразумевается, что скрипт поиска (python) работает
независимо, и при появлении «новой» записи в таблице он (скрипт) определяет эту
запись. Эта запись должна содержать входные параметры поиска.
Создать таблицу результатов, в которую записываются результаты поиска.
После получения результатов написать скрипты для следующего анализа:
- определить количество найденных и не найденных объектов.
- определить количество объектов, для которых найденный адрес соответствует
искомому.
- определить количество объектов в каждом регионе для определенного сегмента,
определяемого площадью объекта. В первый сегмент попадают объекты с площадью
0–10 кв.м., во второй 11-20 кв.м. и т.д.

Дополнительно, будет плюсом:
Написать скрипт/процедуру, которая в случае если по объекту результат не найден,
будет возвращать объект обратно в поиск до трех раз. Если три попытки поиска подряд
завершились неудачно, то больше не пытаемся его искать.
Под выражением добавить в поиск подразумеевается появление «новой» записи в
таблице источнике.

