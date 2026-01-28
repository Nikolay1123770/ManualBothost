from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import hashlib
import hmac
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-12345')

BOT_TOKEN = '8511483464:AAHGBEfL44OggKHyf68ZcSx3PzpjpBbDxF0'
BOT_USERNAME = 'wixyez_auth_bot'
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

HTML = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Telegram Bot Мануалы</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, system-ui, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; color: white; margin-bottom: 40px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .box {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            margin-bottom: 30px;
        }
        .user { display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 20px; }
        .user img { border-radius: 50%; border: 3px solid #667eea; }
        button {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border: none;
            padding: 12px 40px;
            border-radius: 30px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
        }
        button:hover { transform: translateY(-2px); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 25px; }
        .card {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .card:hover { transform: translateY(-5px); box-shadow: 0 15px 40px rgba(0,0,0,0.3); transition: all 0.3s; }
        .card h2 { color: #667eea; margin-bottom: 15px; font-size: 1.5em; }
        .card h3 { color: #764ba2; margin: 20px 0 10px; }
        .code {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: monospace;
            font-size: 12px;
            margin: 10px 0;
            text-align: left;
        }
        .step {
            background: #f5f7fa;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #667eea;
            border-radius: 5px;
            text-align: left;
        }
        .success { background: #d4edda; padding: 15px; margin: 10px 0; border-left: 4px solid #28a745; border-radius: 5px; }
        .warning { background: #fff3cd; padding: 15px; margin: 10px 0; border-left: 4px solid #ffc107; border-radius: 5px; }
        a { color: #667eea; text-decoration: none; font-weight: 600; }
        a:hover { text-decoration: underline; }
        ul { margin-left: 20px; }
        li { margin: 8px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Telegram Bot Мануалы</h1>
            <p>Полное руководство по созданию ботов на BotHost.ru</p>
        </div>
        
        {% if user %}
        <div class="box">
            <div class="user">
                {% if user.photo_url %}<img src="{{ user.photo_url }}" width="60" height="60">{% endif %}
                <div>
                    <h2>👋 Привет, {{ user.first_name }}!</h2>
                    <p style="color:#666">@{{ user.username or 'пользователь' }}</p>
                </div>
            </div>
            <form action="/logout" method="post">
                <button type="submit">🚪 Выйти</button>
            </form>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>🚀 Простой бот (Polling)</h2>
                <p>Для начинающих разработчиков</p>
                <h3>bot.py</h3>
                <div class="code">from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

BOT_TOKEN = "YOUR_TOKEN"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer(f"Привет, {msg.from_user.first_name}!")

@dp.message()
async def echo(msg: types.Message):
    await msg.answer(f"Вы: {msg.text}")

async def main():
    await dp.start_polling(bot)

asyncio.run(main())</div>
                <h3>requirements.txt</h3>
                <div class="code">aiogram==3.3.0</div>
                <div class="success">✅ Команда запуска: python bot.py</div>
            </div>
            
            <div class="card">
                <h2>⚡ Webhook бот (Flask)</h2>
                <p>Для продакшена и высоких нагрузок</p>
                <h3>app.py</h3>
                <div class="code">from flask import Flask, request
import requests

app = Flask(__name__)
TOKEN = "YOUR_TOKEN"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": f"Эхо: {text}"}
        )
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)</div>
                <h3>requirements.txt</h3>
                <div class="code">Flask==3.0.0
requests==2.31.0
gunicorn==21.2.0</div>
                <div class="warning">⚠️ После деплоя откройте: /set_webhook</div>
            </div>
            
            <div class="card">
                <h2>📱 Mini App</h2>
                <p>Веб-приложение внутри Telegram</p>
                <h3>Бот с кнопкой Mini App</h3>
                <div class="code">from aiogram.types import WebAppInfo
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

@dp.message(Command("start"))
async def start(msg: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="🚀 Открыть",
            web_app=WebAppInfo(url="https://your-domain.com")
        )
    ]])
    await msg.answer("Нажмите:", reply_markup=kb)</div>
                <h3>Mini App HTML</h3>
                <div class="code">&lt;script src="https://telegram.org/js/telegram-web-app.js"&gt;&lt;/script&gt;
&lt;script&gt;
let tg = window.Telegram.WebApp;
tg.expand();
alert('Привет, ' + tg.initDataUnsafe.user.first_name);
&lt;/script&gt;</div>
            </div>
            
            <div class="card">
                <h2>🌐 Деплой на BotHost</h2>
                <div class="step">
                    <strong>1.</strong> Зарегистрируйтесь на <a href="https://bothost.ru">bothost.ru</a><br><br>
                    <strong>2.</strong> Создайте репозиторий на GitHub<br><br>
                    <strong>3.</strong> Загрузите bot.py и requirements.txt<br><br>
                    <strong>4.</strong> На BotHost: "Создать бота" → укажите GitHub URL<br><br>
                    <strong>5.</strong> Команда запуска:<br>
                    • Polling: <code>python bot.py</code><br>
                    • Webhook: <code>python bot.py</code> + включите веб-сервер<br><br>
                    <strong>6.</strong> Для webhook откройте: /set_webhook
                </div>
                <div class="success">✅ Готово! Бот работает 24/7</div>
            </div>
            
            <div class="card">
                <h2>⭐ Продвинутые фишки</h2>
                <h3>Inline кнопки</h3>
                <div class="code">from aiogram.types import InlineKeyboardMarkup as IKM
from aiogram.types import InlineKeyboardButton as IKB

kb = IKM(inline_keyboard=[
    [IKB(text="✅ Да", callback_data="yes")],
    [IKB(text="❌ Нет", callback_data="no")]
])
await msg.answer("Выберите:", reply_markup=kb)

@dp.callback_query()
async def cb(callback: types.CallbackQuery):
    await callback.answer(f"Вы выбрали: {callback.data}")</div>
                <h3>Отправка фото</h3>
                <div class="code">from aiogram.types import FSInputFile
photo = FSInputFile("image.jpg")
await msg.answer_photo(photo, caption="📸 Фото")</div>
            </div>
            
            <div class="card">
                <h2>🔗 Полезные ссылки</h2>
                <h3>📚 Документация</h3>
                <ul>
                    <li><a href="https://core.telegram.org/bots/api" target="_blank">Telegram Bot API</a></li>
                    <li><a href="https://docs.aiogram.dev/" target="_blank">Aiogram 3.x</a></li>
                    <li><a href="https://flask.palletsprojects.com/" target="_blank">Flask</a></li>
                    <li><a href="https://core.telegram.org/bots/webapps" target="_blank">Mini Apps</a></li>
                </ul>
                <h3>🛠️ Хостинг</h3>
                <ul>
                    <li><a href="https://bothost.ru" target="_blank">BotHost.ru</a></li>
                    <li><a href="https://railway.app" target="_blank">Railway</a></li>
                    <li><a href="https://render.com" target="_blank">Render</a></li>
                </ul>
                <h3>💬 Сообщества</h3>
                <ul>
                    <li><a href="https://t.me/aiogram_live" target="_blank">@aiogram_live</a></li>
                    <li><a href="https://t.me/bothost_ru" target="_blank">@bothost_ru</a></li>
                </ul>
            </div>
        </div>
        
        {% else %}
        <div class="box">
            <h2 style="margin-bottom: 20px;">🔐 Авторизация</h2>
            <p style="color: #666; margin-bottom: 30px;">Войдите через Telegram для доступа к мануалам</p>
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

def check_auth(data):
    check_hash = data.get('hash')
    data_copy = {k: v for k, v in data.items() if k != 'hash'}
    data_string = '\n'.join([f"{k}={v}" for k, v in sorted(data_copy.items())])
    secret = hashlib.sha256(BOT_TOKEN.encode()).digest()
    calc_hash = hmac.new(secret, data_string.encode(), hashlib.sha256).hexdigest()
    return calc_hash == check_hash

@app.route('/')
def index():
    return render_template_string(HTML, user=session.get('user'), bot_username=BOT_USERNAME)

@app.route('/auth')
def auth():
    data = request.args.to_dict()
    if check_auth(data):
        session['user'] = {
            'id': data.get('id'),
            'first_name': data.get('first_name'),
            'username': data.get('username'),
            'photo_url': data.get('photo_url')
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
    if update and 'message' in update:
        chat_id = update['message']['chat']['id']
        text = update['message'].get('text', '')
        name = update['message']['from'].get('first_name', 'друг')
        
        if text == '/start':
            msg = f"👋 Привет, {name}!\n\n🌐 Сайт: https://manuals.bothost.ru"
        elif text == '/help':
            msg = "📋 Команды:\n/start - Начать\n/help - Помощь"
        else:
            msg = f"Вы написали: {text}"
        
        requests.post(f'{API_URL}/sendMessage', json={'chat_id': chat_id, 'text': msg})
    return 'OK'

@app.route('/set_webhook')
def set_webhook():
    url = request.url_root.rstrip('/') + '/' + BOT_TOKEN
    r = requests.post(f'{API_URL}/setWebhook', json={'url': url})
    return r.json()

@app.route('/webhook_info')
def webhook_info():
    return requests.get(f'{API_URL}/getWebhookInfo').json()

@app.route('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
