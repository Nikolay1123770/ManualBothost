from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import hashlib
import hmac
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

BOT_TOKEN = '8511483464:AAHGBEfL44OggKHyf68ZcSx3PzpjpBbDxF0'
BOT_USERNAME = 'wixyez_auth_bot'

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Telegram Bot Мануалы | BotHost.ru</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
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
        .header p { font-size: 1.2em; opacity: 0.95; }
        .auth-box {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            animation: fadeIn 1s ease;
            margin-bottom: 30px;
        }
        .user-card {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
        }
        .user-card img { border-radius: 50%; border: 3px solid #667eea; }
        .user-card h2 { color: #333; font-size: 1.8em; }
        .logout-btn {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border: none;
            padding: 12px 40px;
            border-radius: 30px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .logout-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
            gap: 25px;
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
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .card h3 {
            color: #764ba2;
            margin: 25px 0 15px;
            font-size: 1.3em;
        }
        .code {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 10px;
            overflow-x: auto;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.6;
            white-space: pre-wrap;
        }
        .step {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            margin: 15px 0;
            border-left: 5px solid #667eea;
            border-radius: 8px;
        }
        .warning {
            background: #fff3cd;
            border-left: 5px solid #ffc107;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
        }
        .success {
            background: #d4edda;
            border-left: 5px solid #28a745;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
        }
        .info {
            background: #d1ecf1;
            border-left: 5px solid #17a2b8;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
        }
        ul { margin-left: 20px; margin-top: 10px; }
        li { margin: 10px 0; line-height: 1.8; }
        a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
        }
        a:hover { color: #764ba2; text-decoration: underline; }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @media (max-width: 768px) {
            .header h1 { font-size: 2em; }
            .grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Telegram Bot Мануалы</h1>
            <p>Полное руководство по созданию и деплою на BotHost.ru</p>
        </div>
        
        {% if user %}
        <div class="auth-box">
            <div class="user-card">
                {% if user.photo_url %}
                <img src="{{ user.photo_url }}" width="70" height="70" alt="Avatar">
                {% endif %}
                <div>
                    <h2>👋 Привет, {{ user.first_name }}!</h2>
                    <p style="color: #666;">@{{ user.username or 'пользователь' }}</p>
                </div>
            </div>
            <form action="/logout" method="post">
                <button type="submit" class="logout-btn">🚪 Выйти</button>
            </form>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>🚀 Простой бот на Polling</h2>
                <p>Идеально для начинающих</p>
                
                <h3>📝 Создание бота</h3>
                <div class="step">
                    1. Найдите @BotFather в Telegram<br>
                    2. Команда: /newbot<br>
                    3. Придумайте имя и username<br>
                    4. Скопируйте токен
                </div>
                
                <h3>💻 Код (bot.py)</h3>
                <div class="code">from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

BOT_TOKEN = "ВАШ_ТОКЕН"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\\n"
        "Я работаю на BotHost!"
    )

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Вы: {message.text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())</div>
                
                <h3>📦 requirements.txt</h3>
                <div class="code">aiogram==3.3.0
aiohttp==3.9.1</div>
                
                <div class="success">✅ Готово! Простой и надежный вариант</div>
            </div>
            
            <div class="card">
                <h2>⚡ Бот на Webhook</h2>
                <p>Для продакшена</p>
                
                <h3>💻 Код (app.py)</h3>
                <div class="code">from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "ВАШ_ТОКЕН"
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    requests.post(f"{API}/sendMessage", 
        json={"chat_id": chat_id, "text": text})

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = request.get_json()
    
    if 'message' in update:
        chat_id = update['message']['chat']['id']
        text = update['message'].get('text', '')
        
        if text == '/start':
            send_message(chat_id, "👋 Webhook бот!")
        else:
            send_message(chat_id, f"Эхо: {text}")
    
    return 'OK'

@app.route('/set_webhook')
def set_webhook():
    webhook_url = request.url_root + BOT_TOKEN
    r = requests.post(f"{API}/setWebhook", 
        json={"url": webhook_url})
    return r.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)</div>
                
                <h3>📦 requirements.txt</h3>
                <div class="code">Flask==3.0.0
requests==2.31.0
gunicorn==21.2.0</div>
                
                <div class="warning">⚠️ После деплоя откройте: /set_webhook</div>
            </div>
            
            <div class="card">
                <h2>📱 Telegram Mini App</h2>
                <p>Веб-приложение в Telegram</p>
                
                <h3>🤖 Бот с кнопкой Mini App</h3>
                <div class="code">from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    WebAppInfo, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)

