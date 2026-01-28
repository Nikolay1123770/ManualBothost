import os
import hmac
import hashlib
import time
from flask import Flask, render_template_string, request, session, redirect, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8511483464:AAHGBEfL44OggKHyf68ZcSx3PzpjpBbDxF0')
BOT_USERNAME = os.environ.get('BOT_USERNAME', 'wixyez_auth_bot')

# Функция проверки данных от Telegram
def check_telegram_authorization(auth_data):
    check_hash = auth_data.get('hash')
    if not check_hash:
        return False
    
    auth_data_copy = {k: v for k, v in auth_data.items() if k != 'hash'}
    data_check_string = '\n'.join([f'{k}={v}' for k, v in sorted(auth_data_copy.items())])
    
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    if calculated_hash != check_hash:
        return False
    
    auth_date = int(auth_data.get('auth_date', 0))
    if time.time() - auth_date > 86400:
        return False
    
    return True

# HTML шаблон
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📚 DevManuals - Мануалы по разработке</title>
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
            margin-bottom: 30px;
            animation: fadeInDown 0.8s;
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
        
        .user-info {
            background: white;
            padding: 15px 25px;
            border-radius: 15px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            animation: fadeIn 1s;
        }
        
        .user-info .user {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .user-info img {
            width: 50px;
            height: 50px;
            border-radius: 50%;
        }
        
        .user-info h3 {
            color: #667eea;
        }
        
        .logout-btn {
            background: #ff4757;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
        }
        
        .logout-btn:hover {
            background: #ff3838;
            transform: translateY(-2px);
        }
        
        .manuals {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-top: 20px;
        }
        
        .manual-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            transition: all 0.3s;
            animation: fadeInUp 1s;
        }
        
        .manual-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        
        .manual-card h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .manual-content {
            line-height: 1.8;
            color: #333;
        }
        
        .code-block {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            position: relative;
        }
        
        .code-block::before {
            content: 'CODE';
            position: absolute;
            top: 5px;
            right: 10px;
            font-size: 0.7em;
            color: #666;
        }
        
        .step {
            background: #f8f9fa;
            padding: 15px;
            border-left: 4px solid #667eea;
            margin: 15px 0;
            border-radius: 5px;
        }
        
        .step h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .highlight {
            background: #fff3cd;
            padding: 2px 6px;
            border-radius: 3px;
            font-weight: bold;
        }
        
        .warning {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
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
        
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2em;
            }
            
            .manuals {
                grid-template-columns: 1fr;
            }
            
            .user-info {
                flex-direction: column;
                gap: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 DevManuals</h1>
            <p>Профессиональные мануалы по разработке Telegram ботов</p>
        </div>
        
        <div class="user-info">
            <div class="user">
                {% if photo_url %}
                <img src="{{ photo_url }}" alt="Avatar">
                {% else %}
                <img src="https://via.placeholder.com/50" alt="Avatar">
                {% endif %}
                <div>
                    <h3>👋 Привет, {{ first_name }}!</h3>
                    <p style="color: #666;">@{{ username if username else 'пользователь' }}</p>
                </div>
            </div>
            <button class="logout-btn" onclick="logout()">Выйти</button>
        </div>
        
        <div class="manuals">
            <!-- Мануал 1: Mini App -->
            <div class="manual-card">
                <h2>🎯 Создание Mini App и развертывание на BotHost</h2>
                <div class="manual-content">
                    
                    <div class="step">
                        <h3>📝 Шаг 1: Создание Mini App</h3>
                        <p>Создайте файл <span class="highlight">index.html</span> для вашего Mini App:</p>
                    </div>
                    
                    <div class="code-block"><!DOCTYPE html>
&lt;html&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
    &lt;script src="https://telegram.org/js/telegram-web-app.js"&gt;&lt;/script&gt;
    &lt;title&gt;My Mini App&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;Hello, Telegram!&lt;/h1&gt;
    &lt;button id="btn"&gt;Отправить данные&lt;/button&gt;
    
    &lt;script&gt;
        let tg = window.Telegram.WebApp;
        tg.expand();
        
        document.getElementById('btn').addEventListener('click', () => {
            tg.sendData(JSON.stringify({message: 'Hello!'}));
        });
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</div>
                    
                    <div class="step">
                        <h3>🐍 Шаг 2: Создание Flask приложения</h3>
                        <p>Создайте <span class="highlight">main.py</span>:</p>
                    </div>
                    
                    <div class="code-block">from flask import Flask, render_template_string

app = Flask(__name__)

HTML = open('index.html').read()

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)</div>
                    
                    <div class="step">
                        <h3>📦 Шаг 3: Создание requirements.txt</h3>
                    </div>
                    
                    <div class="code-block">Flask==3.0.0
