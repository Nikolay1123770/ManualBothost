from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import hashlib
import hmac
import os

app = Flask(__name__)
app.secret_key = 'super-secret-key-for-session-12345'

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
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:-apple-system,system-ui,sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:20px}
        .container{max-width:1200px;margin:0 auto}
        .header{text-align:center;color:white;margin-bottom:40px}
        .header h1{font-size:2.5em;margin-bottom:10px;text-shadow:2px 2px 4px rgba(0,0,0,0.3)}
        .box{background:white;padding:40px;border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,0.3);text-align:center;margin-bottom:30px}
        .user{display:flex;align-items:center;justify-content:center;gap:20px;margin-bottom:20px}
        .user img{border-radius:50%;border:3px solid #667eea}
        button{background:linear-gradient(135deg,#f093fb 0%,#f5576c 100%);color:white;border:none;padding:12px 40px;border-radius:30px;cursor:pointer;font-size:16px;font-weight:600}
        button:hover{transform:translateY(-2px)}
        .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:25px}
        .card{background:white;padding:30px;border-radius:20px;box-shadow:0 10px 30px rgba(0,0,0,0.2)}
        .card:hover{transform:translateY(-5px);box-shadow:0 15px 40px rgba(0,0,0,0.3);transition:all 0.3s}
        .card h2{color:#667eea;margin-bottom:15px;font-size:1.5em}
        .card h3{color:#764ba2;margin:20px 0 10px}
        .code{background:#1e1e1e;color:#d4d4d4;padding:15px;border-radius:8px;overflow-x:auto;font-family:monospace;font-size:12px;margin:10px 0;text-align:left;white-space:pre-wrap}
        .step{background:#f5f7fa;padding:15px;margin:10px 0;border-left:4px solid #667eea;border-radius:5px;text-align:left}
        .success{background:#d4edda;padding:15px;margin:10px 0;border-left:4px solid #28a745;border-radius:5px}
        .warning{background:#fff3cd;padding:15px;margin:10px 0;border-left:4px solid #ffc107;border-radius:5px}
        a{color:#667eea;text-decoration:none;font-weight:600}
        a:hover{text-decoration:underline}
        ul{margin-left:20px}
        li{margin:8px 0}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Telegram Bot Мануалы</h1>
            <p>Руководство по созданию ботов на BotHost.ru</p>
        </div>
        {% if user %}
        <div class="box">
            <div class="user">
                {% if user.photo_url %}<img src="{{ user.photo_url }}" width="60" height="60">{% endif %}
                <div>
                    <h2>👋 Привет, {{ user.first_name }}!</h2>
                    <p style="color:#666">@{{ user.username or 'user' }}</p>
                </div>
            </div>
            <form action="/logout" method="post">
                <button type="submit">🚪 Выйти</button>
            </form>
        </div>
        <div class="grid">
            <div class="card">
                <h2>🚀 Простой бот</h2>
                <h3>bot.py</h3>
                <div class="code">from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

BOT_TOKEN = "YOUR_TOKEN"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer(f"Привет!")

async def main():
    await dp.start_polling(bot)

asyncio.run(main())</div>
                <div class="success">✅ python bot.py</div>
            </div>
            <div class="card">
                <h2>⚡ Webhook бот</h2>
                <h3>app.py</h3>
                <div class="code">from flask import Flask, request
import requests

app = Flask(__name__)
TOKEN = "YOUR_TOKEN"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' in data:
        cid = data['message']['chat']['id']
        txt = data['message'].get('text','')
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id":cid,"text":f"Echo: {txt}"})
    return 'OK'</div>
                <div class="warning">⚠️ Откройте /set_webhook</div>
            </div>
            <div class="card">
                <h2>🌐 Деплой BotHost</h2>
                <div class="step">1. GitHub репозиторий<br>2. bothost.ru → Создать бота<br>3. Указать GitHub URL<br>4. Команда: gunicorn bot:app</div>
            </div>
            <div class="card">
                <h2>🔗 Ссылки</h2>
                <ul>
                    <li><a href="https://core.telegram.org/bots/api">Bot API</a></li>
                    <li><a href="https://docs.aiogram.dev/">Aiogram</a></li>
                    <li><a href="https://bothost.ru">BotHost</a></li>
                </ul>
            </div>
        </div>
        {% else %}
        <div class="box">
            <h2 style="margin-bottom:20px">🔐 Вход</h2>
            <p style="color:#666;margin-bottom:30px">Войдите через Telegram</p>
            <script async src="https://telegram.org/js/telegram-widget.js?22" data-telegram-login="{{ bot_username }}" data-size="large" data-auth-url="{{ url_for('auth', _external=True) }}" data-request-access="write"></script>
        </div>
        {% endif %}
    </div>
</body>
</html>'''

def check_auth(data):
    h = data.get('hash')
    d = {k:v for k,v in data.items() if k!='hash'}
    s = '\n'.join([f"{k}={v}" for k,v in sorted(d.items())])
    secret = hashlib.sha256(BOT_TOKEN.encode()).digest()
    return hmac.new(secret,s.encode(),hashlib.sha256).hexdigest() == h

@app.route('/')
def index():
    return render_template_string(HTML, user=session.get('user'), bot_username=BOT_USERNAME)

@app.route('/auth')
def auth():
    d = request.args.to_dict()
    if check_auth(d):
        session['user'] = {'id':d.get('id'),'first_name':d.get('first_name'),'username':d.get('username'),'photo_url':d.get('photo_url')}
        return redirect(url_for('index'))
    return 'Error', 403

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    u = request.get_json()
    if u and 'message' in u:
        cid = u['message']['chat']['id']
        txt = u['message'].get('text','')
        name = u['message']['from'].get('first_name','')
        if txt == '/start':
            m = f"👋 Привет, {name}!\n\n🌐 https://manuals.bothost.ru"
        elif txt == '/help':
            m = "📋 /start /help"
        else:
            m = f"Вы: {txt}"
        requests.post(f'{API_URL}/sendMessage', json={'chat_id':cid,'text':m})
    return 'OK'

@app.route('/set_webhook')
def set_webhook():
    url = request.url_root.rstrip('/') + '/' + BOT_TOKEN
    return requests.post(f'{API_URL}/setWebhook', json={'url':url}).json()

@app.route('/webhook_info')
def webhook_info():
    return requests.get(f'{API_URL}/getWebhookInfo').json()

@app.route('/health')
def health():
    return {'status':'ok'}
