# Crew AI Setup for fyntool

## Overview
Crew AI is an optional Python library integration for fyntool. When enabled during install, fyntool creates a `.env` file where you put your AI provider key and model.

## Installation
1. Run installer:
   ```bash
   fyntool install
   ```
2. When asked **Do you want to enable Crew AI integration?** select `Yes`.
3. fyntool will create:
   - `~/.config/fyntool/config.json` with `"crew_ai_enabled": true`
   - `~/.config/fyntool/.env` with placeholders

## Configuration
Edit `~/.config/fyntool/.env`:
```
CREW_AI_API_KEY=your_api_key_here
CREW_AI_BASE_URL=https://api.crew.ai
CREW_AI_MODEL=gpt-4o
```
You can also change default editor and language in `~/.config/fyntool/config.json`:
```json
{
  "editor": "nvim",
  "language": "en",
  "crew_ai_enabled": true
}
```

## Usage
Check status:
```bash
fyntool crew status
```
Test connection:
```bash
fyntool crew test
```

Open config:
```bash
fyntool config
```

## Notes
- Crew AI is a Python library. Install it via `uv pip install crewai` or your preferred manager.
- The key and model are read from `.env` at runtime.
