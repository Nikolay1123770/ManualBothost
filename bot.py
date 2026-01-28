from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import hashlib
import hmac
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Конфигурация
BOT_TOKEN = '8511483464:AAHGBEfL44OggKHyf68ZcSx3PzpjpBbDxF0'
BOT_USERNAME = 'wixyez_auth_bot'

# HTML шаблон
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Telegram Bot Мануалы | BotHost Guide</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
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
            opacity: 0.95;
        }
        
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
        
        .user-card img {
            border-radius: 50%;
            border: 3px solid #667eea;
        }
        
        .user-card h2 {
            color: #333;
            font-size: 1.8em;
        }
        
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
        }
        
        .code .keyword { color: #569cd6; }
        .code .string { color: #ce9178; }
        .code .function { color: #dcdcaa; }
        .code .comment { color: #6a9955; }
        
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
        
        ul {
            margin-left: 20px;
            margin-top: 10px;
        }
        
        li {
            margin: 10px 0;
            line-height: 1.8;
        }
        
        a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        a:hover {
            color: #764ba2;
            text-decoration: underline;
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
            <!-- Карточка 1: Простой бот (Polling) -->
            <div class="card">
                <h2>🚀 Простой бот на Polling</h2>
                <p>Идеально подходит для начинающих и небольших проектов</p>
                
                <h3>📝 Шаг 1: Создание бота</h3>
                <div class="step">
                    <strong>1.</strong> Найдите <a href="https://t.me/BotFather">@BotFather</a><br>
                    <strong>2.</strong> Команда: <code>/newbot</code><br>
                    <strong>3.</strong> Придумайте имя и username<br>
                    <strong>4.</strong> Скопируйте токен
                </div>
                
                <h3>💻 Шаг 2: Код (bot.py)</h3>
                <div class="code">
<span class="keyword">from</span> aiogram <span class="keyword">import</span> Bot, Dispatcher, types
<span class="keyword">from</span> aiogram.filters <span class="keyword">import</span> Command
<span class="keyword">import</span> asyncio

BOT_TOKEN = <span class="string">"ВАШ_ТОКЕН"</span>
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

<span class="comment"># Команда /start</span>
@dp.message(Command(<span class="string">"start"</span>))
<span class="keyword">async def</span> <span class="function">cmd_start</span>(message: types.Message):
    <span class="keyword">await</span> message.answer(
        <span class="string">f"👋 Привет, {message.from_user.first_name}!\n"</span>
        <span class="string">"Я работаю на BotHost!"</span>
    )

<span class="comment"># Эхо</span>
@dp.message()
<span class="keyword">async def</span> <span class="function">echo</span>(message: types.Message):
    <span class="keyword">await</span> message.answer(<span class="string">f"Вы: {message.text}"</span>)

<span class="keyword">async def</span> <span class="function">main</span>():
    <span class="keyword">await</span> dp.start_polling(bot)

<span class="keyword">if</span> __name__ == <span class="string">"__main__"</span>:
    asyncio.run(main())
                </div>
                
                <h3>📦 requirements.txt</h3>
                <div class="code">
aiogram==3.3.0
aiohttp==3.9.1
                </div>
                
                <div class="success">
                    ✅ <strong>Готово!</strong> Простой и надежный вариант
                </div>
            </div>
            
            <!-- Карточка 2: Бот на Webhook -->
            <div class="card">
                <h2>⚡ Бот на Webhook</h2>
                <p>Для продакшена и высоких нагрузок</p>
                
                <h3>💻 Код (app.py)</h3>
                <div class="code">
<span class="keyword">from</span> flask <span class="keyword">import</span> Flask, request
<span class="keyword">import</span> requests

app = Flask(__name__)

BOT_TOKEN = <span class="string">"ВАШ_ТОКЕН"</span>
API_URL = <span class="string">f"https://api.telegram.org/bot{BOT_TOKEN}"</span>

<span class="keyword">def</span> <span class="function">send_message</span>(chat_id, text):
    url = <span class="string">f"{API_URL}/sendMessage"</span>
    requests.post(url, json={
        <span class="string">"chat_id"</span>: chat_id,
        <span class="string">"text"</span>: text
    })

@app.route(<span class="string">f'/{BOT_TOKEN}'</span>, methods=[<span class="string">'POST'</span>])
<span class="keyword">def</span> <span class="function">webhook</span>():
    update = request.get_json()
    
    <span class="keyword">if</span> <span class="string">'message'</span> <span class="keyword">in</span> update:
        chat_id = update[<span class="string">'message'</span>][<span class="string">'chat'</span>][<span class="string">'id'</span>]
        text = update[<span class="string">'message'</span>].get(<span class="string">'text'</span>, <span class="string">''</span>)
        
        <span class="keyword">if</span> text == <span class="string">'/start'</span>:
            send_message(chat_id, <span class="string">"👋 Webhook бот запущен!"</span>)
        <span class="keyword">else</span>:
            send_message(chat_id, <span class="string">f"Эхо: {text}"</span>)
    
    <span class="keyword">return</span> <span class="string">'OK'</span>

@app.route(<span class="string">'/set_webhook'</span>)
<span class="keyword">def</span> <span class="function">set_webhook</span>():
    webhook_url = request.url_root + BOT_TOKEN
    url = <span class="string">f"{API_URL}/setWebhook"</span>
    r = requests.post(url, json={<span class="string">"url"</span>: webhook_url})
    <span class="keyword">return</span> r.json()

<span class="keyword">if</span> __name__ == <span class="string">'__main__'</span>:
    app.run(host=<span class="string">'0.0.0.0'</span>, port=5000)
                </div>
                
                <h3>📦 requirements.txt</h3>
                <div class="code">
Flask==3.0.0
requests==2.31.0
gunicorn==21.2.0
                </div>
                
                <div class="warning">
                    ⚠️ После деплоя откройте: <code>https://ваш-домен.bothost.ru/set_webhook</code>
                </div>
            </div>
            
            <!-- Карточка 3: Mini App -->
            <div class="card">
                <h2>📱 Telegram Mini App</h2>
                <p>Веб-приложение внутри Telegram</p>
                
                <h3>🤖 bot.py (с кнопкой Mini App)</h3>
                <div class="code">
<span class="keyword">from</span> aiogram <span class="keyword">import</span> Bot, Dispatcher, types
<span class="keyword">from</span> aiogram.filters <span class="keyword">import</span> Command
<span class="keyword">from</span> aiogram.types <span class="keyword">import</span> WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = <span class="string">"ВАШ_ТОКЕН"</span>
WEBAPP_URL = <span class="string">"https://ваш-домен.bothost.ru/miniapp"</span>

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(<span class="string">"start"</span>))
<span class="keyword">async def</span> <span class="function">start</span>(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text=<span class="string">"🚀 Открыть Mini App"</span>,
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]])
    <span class="keyword">await</span> message.answer(
        <span class="string">"👇 Нажмите кнопку:"</span>,
        reply_markup=keyboard
    )
                </div>
                
                <h3>🌐 templates/miniapp.html</h3>
                <div class="code">
&lt;!DOCTYPE html&gt;
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
        button {
            background: var(--tg-theme-button-color);
            color: var(--tg-theme-button-text-color);
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;🎉 Mini App&lt;/h1&gt;
    &lt;p id="user"&gt;&lt;/p&gt;
    &lt;button onclick="sendData()"&gt;Отправить&lt;/button&gt;
    
    &lt;script&gt;
        let tg = window.Telegram.WebApp;
        tg.expand();
        
        document.getElementById('user').innerHTML = 
            `Привет, ${tg.initDataUnsafe.user.first_name}!`;
        
        function sendData() {
            tg.sendData(JSON.stringify({action: 'click'}));
            tg.close();
        }
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;
                </div>
            </div>
            
            <!-- Карточка 4: Деплой на BotHost -->
            <div class="card">
                <h2>🌐 Деплой на BotHost.ru</h2>
                <p>Пошаговая инструкция</p>
                
                <h3>1️⃣ Регистрация</h3>
                <div class="step">
                    • Перейдите на <a href="https://bothost.ru">bothost.ru</a><br>
                    • Зарегистрируйтесь или войдите<br>
                    • Пополните баланс (от 50₽ в месяц)
                </div>
                
                <h3>2️⃣ Создание проекта</h3>
                <div class="step">
                    • Нажмите <strong>"Создать бота"</strong><br>
                    • Тип: <strong>Python 3.11</strong><br>
                    • Укажите название<br>
                    • Выберите тариф
                </div>
                
                <h3>3️⃣ Загрузка через Git</h3>
                <div class="code">
<span class="comment"># Создайте репозиторий на GitHub</span>
git init
git add .
git commit -m <span class="string">"Initial commit"</span>
git remote add origin https://github.com/ВАШ_ЛОГИН/ВАШ_РЕПО.git
git push -u origin master

<span class="comment"># В BotHost укажите ссылку на репозиторий</span>
                </div>
                
                <h3>4️⃣ Настройка запуска</h3>
                <div class="info">
                    <strong>Для Polling бота:</strong><br>
                    Команда: <code>python bot.py</code><br><br>
                    
                    <strong>Для Webhook бота:</strong><br>
                    1. Включите "Веб-сервер" в настройках<br>
                    2. Команда: <code>gunicorn app:app --bind 0.0.0.0:5000</code><br>
                    3. После запуска откройте: <code>/set_webhook</code>
                </div>
                
                <h3>5️⃣ Полезные команды</h3>
                <div class="code">
<span class="comment"># Просмотр логов</span>
tail -f logs/bot.log

<span class="comment"># Перезапуск</span>
supervisorctl restart all

<span class="comment"># Статус</span>
supervisorctl status
                </div>
                
                <div class="success">
                    ✅ <strong>Бот запущен!</strong> Проверьте в Telegram
                </div>
                
                <div class="warning">
                    <strong>⚠️ Важно:</strong><br>
                    • Не используйте polling и webhook вместе<br>
                    • Храните токены в переменных окружения<br>
                    • Проверяйте логи регулярно
                </div>
            </div>
            
            <!-- Карточка 5: Продвинутые фишки -->
            <div class="card">
                <h2>⭐ Продвинутые возможности</h2>
                
                <h3>🔐 Переменные окружения</h3>
                <div class="code">
<span class="keyword">import</span> os

BOT_TOKEN = os.getenv(<span class="string">'BOT_TOKEN'</span>, <span class="string">'default'</span>)
DATABASE_URL = os.getenv(<span class="string">'DATABASE_URL'</span>)
                </div>
                
                <h3>💾 База данных SQLite</h3>
                <div class="code">
<span class="keyword">import</span> sqlite3

conn = sqlite3.connect(<span class="string">'bot.db'</span>)
cursor = conn.cursor()

<span class="comment"># Создание таблицы</span>
cursor.execute(<span class="string">'''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT
    )
'''</span>)

<span class="comment"># Добавление пользователя</span>
cursor.execute(
    <span class="string">'INSERT OR IGNORE INTO users VALUES (?, ?, ?)'</span>,
    (user_id, username, first_name)
)
conn.commit()
                </div>
                
                <h3>📊 Inline кнопки</h3>
                <div class="code">
<span class="keyword">from</span> aiogram.types <span class="keyword">import</span> InlineKeyboardMarkup, InlineKeyboardButton

kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=<span class="string">"✅ Да"</span>, callback_data=<span class="string">"yes"</span>)],
    [InlineKeyboardButton(text=<span class="string">"❌ Нет"</span>, callback_data=<span class="string">"no"</span>)]
])

