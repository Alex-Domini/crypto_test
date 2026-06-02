# Crypto Price Tracker

Приложение периодически получает цены `BTC_USD` и `ETH_USD` с биржи Deribit, сохраняет их в PostgreSQL и предоставляет REST API для чтения данных.

## Стек

- Python 
- FastAPI 
- PostgreSQL 
- SQLAlchemy
- Alembic
- Celery 
- Redis
- httpx

## Структура проекта

```
Crypto_test
├─ alembic.ini
├─ app
│  ├─ api
│  │  └─ routes
│  │     └─ price.py
│  ├─ celery_app.py
│  ├─ core
│  │  ├─ base.py
│  │  ├─ config.py
│  │  └─ db.py
│  ├─ main.py
│  ├─ models
│  │  └─ price.py
│  ├─ repositories
│  │  └─ price_repository.py
│  ├─ schemas
│  │  └─ price.py
│  ├─ services
│  │  ├─ deribit_client.py
│  │  └─ price_service.py
│  └─ tasks
│     └─ price_tasks.py
├─ migrations
│  ├─ env.py
│  ├─ README
│  ├─ script.py.mako
│  └─ versions
│     ├─ 17f51225672e_create_price_table.py
│     └─ e4865aa9c146_change_price_scale_to_2.py
├─ README.md
└─ requirements.txt
```

## Локальный запуск

## Переменные окружения

Создать `.env` и заполнить:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=crypto_db
REDIS_URL=redis://localhost:6379/0
```

**Требования:** Python 3.11+, PostgreSQL, Redis
Перед запуском приложения убедитесь, что PostgreSQL и Redis запущены локально.

```bash
git clone https://github.com/Alex-Domini/crypto_test.git 
cd crypto_test

python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

Применить миграции Alembic:
- alembic upgrade head

uvicorn app.main:app --reload
```

Документация API: http://127.0.0.1:8000/docs

## Celery

В двух отдельных терминалах:

```bash
# На Windows worker запускается с `--pool=solo`.
- celery -A app.celery_app:celery_app worker --loglevel=info --pool=solo
- celery -A app.celery_app:celery_app beat --loglevel=info
```

После этого приложение будет получать цены каждую минуту.

## API

### GET /prices/history

Вся история цен по тикеру.

```
GET /prices/history?ticker=BTC_USD
```

```json
[
  { "ticker": "BTC_USD", "price": 67423.5, "timestamp": 1746613200 },
  { "ticker": "BTC_USD", "price": 67318.0, "timestamp": 1746613140 }
]
```

### GET /prices/latest

Последняя цена по тикеру.

```
GET /prices/latest?ticker=ETH_USD
```

```json
{ "ticker": "ETH_USD", "price": 3182.75, "timestamp": 1746613200 }
```

### GET /prices/date_range

Цены по тикеру в диапазоне дат.

```
GET /prices/date_range?ticker=BTC_USD&date_from=2026-05-01&date_to=2026-05-10
```

```json
[
  { "ticker": "BTC_USD", "price": 67423.5, "timestamp": 1746613200 }
]
```

## Архитектурные решения

**DeribitClient** — отдельный класс для работы с внешним API биржи. Изолирует HTTP-логику от бизнес-логики.

**Repository / Service** — `PriceRepository` отвечает за SQL-запросы, `PriceService` — за сценарий получения и сохранения цен. Снижает связность и упрощает тестирование.

**Celery** — периодические задачи через Celery Beat + worker. Beat формирует расписание, worker выполняет задачи.

**UNIX timestamp** — поле `timestamp` хранится в формате UNIX timestamp согласно требованиям задания.

**Pydantic-схема ответа** — публичный ответ не содержит внутреннего `id`, чтобы не раскрывать детали реализации таблицы.

**Формат дат в API** — фильтрация принимает `YYYY-MM-DD`, внутри конвертируется в UNIX timestamp. Удобно для клиента, совместимо с форматом хранения.