gunicorn==21.2.0</div>
                    
                    <div class="step">
                        <h3>⚙️ Шаг 4: Создание Procfile</h3>
                    </div>
                    
                    <div class="code-block">web: gunicorn main:app</div>
                    
                    <div class="step">
                        <h3>🚀 Шаг 5: Развертывание на BotHost</h3>
                        <ol style="margin-left: 20px; margin-top: 10px;">
                            <li>Зайдите на <a href="https://bothost.net" target="_blank">bothost.net</a></li>
                            <li>Создайте новый проект → выберите "Web App"</li>
                            <li>Загрузите все файлы (main.py, index.html, requirements.txt, Procfile)</li>
                            <li>Нажмите "Deploy"</li>
                            <li>Получите URL вашего приложения</li>
                            <li>Через @BotFather создайте Mini App командой /newapp</li>
                            <li>Вставьте полученный URL</li>
                        </ol>
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ Важно:</strong> BotHost требует файл Procfile для запуска. Убедитесь, что используете gunicorn для production.
                    </div>
                    
                </div>
            </div>
            
            <!-- Мануал 2: Webhook Bot -->
            <div class="manual-card">
                <h2>🤖 Создание Telegram бота на Webhook под BotHost</h2>
                <div class="manual-content">
                    
                    <div class="step">
                        <h3>📝 Шаг 1: Получение токена</h3>
                        <ol style="margin-left: 20px; margin-top: 10px;">
                            <li>Откройте @BotFather в Telegram</li>
                            <li>Отправьте команду /newbot</li>
                            <li>Следуйте инструкциям</li>
                            <li>Сохраните токен</li>
                        </ol>
                    </div>
                    
                    <div class="step">
                        <h3>🐍 Шаг 2: Создание main.py с webhook</h3>
                    </div>
                    
                    <div class="code-block">import os
from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    requests.post(url, json={'chat_id': chat_id, 'text': text})

@app.route('/', methods=['GET'])
def index():
    return 'Bot is running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    
    if 'message' in update:
        chat_id = update['message']['chat']['id']
        text = update['message'].get('text', '')
        
        if text == '/start':
            send_message(chat_id, 'Привет! Я работаю на webhook!')
        else:
            send_message(chat_id, f'Вы написали: {text}')
    
    return 'ok'

@app.route('/set_webhook')
def set_webhook():
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook'
    response = requests.post(url, json={'url': f'{WEBHOOK_URL}/webhook'})
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)</div>
                    
                    <div class="step">
                        <h3>📦 Шаг 3: requirements.txt</h3>
                    </div>
                    
                    <div class="code-block">Flask==3.0.0
requests==2.31.0
gunicorn==21.2.0</div>
                    
                    <div class="step">
                        <h3>⚙️ Шаг 4: Procfile</h3>
                    </div>
                    
                    <div class="code-block">web: gunicorn main:app --bind 0.0.0.0:$PORT</div>
                    
                    <div class="step">
                        <h3>🚀 Шаг 5: Развертывание</h3>
                        <ol style="margin-left: 20px; margin-top: 10px;">
                            <li>Загрузите файлы на BotHost</li>
                            <li>В настройках проекта добавьте переменные окружения:
                                <ul style="margin-left: 20px; margin-top: 5px;">
                                    <li><strong>BOT_TOKEN</strong> - токен от BotFather</li>
                                    <li><strong>WEBHOOK_URL</strong> - URL вашего приложения на BotHost</li>
                                </ul>
                            </li>
                            <li>Задеплойте проект</li>
                            <li>Перейдите по адресу: <span class="highlight">your-app.bothost.net/set_webhook</span></li>
                            <li>Проверьте бота - отправьте /start</li>
                        </ol>
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ Важно:</strong> После каждого передеплоя заново устанавливайте webhook через /set_webhook!
                    </div>
                    
                    <div class="step">
                        <h3>🔧 Полезные команды для проверки</h3>
                    </div>
                    
                    <div class="code-block"># Проверить текущий webhook
