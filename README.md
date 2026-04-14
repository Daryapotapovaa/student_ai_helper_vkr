## Установка и запуск
**1. Клонирование и установка**

```
git clone https://github.com/moevm/bsc_Potapova.git  
cd student-ai-helper
npm install
```

**2. Сборка проекта**
```
npm run compile
```

**3. Запуск в режиме разработки**

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

Выберете Student AI: Insert Help

 На месте курсора появится комментарий с советом от AI-модели

 ## Отслеживание логов
  Для отслеживания логов об инициализации сервера необходимо в узле разработки расширения в разделе Выходные данные в качестве задачи выбрать Student AI Server. 


