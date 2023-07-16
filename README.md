
# Тестовый проект



## Развёртка

Клонируем репозиторий заходим в директорию

```bash
  git clone https://github.com/Pelmexaxa/test_task.git
  cd .\test_task\
```

Сборка и запуск
```bash
  docker-compose build
  docker-compose up
```

## Документация
API: [localhost](http://127.0.0.1:8000/docs) `http://127.0.0.1:8000/docs`

#

`/init_data` - **get** запрос на внесение данных в базу (уже внесены)

Данные в базе:

![DB](https://i.imgur.com/ZTkzMwl.png)

#

`/get_price_test` - **get** запрос на проверку тестовыми данными (файл `testing_data.py`)

#

`/get_price` - **post** запрос для получение цены страхования

сервер возвращает следующий формат JSON:

```json
{
    "request": [
            {
                "date": "2020-06-01",
                "cargo_type": "Glass",
                "rate": 0.04,
                "price": 400.0
            },
            {
                "date": "2020-06-01",
                "cargo_type": "Other",
                "rate": 0.01,
                "price": 240.0
            },
    "errors" : [
            "additionalProp1 - не является датой в формате YYYY-MM-DD",
            "additionalProp2 - не является датой в формате YYYY-MM-DD",
            "additionalProp3 - не является датой в формате YYYY-MM-DD",
            "По дате 2020-06-02 нет данных о товаре",
            "вздбадбвдаблд - не является датой в формате YYYY-MM-DD"
        ]
    ]
}
```

`request` - Список из объектов который хранит в себе данные:

    "date" - дата (принятая в запросе)
    "cargo_type": - тип товара (принятый в запросе и прошедший проверку в базе, на его основании берётся исходная цена)
    "rate": - рейтинг (коэфициент умножения, принятый в запросе)
    "price": - цена страхования (результат умножения исходной цены на рейтинг)


`errors` - Список из ошибок полученных в ходе обработки данных

## Стек

Фреймворк: [FastAPI](https://fastapi.tiangolo.com)

ОRM для работы с sqlite: [Tortoise ORM](https://tortoise.github.io)

Инструмент для структурирования данных: [Pydantic](https://docs.pydantic.dev/latest/)



## Authors

- [@pelmexaxa](https://www.github.com/pelmexaxa)

