# Student AI Helper

Плагин для Visual Studio Code, обеспечивающий умное автодополнение кода с педагогическими подсказками для студентов, изучающих Python. Реализован на базе протокола LSP (Language Server Protocol) с интеграцией языковых моделей через OpenAI-совместимый API.

## Возможности

- **Автоматическая проверка кода** при сохранении файла 
- **Педагогические объяснения ошибок** на русском языке вместо стандартных сообщений интерпретатора
- **Два режима работы:**
  - `advice` — наводящая подсказка без готового кода, стимулирует самостоятельное решение
  - `code` — готовое исправление с кратким комментарием, применяется через меню «лампочки»
- **Поддержка локальных моделей** — код не покидает устройство при использовании Ollama или LM Studio
- **Механизм отказоустойчивости** — автоматическое переключение на резервную модель при недоступности основной

## Требования

- [Node.js](https://nodejs.org/) 20 LTS и выше
- [Visual Studio Code](https://code.visualstudio.com/) 1.100.0 и выше
- Ключ API для [OpenRouter](https://openrouter.ai/) (облачный режим) или локальный сервер [LM Studio](https://lmstudio.ai/) / [Ollama](https://ollama.com/) (локальный режим)

## Быстрая установка (из готового файла)

1. Скачайте файл `student-ai-helper.vsix` из раздела [Releases]()
2. Откройте VS Code → Extensions → ··· → **Install from VSIX...**
3. Выберите скачанный файл
4. Создайте файл `.env` в корне проекта

## Установка из исходного кода

```bash
# 1. Клонируйте репозиторий
git clone [ссылка]
cd student-ai-helper

# 2. Установите зависимости
npm install

# 3. Скомпилируйте TypeScript
npm run compile

# 4. Создайте файл конфигурации
touch .env

# 5. Соберите .vsix файл
npm install -g @vscode/vsce
vsce package

# 6. Установите плагин в VS Code
# Extensions → ··· → Install from VSIX... → выберите .vsix файл
```

## Конфигурация

Создайте файл `.env` на основе шаблона:

```dotenv
# Базовый адрес API
# Облачный режим (OpenRouter):
API_BASE_URL=https://openrouter.ai/api/v1
# Локальный режим (LM Studio):
# API_BASE_URL=http://localhost:1234/v1

# Ключ доступа к API
API_KEY=your-api-key-here

# Список моделей через запятую (первая — основная, остальные — резервные)
MODEL_NAME=meta-llama/llama-3.2-3b-instruct:free,openai/gpt-oss-20b:free

# Режим работы: advice (наводящая подсказка) или code (готовое исправление)
HELP_MODE=advice
```

## Структура репозитория

```
student-ai-helper/
├── client/                  # Клиентская часть — расширение VS Code
│   └── src/
│       └── extension.ts
├── server/                  # Серверная часть — LSP-сервер
│   └── src/
│       └── server.ts
├── tests/                   # Тестовая база из 30 файлов Python
│   ├── syntax/              # Синтаксические ошибки (10 файлов)
│   ├── indent/              # Ошибки отступа (10 файлов)
│   └── logic/               # Логические ошибки (10 файлов)
├── experiments/             # Скрипты для воспроизведения экспериментов
│   ├── measure_response_time.py
│   ├── measure_accuracy.py
│   └── measure_resources.py
├── package.json
└── student-ai-helper.vsix   # Готовый плагин для установки
```

## Воспроизведение экспериментов

Скрипты для воспроизведения экспериментов из главы 4 дипломной работы находятся в папке `experiments/`.

```bash
pip install openai python-dotenv psutil
cd experiments
python measure_response_time.py   # Замер времени отклика
python measure_accuracy.py        # Замер точности локализации ошибок
python measure_resources.py       # Замер потребления ресурсов
```

## Автор

Потапова Д.М., СПбГЭТУ «ЛЭТИ», 2026
