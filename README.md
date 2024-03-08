# Спортивные чувачки

Сайт нужен для проведения соревнований по любому виду спорта. Поддерживает управление несколькими людьми: судьями и администратором соревнования

## Установка и запуск

### Linux

1. Загрузка репозитория

```bash
git clone https://github.com/MoxForever/sport_site
cd sport_site
```

2. Создание виртуального окружения

```bash
pip3 install virtualenv
python3 -m venv .venv
source .venv/bin/activate
```

3. Установка библиотек

```bash
pip install -r requirements.txt
```

4. Запуск сервера

```bash
uvicorn main:app --port <PORT> --host <HOST>
```
### Windows

1. Загрузка репозитория

```bash
git clone https://github.com/MoxForever/sport_site
cd sport_site
```

2. Создание виртуального окружения

```bash
pip install virtualenv
python -m venv .venv
source .venv\Scripts\activate
```

3. Установка библиотек

```bash
pip install -r requirements.txt
```

4. Запуск сервера

```bash
python -m uvicorn main:app --port <PORT> --host <HOST>
```
