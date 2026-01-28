from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import hashlib
import hmac
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Конфигурация бота
BOT_TOKEN = '8511483464:AAHGBEfL44OggKHyf68ZcSx3PzpjpBbDxF0'
BOT_USERNAME = 'wixyez_auth_bot'
WEBHOOK_URL = ''  # Заполнится автоматически после деплоя

# HTML шаблон сайта
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telegram Bot Мануалы | @wixyez_auth_bot</title>
    <script src="https://telegram.org/js/telegram-widget.js?22"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
            animation: fadeInDown 0.8s ease;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .auth-section {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            margin-bottom: 30px;
            text-align: center;
            animation: fadeIn 1s ease;
        }
        
        .user-info {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .user-info img {
            border-radius: 50%;
            border: 3px solid #667eea;
        }
        
        .user-info h2 {
            color: #333;
        }
        
        .logout-btn {
            background: #e74c3c;
            color: white;
            border: none;
            padding: 10px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        .logout-btn:hover {
            background: #c0392b;
            transform: scale(1.05);
        }
        
        .content-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }
        
        .card {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: all 0.3s;
            animation: fadeInUp 0.8s ease;
        }
        
        .card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        
        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .card-icon {
            font-size: 1.5em;
        }
        
        .card h3 {
            color: #764ba2;
            margin-top: 25px;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .code-block {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 10px;
            overflow-x: auto;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.6;
        }
        
        .code-block code {
            color: #a6e22e;
        }
        
        .step {
            background: #f8f9fa;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #667eea;
            border-radius: 5px;
        }
        
        .step strong {
            color: #667eea;
        }
        
        .warning {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        
        .success {
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        ul {
            margin-left: 20px;
            margin-top: 10px;
        }
        
        li {
            margin: 8px 0;
            line-height: 1.6;
        }
        
        a {
            color: #667eea;
            text-decoration: none;
            font-weight: bold;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2em;
            }
            
            .content-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Telegram Bot Мануалы</h1>
            <p>Полное руководство по созданию и деплою ботов</p>
        </div>
        
        {% if user %}
        <div class="auth-section">
            <div class="user-info">
                {% if user.photo_url %}
                <img src="{{ user.photo_url }}" width="60" height="60" alt="Avatar">
                {% endif %}
                <h2>👋 Привет, {{ user.first_name }}!</h2>
            </div>
            <p style="color: #666; margin-bottom: 15px;">Вы авторизованы как @{{ user.username or 'пользователь' }}</p>
            <form action="/logout" method="post">
                <button type="submit" class="logout-btn">Выйти</button>
            </form>
        </div>
        
        <div class="content-grid">
            <!-- Карточка 1: Простой бот -->
            <div class="card">
                <h2><span class="card-icon">🚀</span> Простой Telegram бот</h2>
                <p>Создайте своего первого бота за 5 минут!</p>
                
                <h3>Шаг 1: Создание бота</h3>
                <div class="step">
                    <strong>1.</strong> Найдите <a href="https://t.me/BotFather" target="_blank">@BotFather</a> в Telegram<br>
                    <strong>2.</strong> Отправьте команду <code>/newbot</code><br>
                    <strong>3.</strong> Придумайте имя и username для бота<br>
                    <strong>4.</strong> Сохраните полученный токен
                </div>
                
                <h3>Шаг 2: Код бота (bot.py)</h3>
                <div class="code-block">
<code>from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

BOT_TOKEN = "YOUR_TOKEN_HERE"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n"
        "Я твой новый бот!"
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "📋 Доступные команды:\n"
        "/start - Начать работу\n"
        "/help - Помощь"
    )

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Вы написали: {message.text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())</code>
                </div>
                
                <h3>Шаг 3: Установка зависимостей</h3>
                <div class="code-block">
pip install aiogram
                </div>
                
                <h3>Шаг 4: Запуск</h3>
                <div class="code-block">
python bot.py
                </div>
                
                <div class="success">
                    ✅ Готово! Бот запущен и отвечает на сообщения
                </div>
            </div>
            
            <!-- Карточка 2: Бот на вебхуке -->
            <div class="card">
                <h2><span class="card-icon">⚡</span> Бот на Webhook</h2>
                <p>Продвинутый способ для продакшена</p>
                
                <h3>Код бота с webhook (app.py)</h3>
                <div class="code-block">
<code>from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "YOUR_TOKEN_HERE"
WEBHOOK_URL = "https://your-domain.com/webhook"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, json=data)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    
    if 'message' in update:
        chat_id = update['message']['chat']['id']
        text = update['message'].get('text', '')
        
        if text == '/start':
            send_message(chat_id, "👋 Привет! Бот на webhook работает!")
        else:
            send_message(chat_id, f"Эхо: {text}")
    
    return 'OK'

@app.route('/set_webhook')
def set_webhook():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    data = {"url": WEBHOOK_URL}
    r = requests.post(url, json=data)
    return r.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)</code>
                </div>
                
                <h3>requirements.txt</h3>
                <div class="code-block">
Flask==3.0.0
requests==2.31.0
gunicorn==21.2.0
                </div>
                
                <div class="warning">
                    ⚠️ После деплоя обязательно откройте /set_webhook для активации вебхука
                </div>
            </div>
            
            <!-- Карточка 3: Mini App -->
            <div class="card">
                <h2><span class="card-icon">📱</span> Telegram Mini App</h2>
                <p>Создайте веб-приложение внутри Telegram</p>
                
                <h3>Структура проекта</h3>
                <div class="code-block">
project/
  ├── bot.py          # Бот
  ├── app.py          # Flask сервер
  ├── templates/
  │   └── miniapp.html
  └── requirements.txt
                </div>
                
                <h3>bot.py - Бот с кнопкой Mini App</h3>
                <div class="code-block">
<code>from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "YOUR_TOKEN"
WEBAPP_URL = "https://your-domain.com/miniapp"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🚀 Открыть Mini App",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    await message.answer(
        "👋 Нажми на кнопку ниже:",
        reply_markup=keyboard
    )</code>
                </div>
                
                <h3>app.py - Flask сервер</h3>
                <div class="code-block">
