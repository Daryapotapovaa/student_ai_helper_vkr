## Установка и запуск
**1. Клонирование и установка**

В корне проекта:
```
git clone https://github.com/moevm/bsc_Potapova.git  
npm install
cd server
npm install
cd ..
```
**2. Создание файла .env**

В корне проекта создайте файл .env:
```
# Для OpenRouter
MODEL_NAME=openai/gpt-oss-20b:free,google/gemma-7b-it:free,anthropic/claude-3-haiku:free,nvidia/nemotron-3-super-120b-a12b:free
API_KEY=sk-or-v1-api_key

# При переключении на локальный сервер, раскомментируйте эту строку:
# API_BASE_URL=http://localhost:1234/v1

# Режим работы плагина: 
# 'advice' - только текстовые подсказки
# 'code' - подсказки с примером исправленного кода
HELP_MODE=code
```

**3. Сборка проекта**
```
npm run compile
```

**4. Запуск в режиме разработки**

Откройте проект в VS Code

Нажмите F5 или перейдите в панель Debug (Ctrl+Shift+D)

Выберите "Run Extension"

Откроется новое окно VS Code с заголовком [Extension Development Host], где будет активен плагин.

## Тестирование функциональности

В Development Host создайте файл test.py

Напишите код с какой-либо ошибкой. Например:

```
def func()
  print('Hello')
```

Нажмите Ctrl+Shift+P

Выберете **Student AI: Insert Help**

 На месте курсора появится комментарий с советом от AI-модели

 ## Отслеживание логов
  Для отслеживания логов об инициализации сервера необходимо в узле разработки расширения в разделе Выходные данные в качестве задачи выбрать Student AI Server. 