<span class="keyword">await</span> message.answer(<span class="string">"Выберите:"</span>, reply_markup=kb)

@dp.callback_query()
<span class="keyword">async def</span> <span class="function">process</span>(callback: types.CallbackQuery):
    <span class="keyword">await</span> callback.message.answer(<span class="string">f"Вы выбрали: {callback.data}"</span>)
    <span class="keyword">await</span> callback.answer()
                </div>
                
                <h3>🖼️ Отправка файлов</h3>
                <div class="code">
<span class="keyword">from</span> aiogram.types <span class="keyword">import</span> FSInputFile

<span class="comment"># Фото</span>
photo = FSInputFile(<span class="string">"image.jpg"</span>)
<span class="keyword">await</span> message.answer_photo(photo, caption=<span class="string">"📸 Фото"</span>)

<span class="comment"># Документ</span>
doc = FSInputFile(<span class="string">"file.pdf"</span>)
<span class="keyword">await</span> message.answer_document(doc)
                </div>
            </div>
            
            <!-- Карточка 6: Полезные ссылки -->
            <div class="card">
                <h2>🔗 Полезные ресурсы</h2>
                
                <h3>📚 Документация</h3>
                <ul>
                    <li><a href="https://core.telegram.org/bots/api">Telegram Bot API</a></li>
                    <li><a href="https://docs.aiogram.dev/">Aiogram 3.x Docs</a></li>
                    <li><a href="https://flask.palletsprojects.com/">Flask Documentation</a></li>
                    <li><a href="https://core.telegram.org/bots/webapps">Telegram Mini Apps API</a></li>
                </ul>
                
                <h3>🛠️ Хостинг</h3>
                <ul>
                    <li><a href="https://bothost.ru">BotHost.ru</a> — Специализированный</li>
                    <li><a href="https://heroku.com">Heroku</a> — Бесплатный tier</li>
                    <li><a href="https://railway.app">Railway</a> — Простой деплой</li>
                    <li><a href="https://render.com">Render</a> — Современный</li>
                </ul>
                
                <h3>💡 Сообщества</h3>
                <ul>
                    <li><a href="https://t.me/aiogram_live">@aiogram_live</a> — Чат Aiogram</li>
                    <li><a href="https://t.me/bothost_ru">@bothost_ru</a> — Поддержка BotHost</li>
                </ul>
                
                <div class="info">
                    <strong>💡 Совет:</strong> Начните с простого polling бота, затем переходите на webhook и Mini Apps!
                </div>
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
</html>
'''

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
                "🌐 Перейди на сайт: https://manuals.bothost.ru"
            )
        elif text == '/help':
            send_message(chat_id,
                "📋 Команды:\n"
                "/start — Начать\n"
                "/help — Помощь\n\n"
                "Используй меня для входа на сайт!"
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
    app.run(host='0.0.0.0', port=5000)