<code>from flask import Flask, render_template

app = Flask(__name__)

@app.route('/miniapp')
def miniapp():
    return render_template('miniapp.html')

if __name__ == '__main__':
    app.run()</code>
                </div>
                
                <h3>templates/miniapp.html</h3>
                <div class="code-block">
<code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;meta name="viewport" content="width=device-width"&gt;
    &lt;script src="https://telegram.org/js/telegram-web-app.js"&gt;&lt;/script&gt;
    &lt;style&gt;
        body {
            font-family: Arial;
            padding: 20px;
            background: var(--tg-theme-bg-color);
            color: var(--tg-theme-text-color);
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;🎉 Telegram Mini App&lt;/h1&gt;
    &lt;p id="user-info"&gt;&lt;/p&gt;
    &lt;button onclick="sendData()"&gt;Отправить данные боту&lt;/button&gt;
    
    &lt;script&gt;
        let tg = window.Telegram.WebApp;
        tg.expand();
        
        document.getElementById('user-info').innerHTML = 
            `Привет, ${tg.initDataUnsafe.user.first_name}!`;
        
        function sendData() {
            tg.sendData(JSON.stringify({action: 'button_clicked'}));
            tg.close();
        }
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</code>
                </div>
            </div>
            
            <!-- Карточка 4: Деплой на BotHost -->
            <div class="card">
                <h2><span class="card-icon">🌐</span> Деплой на BotHost.ru</h2>
                <p>Пошаговая инструкция по загрузке бота</p>
                
                <h3>Шаг 1: Регистрация</h3>
                <div class="step">
                    <strong>1.</strong> Перейдите на <a href="https://bothost.ru" target="_blank">bothost.ru</a><br>
                    <strong>2.</strong> Зарегистрируйтесь / войдите<br>
                    <strong>3.</strong> Пополните баланс (от 50₽)
                </div>
                
                <h3>Шаг 2: Создание проекта</h3>
                <div class="step">
                    <strong>1.</strong> Нажмите "Создать проект"<br>
                    <strong>2.</strong> Выберите тип: <strong>Python 3.11</strong><br>
                    <strong>3.</strong> Укажите название проекта<br>
                    <strong>4.</strong> Выберите тариф
                </div>
                
                <h3>Шаг 3: Подготовка файлов</h3>
                <div class="code-block">
# requirements.txt
aiogram==3.3.0
aiohttp==3.9.1

# Для Flask проектов добавьте:
Flask==3.0.0
gunicorn==21.2.0
                </div>
                
                <h3>Шаг 4: Загрузка</h3>
                <div class="step">
                    <strong>Через Git:</strong><br>
                    <code>git push bothost master</code><br><br>
                    
                    <strong>Через файловый менеджер:</strong><br>
                    - Откройте раздел "Файлы"<br>
                    - Загрузите bot.py и requirements.txt<br>
                    - Нажмите "Установить зависимости"
                </div>
                
                <h3>Шаг 5: Настройка для Webhook</h3>
                <div class="step">
                    <strong>1.</strong> В настройках проекта включите "Веб-сервер"<br>
                    <strong>2.</strong> Скопируйте URL вашего проекта<br>
                    <strong>3.</strong> Замените в коде WEBHOOK_URL<br>
                    <strong>4.</strong> Откройте https://ваш-домен.com/set_webhook
                </div>
                
                <h3>Шаг 6: Запуск</h3>
                <div class="step">
                    <strong>Для polling бота:</strong><br>
                    Команда запуска: <code>python bot.py</code><br><br>
                    
                    <strong>Для webhook бота:</strong><br>
                    Команда запуска: <code>gunicorn app:app --bind 0.0.0.0:5000</code>
                </div>
                
                <div class="success">
                    ✅ Бот развёрнут! Проверьте работу в Telegram
                </div>
                
                <h3>Полезные команды</h3>
                <div class="code-block">
# Просмотр логов
tail -f logs/app.log

# Перезапуск бота
supervisorctl restart all

# Проверка процессов
supervisorctl status
                </div>
                
                <div class="warning">
                    <strong>⚠️ Важно:</strong>
                    <ul>
                        <li>Не используйте polling и webhook одновременно</li>
                        <li>Храните токены в переменных окружения</li>
                        <li>Регулярно проверяйте логи</li>
                        <li>Для webhook нужен SSL (есть на BotHost)</li>
                    </ul>
                </div>
            </div>
            
            <!-- Карточка 5: Дополнительные возможности -->
            <div class="card">
                <h2><span class="card-icon">⭐</span> Продвинутые фишки</h2>
                
                <h3>🔐 Использование переменных окружения</h3>
                <div class="code-block">
<code>import os

BOT_TOKEN = os.getenv('BOT_TOKEN', 'default_token')
DATABASE_URL = os.getenv('DATABASE_URL')</code>
                </div>
                
                <h3>💾 Подключение базы данных SQLite</h3>
                <div class="code-block">
<code>import sqlite3

conn = sqlite3.connect('bot.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT
    )
''')

# Добавление пользователя
cursor.execute(
    'INSERT OR IGNORE INTO users VALUES (?, ?, ?)',
    (user_id, username, first_name)
)
conn.commit()</code>
                </div>
                
                <h3>📊 Inline кнопки</h3>
                <div class="code-block">
<code>from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Да", callback_data="yes")],
    [InlineKeyboardButton(text="❌ Нет", callback_data="no")]
])

await message.answer("Выберите:", reply_markup=keyboard)

@dp.callback_query()
async def process_callback(callback: types.CallbackQuery):
    if callback.data == "yes":
        await callback.message.answer("Вы выбрали ДА!")
    await callback.answer()</code>
                </div>
                
                <h3>🖼️ Отправка фото</h3>
                <div class="code-block">
<code>from aiogram.types import FSInputFile

photo = FSInputFile("photo.jpg")
await message.answer_photo(
    photo,
    caption="📸 Красивое фото!"
)</code>
                </div>
                
                <h3>⏱️ Отложенные сообщения</h3>
                <div class="code-block">
<code>import asyncio

await message.answer("Сообщение через 5 секунд...")
await asyncio.sleep(5)
await message.answer("⏰ Прошло 5 секунд!")</code>
                </div>
            </div>
            
            <!-- Карточка 6: Полезные ссылки -->
            <div class="card">
                <h2><span class="card-icon">🔗</span> Полезные ссылки</h2>
                
                <h3>📚 Документация</h3>
                <ul>
                    <li><a href="https://core.telegram.org/bots/api" target="_blank">Telegram Bot API</a></li>
                    <li><a href="https://docs.aiogram.dev/" target="_blank">Aiogram 3.x</a></li>
                    <li><a href="https://flask.palletsprojects.com/" target="_blank">Flask</a></li>
                    <li><a href="https://core.telegram.org/bots/webapps" target="_blank">Telegram Mini Apps</a></li>
                </ul>
                
                <h3>🛠️ Хостинг для ботов</h3>
                <ul>
                    <li><a href="https://bothost.ru" target="_blank">BotHost.ru</a> - Специализированный хостинг</li>
                    <li><a href="https://heroku.com" target="_blank">Heroku</a> - Бесплатный вариант</li>
                    <li><a href="https://railway.app" target="_blank">Railway</a> - Простой деплой</li>
                    <li><a href="https://vercel.com" target="_blank">Vercel</a> - Для веб-приложений</li>
                </ul>
                
                <h3>💡 Примеры ботов</h3>
                <ul>
                    <li><a href="https://github.com/aiogram/aiogram" target="_blank">Официальные примеры Aiogram</a></li>
                    <li><a href="https://t.me/botlist" target="_blank">@botlist</a> - Каталог ботов</li>
                </ul>
                
                <div class="success">
                    <strong>🎓 Совет:</strong> Начните с простого бота, потом добавляйте функции постепенно!
                </div>
            </div>
        </div>
        
        {% else %}
        <div class="auth-section">
            <h2 style="margin-bottom: 20px;">🔐 Войдите через Telegram</h2>
            <p style="color: #666; margin-bottom: 20px;">Для доступа к мануалам необходима авторизация</p>
            <script async src="https://telegram.org/js/telegram-widget.js?22" 
                    data-telegram-login="{{ bot_username }}" 
                    data-size="large" 
                    data-auth-url="{{ url_for('auth', _external=True) }}" 
                    data-request-access="write">
            </script>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

# Проверка авторизации Telegram
def check_telegram_authorization(auth_data):
    check_hash = auth_data.get('hash')
    auth_data_copy = {k: v for k, v in auth_data.items() if k != 'hash'}
    data_check_string = '\n'.join([f"{k}={v}" for k, v in sorted(auth_data_copy.items())])
    
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    return calculated_hash == check_hash

# Главная страница
@app.route('/')
def index():
    user = session.get('user')
    return render_template_string(HTML_TEMPLATE, user=user, bot_username=BOT_USERNAME)

# Обработка авторизации
@app.route('/auth')
def auth():
    auth_data = request.args.to_dict()
    
    if check_telegram_authorization(auth_data):
        session['user'] = {
            'id': auth_data.get('id'),
            'first_name': auth_data.get('first_name'),
            'last_name': auth_data.get('last_name'),
            'username': auth_data.get('username'),
            'photo_url': auth_data.get('photo_url'),
            'auth_date': auth_data.get('auth_date')
        }
        return redirect(url_for('index'))
    
    return 'Ошибка авторизации', 403

# Выход
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

# Webhook для бота
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = request.get_json()
    
    if 'message' in update:
        chat_id = update['message']['chat']['id']
        text = update['message'].get('text', '')
        first_name = update['message']['from'].get('first_name', 'друг')
        
        if text == '/start':
            send_message(chat_id, 
                f"👋 Привет, {first_name}!\n\n"
                f"Я бот для авторизации на сайте с мануалами.\n\n"
                f"🌐 Перейди на сайт и авторизуйся через кнопку Telegram!"
            )
        elif text == '/help':
            send_message(chat_id,
                "📋 Доступные команды:\n"
                "/start - Начать работу\n"
                "/help - Помощь\n\n"
                "Используй меня для авторизации на сайте!"
            )
        else:
            send_message(chat_id, f"Вы написали: {text}")
    
    return 'OK', 200

# Отправка сообщения
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    requests.post(url, json=data)

# Установка webhook
@app.route('/set_webhook')
def set_webhook():
    webhook_url = request.url_root + BOT_TOKEN
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    data = {"url": webhook_url}
    response = requests.post(url, json=data)
    return response.json()

# Информация о webhook
@app.route('/webhook_info')
def webhook_info():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    response = requests.get(url)
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
