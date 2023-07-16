from datetime import date
from typing import List, Dict
from pydantic import BaseModel, ValidationError

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from models import Cargo
from tortoise.contrib.fastapi import register_tortoise

from testing_data import data as test_data


class CargoInfoResponse(BaseModel):
    date: str
    cargo_type: str
    rate: float
    price: float


app = FastAPI()


def chek_date(value: str):
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def get_cargos(cargo_type: str, cargo_price: float | int) -> List[Cargo]:
    return Cargo.filter(cargo_type__contains=cargo_type,
                        cargo_price__contains=cargo_price,)


def get_cargo_on_type(cargo_type: str) -> List[Cargo]:
    return Cargo.filter(cargo_type=cargo_type)


def create_cargo(cargo_type: str, cargo_price: float | int):
    return Cargo(cargo_type=cargo_type,
                 cargo_price=cargo_price,)


@app.get("/init_data")
async def init_data():
    mass = {
        'Glass': 10000,
        'Other': 24000,
        'Wood': 12000,
        'Metal': 8000,
    }
    for k, v in mass.items():
        result = await get_cargos(cargo_type=k, cargo_price=v)
        if len(result) == 0:
            obj = await create_cargo(cargo_type=k, cargo_price=v)
            await obj.save()
    return 'Данные занесены в базу'


async def get_price_func(data: dict):
    mass = {
        'request': [],
        'errors': []
    }
    if data is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=mass)
    for key, value in data.items():
        if len(data[f'{key}']) == 0:
            mass['errors'].append(f'По дате {key} нет данных о товаре')
        if not (chek_date(key)):
            mass['errors'].append(
                f'{key} - не является датой в формате YYYY-MM-DD')
            continue

        for elem in data[f'{key}']:
            try:
                cargo = await get_cargo_on_type(cargo_type=elem['cargo_type'])
                price = float(elem['rate']) * float(cargo[0].cargo_price)
                temp = CargoInfoResponse(
                    date=key,
                    cargo_type=elem['cargo_type'],
                    rate=elem['rate'],
                    price='{:0.2f}'.format(price),
                )
                mass['request'].append(temp)
            except IndexError as e:
                mass['errors'].append(
                    f"Данного товара нет в базе - {elem['cargo_type']}")
            except ValidationError as e:
                mass['errors'].append(e)
            except KeyError as e:
                mass['errors'].append(
                    f'По дате {key} пришли не полные данные о товаре')
    return mass


@app.get("/get_price_test")
async def get_price_test():
    return await get_price_func(test_data)


@app.post("/get_price")
async def get_price(data: Dict[str, List[Dict[str, str]]]):
    return await get_price_func(data)

register_tortoise(
    app,
    db_url="sqlite://db.sqlite",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