BOT_TOKEN = "ВАШ_ТОКЕН"
WEBAPP_URL = "https://ваш-домен.bothost.ru/miniapp"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="🚀 Открыть Mini App",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]]
    )
    await message.answer(
        "👇 Нажмите кнопку:",
        reply_markup=keyboard
    )</div>
                
                <h3>🌐 HTML для Mini App</h3>
                <div class="code">&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;script src="https://telegram.org/js/telegram-web-app.js"&gt;&lt;/script&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;🎉 Mini App&lt;/h1&gt;
    &lt;p id="user"&gt;&lt;/p&gt;
    &lt;button onclick="send()"&gt;Отправить&lt;/button&gt;
    
    &lt;script&gt;
        let tg = window.Telegram.WebApp;
        tg.expand();
        
        document.getElementById('user').innerHTML = 
            `Привет, ${tg.initDataUnsafe.user.first_name}!`;
        
        function send() {
            tg.sendData('button_clicked');
            tg.close();
        }
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</div>
            </div>
            
            <div class="card">
                <h2>🌐 Деплой на BotHost</h2>
                
                <h3>1️⃣ Подготовка</h3>
                <div class="step">
                    • Создайте репозиторий на GitHub<br>
                    • Загрузите bot.py и requirements.txt<br>
                    • Скопируйте URL репозитория
                </div>
                
                <h3>2️⃣ Создание бота</h3>
                <div class="step">
                    • Войдите на bothost.ru<br>
                    • "Создать бота" → Python 3.11<br>
                    • Вставьте URL репозитория
                </div>
                
                <h3>3️⃣ Настройка</h3>
                <div class="info">
                    <strong>Для Polling:</strong><br>
                    Команда: python bot.py<br><br>
                    
                    <strong>Для Webhook:</strong><br>
                    1. Включите "Веб-сервер"<br>
                    2. Команда: gunicorn bot:app --bind 0.0.0.0:5000<br>
                    3. Откройте: /set_webhook
                </div>
                
                <h3>4️⃣ Переменные окружения</h3>
                <div class="code">BOT_TOKEN=ваш_токен
ADMIN_ID=123456789</div>
                
                <div class="success">✅ Бот запущен!</div>
            </div>
            
            <div class="card">
                <h2>⭐ Продвинутые фишки</h2>
                
                <h3>🔐 Inline кнопки</h3>
                <div class="code">from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)

kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="✅ Да", 
        callback_data="yes"
    )],
    [InlineKeyboardButton(
        text="❌ Нет", 
        callback_data="no"
    )]
])

await message.answer("Выберите:", reply_markup=kb)</div>
                
                <h3>📊 Обработка callback</h3>
                <div class="code">@dp.callback_query()
async def process(callback: types.CallbackQuery):
    if callback.data == "yes":
        await callback.message.answer("Вы выбрали ДА!")
    await callback.answer()</div>
                
                <h3>🖼️ Отправка фото</h3>
                <div class="code">from aiogram.types import FSInputFile

photo = FSInputFile("image.jpg")
await message.answer_photo(
    photo, 
    caption="📸 Фото"
)</div>
            </div>
            
            <div class="card">
                <h2>🔗 Полезные ссылки</h2>
                
                <h3>📚 Документация</h3>
                <ul>
                    <li><a href="https://core.telegram.org/bots/api" target="_blank">Telegram Bot API</a></li>
                    <li><a href="https://docs.aiogram.dev/" target="_blank">Aiogram 3.x</a></li>
                    <li><a href="https://flask.palletsprojects.com/" target="_blank">Flask Docs</a></li>
                </ul>
                
                <h3>🛠️ Хостинг</h3>
                <ul>
                    <li><a href="https://bothost.ru" target="_blank">BotHost.ru</a></li>
                    <li><a href="https://railway.app" target="_blank">Railway</a></li>
                    <li><a href="https://render.com" target="_blank">Render</a></li>
                </ul>
                
                <h3>💡 Сообщества</h3>
                <ul>
                    <li><a href="https://t.me/aiogram_live" target="_blank">@aiogram_live</a></li>
                    <li><a href="https://t.me/bothost_ru" target="_blank">@bothost_ru</a></li>
                </ul>
            </div>
        </div>
        
        {% else %}
        <div class="auth-box">
            <h2 style="margin-bottom: 20px; color: #333;">🔐 Авторизация</h2>
            <p style="color: #666; margin-bottom: 30px; font-size: 1.1em;">
                Войдите через Telegram для доступа к мануалам
            </p>
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
</html>'''

def check_telegram_auth(auth_data):
    check_hash = auth_data.get('hash')
    auth_data_copy = {k: v for k, v in auth_data.items() if k != 'hash'}
    data_check_string = '\n'.join([f"{k}={v}" for k, v in sorted(auth_data_copy.items())])
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return calculated_hash == check_hash

@app.route('/')
def index():
    user = session.get('user')
    return render_template_string(HTML_TEMPLATE, user=user, bot_username=BOT_USERNAME)

@app.route('/auth')
def auth():
    auth_data = request.args.to_dict()
    if check_telegram_auth(auth_data):
        session['user'] = {
            'id': auth_data.get('id'),
            'first_name': auth_data.get('first_name'),
            'last_name': auth_data.get('last_name'),
            'username': auth_data.get('username'),
            'photo_url': auth_data.get('photo_url')
        }
        return redirect(url_for('index'))
    return 'Auth Error', 403

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

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
                "Я бот для авторизации на сайте.\n\n"
                "🌐 Сайт: https://manuals.bothost.ru"
            )
        elif text == '/help':
            send_message(chat_id,
                "📋 Команды:\n"
                "/start - Начать\n"
                "/help - Помощь"
            )
        else:
            send_message(chat_id, f"Вы написали: {text}")
    return 'OK', 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

@app.route('/set_webhook')
def set_webhook():
    webhook_url = request.url_root.rstrip('/') + '/' + BOT_TOKEN
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    response = requests.post(url, json={"url": webhook_url})
    return response.json()

@app.route('/webhook_info')
def webhook_info():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    response = requests.get(url)
    return response.json()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
