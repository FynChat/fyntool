# fyntool

Fyn dev tool to create projects, manage docker, git repos and more.

## Installation

### Prerequisites
- Python >=3.12
- `uv` package manager

### Install globally with uv tool  [Recommended]
```bash
uv tool install --from /home/grigoriy/tools/fyntool fyntool
# or from git
uv tool install --from git+https://github.com/your/repo fyntool
```
This places `fyntool` on your PATH via `~/.local/bin`. Run `fyntool --help` anywhere.

### Dev install
```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

### Install with pip
```bash
pip install -e .
```

The tool uses `questionary` for interactive prompts.

## Usage

```bash
fyntool --help
```

### Commands

#### install
Interactive installer. Detects OS and asks project types, tech stacks, and prerequisites.
```bash
fyntool install
```
Questions:
- Which type of project you usually build? `Mobile, Desktop App, FullStack, Backend, Frontend, Data Science, Game Dev, Other`
- Mobile stacks: `Flutter, Kotlin, Swift`
- Desktop stacks: `C++, Node.js with Electron, Tauri`
- Backend languages: `Python, Golang, Rust, C, C#, Java, PHP`
- Install Git? Install Docker? Install uv? Enable Crew AI?

OS support: Linux, macOS, Windows.

#### docker
Docker compose manager
```bash
fyntool docker up
fyntool docker down
fyntool docker ps
fyntool docker logs
```

#### g – Git manager
```bash
fyntool g status
fyntool g commit
fyntool g log
fyntool g push
```
`push` picks repo from `~/.config/fyntool/repos.json` and offers to commit.

#### repos
Manage registered repos
```bash
fyntool repos list
fyntool repos add
fyntool repos remove
```

#### env
Check tool versions
```bash
fyntool env
```

#### build / run / clean
Auto-detect Makefile or package.json
```bash
fyntool build
fyntool run
fyntool clean
```

#### db
Docker DB helpers
```bash
fyntool db migrate
fyntool db fresh
fyntool db shell
```

#### health
Service health checks
```bash
fyntool health
```

#### version
```bash
fyntool version
```

#### doctor
Check environment and config
```bash
fyntool doctor
```

#### config
Open config file in editor
```bash
fyntool config
```
Config location: `~/.config/fyntool/config.json`

#### crew
Crew AI integration
```bash
fyntool crew status
fyntool crew test
```
Enabled during `install`. Creates `~/.config/fyntool/.env`.

### Config
`~/.config/fyntool/config.json`
```json
{
  "editor": "nvim",
  "language": "en",
  "default_branch": "main",
  "auto_push": false,
  "crew_ai_enabled": false
}
```

### Crew AI example

A minimal Crew AI example for FynChat UI generation:

```python
import os
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

load_dotenv()

BASE_DIR = Path(__file__).parent

llm = LLM(
    model=os.getenv('CREW_AI_MODEL','gpt-4o'),
    base_url=os.getenv('CREW_AI_BASE_URL'),
    api_key=os.getenv('CREW_AI_API_KEY'),
    temperature=0.3
)

designer = Agent(role="UI Designer", goal="Design UI", llm=llm, verbose=True)
coder = Agent(role="Qt Developer", goal="Implement UI", llm=llm, verbose=True)

# ... build crew, tasks, kickoff
```

Set keys in `~/.config/fyntool/.env`:
```
CREW_AI_API_KEY=your_api_key
CREW_AI_BASE_URL=https://api.your-provider.com/v1
CREW_AI_MODEL=gpt-4o
```

Full documentation:
- `docs/crew_ai_setup_en.md`
- `docs/crew_ai_setup_ru.md`
- `docs/crew_ai_setup_pt.md`

## Doctor
```bash
fyntool doctor
fyntool doctor --fix
```
Checks Python, uv, config files, git/docker/node and auto-creates missing config on `--fix`.

## CI/CD for beginners
See `docs/ci_cd_beginner.md` for a simple GitHub Actions workflow that runs `fyntool doctor` and `fyntool env` on push.

## Environments
- Linux: `apt`, `sudo`
- macOS: `brew`
- Windows: `winget`

All install commands are OS-aware.

## License
MIT
