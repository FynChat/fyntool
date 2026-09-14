# Настройка Crew AI для fyntool

## Обзор
Crew AI — необязательная интеграция Python-библиотеки для fyntool. При включении во время установки fyntool создаёт файл `.env`, где вы указываете ключ провайдера ИИ и модель.

## Установка
1. Запустите установщик:
   ```bash
   fyntool install
   ```
2. На вопрос **Do you want to enable Crew AI integration?** выберите `Yes`.
3. Будут созданы:
   - `~/.config/fyntool/config.json` с `"crew_ai_enabled": true`
   - `~/.config/fyntool/.env` с пустыми значениями

## Конфигурация
Отредактируйте `~/.config/fyntool/.env`:
```
CREW_AI_API_KEY=your_api_key_here
CREW_AI_BASE_URL=https://api.crew.ai
CREW_AI_MODEL=gpt-4o
```
Также можно изменить редактор и язык в `~/.config/fyntool/config.json`.

## Использование
Проверка статуса:
```bash
fyntool crew status
```
Тест подключения:
```bash
fyntool crew test
```

Открыть конфиг:
```bash
fyntool config
```

## Примечание
- Crew AI — Python библиотека. Установите её через `uv pip install crewai`.
- Ключ и модель читаются из `.env` во время работы.
