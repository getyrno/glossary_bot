# Telegram Бот для Поиска Определений Терминов

**Посмотреть - https://t.me/glossaryHubBot**
## Описание

Данный проект представляет собой Telegram-бота, который позволяет пользователям искать определения различных терминов на нескольких языках. Бот обрабатывает запросы пользователей, ищет наиболее подходящие определения из внешних источников (таких как Википедия, Викисловарь и DuckDuckGo), а также использует элементы машинного обучения для анализа и классификации терминов.

## Особенности

- **Поиск определений терминов**: Быстрый поиск определений из различных источников.
- **Многоязычная поддержка**: Поддержка русского, английского и китайского языков.
- **Обработка естественного языка**: Использование технологий машинного обучения для улучшения качества ответов.
- **Асинхронная обработка запросов**: Высокая производительность благодаря использованию `asyncio` и `httpx`.
- **Логирование и уведомления**: Подробное логирование работы бота и отправка уведомлений администратору.

## Установка

### Предварительные требования

- Python 3.8 или выше
- Аккаунт Telegram и созданный бот (получите токен у [@BotFather](https://t.me/BotFather))
- Установленный Git для клонирования репозитория
- Рекомендуется использование виртуального окружения (venv, virtualenv)

### Шаги установки

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/getyrno/glossary_bot.git
   cd glossary_bot
   ```

2. **Создайте виртуальное окружение и активируйте его:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/MacOS
   venv\Scripts\activate     # Для Windows
   ```

3. **Установите необходимые зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте переменные окружения:**

   Создайте файл `.env` в корневой директории проекта и добавьте следующие переменные:

   ```env
   TELEGRAM_BOT_TOKEN=ваш_токен_бота
   TELEGRAM_BOT_TOKEN2=токен_бота_для_уведомлений
   TELEGRAM_CHAT_ID=идентификатор_чата_для_уведомлений
   ```

   - `TELEGRAM_BOT_TOKEN`: Токен вашего основного Telegram-бота.
   - `TELEGRAM_BOT_TOKEN2`: Токен бота для отправки уведомлений (опционально).
   - `TELEGRAM_CHAT_ID`: Идентификатор чата или пользователя для отправки уведомлений.

## Запуск

После установки и настройки запустите бота с помощью команды:

```bash
python main.py
```

## Использование

- **/start**: Начать взаимодействие с ботом. Бот приветствует вас и предлагает ввести термин для поиска.
- **/set_language**: Изменить язык интерфейса бота (функция в разработке).
- **Поиск терминов**: Отправьте боту сообщение с интересующим вас термином, и он вернёт его определение.

## Структура проекта

- **main.py**: Основной файл, запускающий бота и обрабатывающий команды.
- **external_sources.py**: Модуль для получения определений из внешних источников.
- **handlers.py**: Обработчики команд и сообщений пользователей.
- **search.py**: Логика поиска и выбора наилучшего определения термина.
- **translator.py**: Функции для перевода текстов между языками.
- **utils.py**: Утилиты и вспомогательные функции (например, создание клавиатур).
- **ml/**: Директория с модулями машинного обучения:
  - **train_model.py**: Обработка терминов и уведомление администратора.
  - **utils.py**: Утилиты для предобработки и векторизации терминов.
  - **notification_bot.py**: Отправка уведомлений администратору.
  - **generate_definition.py**: Генерация определений с помощью моделей GPT-2.
  - **classifier.py**: Классификация контекста терминов.

## Зависимости

- **python-telegram-bot**: Библиотека для создания Telegram-ботов.
- **httpx**: Асинхронный HTTP-клиент для Python.
- **deep-translator**: Библиотека для перевода текстов.
- **transformers**: Модели и токенизаторы от Hugging Face для NLP.
- **dotenv**: Работа с переменными окружения из файла `.env`.
- **psutil**: Получение информации о системе и процессах.

## Переменные окружения

- **TELEGRAM_BOT_TOKEN**: Токен основного бота.
- **TELEGRAM_BOT_TOKEN2**: Токен бота для отправки уведомлений (опционально).
- **TELEGRAM_CHAT_ID**: ID чата для отправки уведомлений администратору.

## Дополнительная настройка

### Машинное обучение

Для использования функций машинного обучения убедитесь, что у вас установлены необходимые модели и пакеты:

- Установите PyTorch, соответствующий вашей системе и версии CUDA (если используется GPU).
- Модели GPT-2 и T5 будут загружены автоматически при первом запуске соответствующих модулей.

### Перевод

Если вы планируете использовать функции перевода, убедитесь, что у вас есть стабильное интернет-соединение, так как некоторые библиотеки обращаются к внешним API.

## Вклад в проект

Если вы хотите внести свой вклад в развитие проекта:

1. Сделайте форк репозитория.
2. Создайте новую ветку: `git checkout -b feature/YourFeature`.
3. Внесите изменения и сделайте коммит: `git commit -m 'Add YourFeature'`.
4. Отправьте изменения в удаленный репозиторий: `git push origin feature/YourFeature`.
5. Создайте Pull Request.

**Коллеги - удачи!**