https://api.telegram.org/bot{TOKEN}/getWebhookInfo

# Удалить webhook
https://api.telegram.org/bot{TOKEN}/deleteWebhook</div>
                    
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function logout() {
            if(confirm('Вы уверены, что хотите выйти?')) {
                window.location.href = '/logout';
            }
        }
    </script>
</body>
</html>
'''

# Страница авторизации
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔐 Авторизация - DevManuals</title>
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
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .login-container {
            background: white;
            padding: 60px 40px;
            border-radius: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 450px;
            animation: scaleIn 0.5s;
        }
        
        .login-container h1 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 2.5em;
        }
        
        .login-container p {
            color: #666;
            margin-bottom: 40px;
            font-size: 1.1em;
        }
        
        .telegram-login-button {
            display: inline-block;
            margin: 20px auto;
        }
        
        .features {
            margin-top: 40px;
            text-align: left;
        }
        
        .feature {
            display: flex;
            align-items: center;
            gap: 15px;
            margin: 15px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .feature-icon {
            font-size: 2em;
        }
        
        @keyframes scaleIn {
            from {
                transform: scale(0.9);
                opacity: 0;
            }
            to {
                transform: scale(1);
                opacity: 1;
            }
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>📚 DevManuals</h1>
        <p>Для доступа к мануалам войдите через Telegram</p>
        
        <script async src="https://telegram.org/js/telegram-widget.js?22" 
                data-telegram-login="{{ bot_username }}" 
                data-size="large" 
                data-radius="10"
                data-auth-url="{{ auth_url }}" 
                data-request-access="write">
        </script>
        
        <div class="features">
            <div class="feature">
                <div class="feature-icon">🎯</div>
                <div>
                    <strong>Mini App разработка</strong>
                    <p style="font-size: 0.9em; color: #666; margin-top: 5px;">Полный гайд по созданию и деплою</p>
                </div>
            </div>
            
            <div class="feature">
                <div class="feature-icon">🤖</div>
                <div>
                    <strong>Webhook боты</strong>
                    <p style="font-size: 0.9em; color: #666; margin-top: 5px;">Настройка вебхуков на BotHost</p>
                </div>
            </div>
            
            <div class="feature">
                <div class="feature-icon">🚀</div>
                <div>
                    <strong>Production готово</strong>
                    <p style="font-size: 0.9em; color: #666; margin-top: 5px;">Все примеры протестированы</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    
    return render_template_string(
        HTML_TEMPLATE,
        first_name=session.get('first_name', 'Пользователь'),
        username=session.get('username'),
        photo_url=session.get('photo_url')
    )

@app.route('/login')
def login():
    return render_template_string(
        LOGIN_TEMPLATE,
        bot_username=BOT_USERNAME,
        auth_url=request.host_url + 'auth'
    )

@app.route('/auth')
def auth():
    auth_data = request.args.to_dict()
    
    if not check_telegram_authorization(auth_data):
        return 'Authorization failed!', 403
    
    session['user_id'] = auth_data.get('id')
    session['first_name'] = auth_data.get('first_name')
    session['username'] = auth_data.get('username')
    session['photo_url'] = auth_data.get('photo_url')
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=30)
    
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Webhook для бота (опционально)
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = request.get_json()
        
        if 'message' in update:
            chat_id = update['message']['chat']['id']
            text = update['message'].get('text', '')
            
            if text == '/start':
                import requests
                url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
                requests.post(url, json={
                    'chat_id': chat_id,
                    'text': '👋 Привет! Я бот для авторизации на сайте DevManuals.\n\n'
                            'Перейди на сайт и нажми кнопку "Войти через Telegram"!'
                })
        
        return 'ok'
    except:
        return 'ok'

@app.route('/set_webhook')
def set_webhook():
    import requests
    webhook_url = request.host_url + 'webhook'
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook'
    response = requests.post(url, json={'url': webhook_url})
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))