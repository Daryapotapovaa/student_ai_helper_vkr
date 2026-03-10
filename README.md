## Установка и запуск
**1. Клонирование и установка**

```
git clone https://github.com/moevm/bsc_Potapova.git  
cd lsp-proxy-demo
npm install
```

**2. Сборка проекта**
```
npm run compile
```
Или отдельно
```
npm run compile:client    # Клиентская часть
npm run compile:server    # LSP-сервер
```

**3. Запуск в режиме разработки**

Откройте проект в VS Code

Нажмите F5 или перейдите в панель Debug (Ctrl+Shift+D)

Выберите "Run Extension"

Откроется новое окно VS Code с заголовком [Extension Development Host], где будет активен плагин.

## Тестирование функциональности
**Тест 1: Команда Hello World**

В Development Host создайте файл test.py

Нажмите Ctrl+Shift+P

Введите "Hello World"

Появится сообщение 'Hello World from LSP Proxy Demo!' в сплывающем окне, а также на месте курсора вставится комментарий:
```
# Hello World from LSP Proxy!
```
**Тест 2: Проверка LSP соединения**

Откройте Developer Tools (Help → Toggle Developer Tools)

Перейдите на вкладку Console

Должны отображаться логи:
```
LSP Client: Hello! Connected to server
LSP Server: Initialized
```
