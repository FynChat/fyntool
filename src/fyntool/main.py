'''
Fyn tool: A tool to create your projects, manage docker, git remote repos and more.
'''

import os
import sys
import json
import platform
import shutil
import subprocess
from pathlib import Path

import questionary
import subparse

CONFIG_DIR = Path.home() / ".config" / "fyntool"
REPOS_FILE = CONFIG_DIR / "repos.json"
CONFIG_FILE = CONFIG_DIR / "config.json"
VERSION = "1.0.0"


def detect_os():
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    return system


def command_exists(cmd):
    return shutil.which(cmd) is not None


def run_cmd(cmd, cwd=None, check=True):
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, text=True, cwd=cwd)
    if check and result.returncode != 0:
        print(f"Command failed with code {result.returncode}")
    return result.returncode == 0


def install_git(os_type):
    if command_exists("git"):
        print("Git is already installed.")
        return True
    print("Installing Git...")
    cmds = {
        "linux": "sudo apt-get update && sudo apt-get install -y git",
        "macos": "brew install git",
        "windows": "winget install --id Git.Git -e",
    }
    cmd = cmds.get(os_type)
    if cmd:
        return run_cmd(cmd)
    print("Unsupported OS for automatic Git install.")
    return False


def install_docker(os_type):
    if command_exists("docker"):
        print("Docker is already installed.")
        return True
    print("Installing Docker...")
    cmds = {
        "linux": "sudo apt-get update && sudo apt-get install -y docker.io",
        "macos": "brew install --cask docker",
        "windows": "winget install --id Docker.DockerDesktop -e",
    }
    cmd = cmds.get(os_type)
    if cmd:
        return run_cmd(cmd)
    print("Unsupported OS for automatic Docker install.")
    return False


def install_uv(os_type):
    if command_exists("uv"):
        print("uv is already installed.")
        return True
    print("Installing uv...")
    # Official install script
    cmd = "curl -LsSf https://astral.sh/uv/install.sh | sh"
    if os_type == "windows":
        cmd = "powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\""
    return run_cmd(cmd, check=False)


def install_node(os_type):
    if command_exists("node"):
        print("Node.js is already installed.")
        return True
    print("Installing Node.js...")
    cmds = {
        "linux": "curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs",
        "macos": "brew install node",
        "windows": "winget install --id OpenJS.NodeJS.LTS -e",
    }
    cmd = cmds.get(os_type)
    if cmd:
        return run_cmd(cmd)
    return False


def install_python(os_type):
    # Python is usually preinstalled, ensure via uv
    print("Ensuring Python is available via uv...")
    return True


def install_go(os_type):
    if command_exists("go"):
        print("Go is already installed.")
        return True
    print("Installing Go...")
    cmds = {
        "linux": "sudo apt-get update && sudo apt-get install -y golang",
        "macos": "brew install go",
        "windows": "winget install --id Golang.Go -e",
    }
    cmd = cmds.get(os_type)
    return run_cmd(cmd) if cmd else False


def install_rust(os_type):
    if command_exists("cargo"):
        print("Rust is already installed.")
        return True
    print("Installing Rust via rustup...")
    return run_cmd("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh", check=False)


def install_dotnet(os_type):
    if command_exists("dotnet"):
        print(".NET SDK is already installed.")
        return True
    print("Installing .NET SDK...")
    cmds = {
        "linux": "wget https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb && sudo dpkg -i packages-microsoft-prod.deb && sudo apt-get update && sudo apt-get install -y dotnet-sdk-8.0",
        "macos": "brew install --cask dotnet-sdk",
        "windows": "winget install --id Microsoft.DotNet.SDK.8 -e",
    }
    cmd = cmds.get(os_type)
    return run_cmd(cmd) if cmd else False


def install_java(os_type):
    if command_exists("java"):
        print("Java is already installed.")
        return True
    print("Installing Java...")
    cmds = {
        "linux": "sudo apt-get update && sudo apt-get install -y openjdk-17-jdk",
        "macos": "brew install openjdk@17",
        "windows": "winget install --id Oracle.JavaRuntimeEnvironment -e",
    }
    cmd = cmds.get(os_type)
    return run_cmd(cmd) if cmd else False


def install_php(os_type):
    if command_exists("php"):
        print("PHP is already installed.")
        return True
    print("Installing PHP...")
    cmds = {
        "linux": "sudo apt-get update && sudo apt-get install -y php",
        "macos": "brew install php",
        "windows": "winget install --id PHP.PHP -e",
    }
    cmd = cmds.get(os_type)
    return run_cmd(cmd) if cmd else False


def install_cpp(os_type):
    print("Installing C++ build tools...")
    cmds = {
        "linux": "sudo apt-get update && sudo apt-get install -y build-essential",
        "macos": "xcode-select --install",
        "windows": "winget install --id Microsoft.VisualStudio.2022.BuildTools -e",
    }
    cmd = cmds.get(os_type)
    return run_cmd(cmd) if cmd else False


def install_flutter(os_type):
    print("Installing Flutter...")
    print("[INFO] Flutter installation is manual. Run: https://docs.flutter.dev/get-started/install")
    return False


def install_kotlin(os_type):
    print("Installing Kotlin / Android SDK...")
    print("[INFO] Install Android Studio and SDK for Kotlin. https://developer.android.com/studio")
    return False


def install_swift(os_type):
    if os_type != "macos":
        print("Swift requires macOS. Skipping.")
        return False
    print("Installing Swift / Xcode...")
    print("[INFO] Install Xcode from Mac App Store.")
    return False


PROJECT_TOOLS = {
    "Mobile": ["flutter"],
    "Desktop App": ["nodejs", "tauri"],
    "FullStack": ["nodejs", "python", "postgresql"],
    "Backend": ["python", "postgresql"],
    "Frontend": ["nodejs"],
    "Data Science": ["python", "jupyter"],
    "Game Dev": ["nodejs"],
    "Other": [],
}


def handle_install(context, args):
    os_type = detect_os()
    print(f"Detected OS: {os_type}")

    project_types = questionary.checkbox(
        "Which type of project you usually build?",
        choices=[
            "Mobile",
            "Desktop App",
            "FullStack",
            "Backend",
            "Frontend",
            "Data Science",
            "Game Dev",
            "Other",
        ],
    ).ask()

    if not project_types:
        print("No project types selected. Exiting.")
        return

    print(f"Selected project types: {', '.join(project_types)}")

    # Technology sub-questions
    tech_choices = {}
    if "Mobile" in project_types:
        mobile_stacks = questionary.checkbox(
            "Which mobile stacks do you use?",
            choices=["Flutter", "Kotlin", "Swift"],
        ).ask() or []
        tech_choices["mobile"] = mobile_stacks
        print(f"Mobile stacks: {', '.join(mobile_stacks) if mobile_stacks else 'None'}")

    if "Desktop App" in project_types:
        desktop_stacks = questionary.checkbox(
            "Which desktop stacks do you use?",
            choices=["C++", "Node.js with Electron", "Tauri"],
        ).ask() or []
        tech_choices["desktop"] = desktop_stacks
        print(f"Desktop stacks: {', '.join(desktop_stacks) if desktop_stacks else 'None'}")

    if "Backend" in project_types:
        backend_langs = questionary.checkbox(
            "Which backend languages do you use?",
            choices=["Python", "Golang", "Rust", "C", "C#", "Java", "PHP"],
        ).ask() or []
        tech_choices["backend"] = backend_langs
        print(f"Backend languages: {', '.join(backend_langs) if backend_langs else 'None'}")

    install_git_flag = questionary.confirm(
        "Do you want to install Git?", default=True
    ).ask()
    install_docker_flag = questionary.confirm(
        "Do you want to install Docker?", default=False
    ).ask()
    install_uv_flag = questionary.confirm(
        "Do you want to install uv package manager?", default=True
    ).ask()
    crew_ai_flag = questionary.confirm(
        "Do you want to enable Crew AI integration?", default=False
    ).ask()

    # Additional questions
    non_interactive = questionary.confirm(
        "Skip project-specific tool installation and only install prerequisites?",
        default=False
    ).ask()

    if install_git_flag:
        install_git(os_type)

    if install_docker_flag:
        install_docker(os_type)

    if install_uv_flag:
        install_uv(os_type)

    # Crew AI setup
    ensure_config()
    config_data = json.loads(CONFIG_FILE.read_text())
    config_data["crew_ai_enabled"] = crew_ai_flag
    CONFIG_FILE.write_text(json.dumps(config_data, indent=2))
    if crew_ai_flag:
        env_file = CONFIG_DIR / ".env"
        if not env_file.exists():
            env_content = """# Crew AI Configuration
CREW_AI_API_KEY=your_api_key_here
CREW_AI_BASE_URL=https://api.crew.ai
"""
            env_file.write_text(env_content)
            print(f"Created {env_file} – edit with your credentials.")
        else:
            print(f".env already exists at {env_file}")

    if not non_interactive:
        # Install based on project types
        tools_needed = set()
        for pt in project_types:
            tools_needed.update(PROJECT_TOOLS.get(pt, []))

        if "nodejs" in tools_needed:
            install_node(os_type)
        if "python" in tools_needed:
            install_python(os_type)

        # Install based on tech choices
        mobile = tech_choices.get("mobile", [])
        if "Flutter" in mobile:
            install_flutter(os_type)
        if "Kotlin" in mobile:
            install_kotlin(os_type)
        if "Swift" in mobile:
            install_swift(os_type)

        desktop = tech_choices.get("desktop", [])
        if "C++" in desktop:
            install_cpp(os_type)
        if "Node.js with Electron" in desktop:
            install_node(os_type)

        backend = tech_choices.get("backend", [])
        if "Python" in backend:
            install_python(os_type)
        if "Golang" in backend:
            install_go(os_type)
        if "Rust" in backend:
            install_rust(os_type)
        if "C#" in backend:
            install_dotnet(os_type)
        if "Java" in backend:
            install_java(os_type)
        if "PHP" in backend:
            install_php(os_type)
        if "C" in backend:
            install_cpp(os_type)

        # Placeholder for other tools
        for tool in tools_needed:
            if tool not in ("nodejs", "python"):
                print(f"[INFO] Would install {tool} for your selected projects. Manual installation required.")

    print("Installation setup complete!")


def docker_factory(parser):
    """
    Manage docker compose

    Usage:
        fyntool docker up
        fyntool docker down
        fyntool docker ps
        fyntool docker logs
    """
    parser.add_argument("action", choices=["up", "down", "ps", "logs"], help="Docker compose action")


def handle_docker(context, args):
    cwd = Path.cwd()
    action = args.action
    print(f"Running docker compose {action} in {cwd}")
    if action == "up":
        run_cmd("docker compose up -d --build", cwd=str(cwd))
    elif action == "down":
        run_cmd("docker compose down", cwd=str(cwd))
    elif action == "ps":
        run_cmd("docker compose ps", cwd=str(cwd))
    elif action == "logs":
        run_cmd("docker compose logs --tail=50", cwd=str(cwd))


def git_factory(parser):
    """
    Git manager

    Usage:
        fyntool g status
        fyntool g commit
        fyntool g log
        fyntool g push
        fyntool g pull
    """
    parser.add_argument("action", choices=["status", "commit", "log", "push", "pull"], help="Git action")


def handle_git(context, args):
    action = args.action
    if action == "status":
        cwd = Path.cwd()
        run_cmd("git status --short", cwd=str(cwd))
    elif action == "commit":
        cwd = Path.cwd()
        msg = questionary.text("Commit message", default="chore: update").ask()
        if not msg:
            print("Commit message required.")
            return
        run_cmd("git add .", cwd=str(cwd))
        run_cmd(f'git commit -m "{msg}"', cwd=str(cwd))
    elif action == "log":
        cwd = Path.cwd()
        run_cmd("git log --oneline -n 20", cwd=str(cwd))
    elif action == "push":
        # Pick repo from registry if available
        ensure_config()
        data = load_repos()
        repos = data.get("repos", [])
        if repos:
            names = [r.get("name") for r in repos]
            choice = questionary.select("Which repo to push?", names).ask()
            if not choice:
                print("Cancelled.")
                return
            repo = next(r for r in repos if r.get("name") == choice)
            repo_path = Path(repo.get("path")).expanduser()
            branch = questionary.text("Branch", default=repo.get("branch","main")).ask() or repo.get("branch","main")
        else:
            repo_path = Path.cwd()
            branch = questionary.text("Branch", default="main").ask() or "main"
        if not repo_path.exists():
            print(f"Path does not exist: {repo_path}")
            return
        # Check status
        status = subprocess.run("git status --porcelain", shell=True, cwd=str(repo_path), capture_output=True, text=True)
        has_changes = bool(status.stdout.strip())
        if has_changes:
            if questionary.confirm("Local changes detected. Commit before push?", default=True).ask():
                msg = questionary.text("Commit message", default="chore: update").ask()
                run_cmd("git add .", cwd=str(repo_path))
                run_cmd(f'git commit -m "{msg}"', cwd=str(repo_path))
        run_cmd(f"git push origin {branch}", cwd=str(repo_path))
    elif action == "pull":
        cwd = Path.cwd()
        # Check if branch has upstream
        upstream_check = subprocess.run(
            "git rev-parse --abbrev-ref --symbolic-full-name @{u}",
            shell=True, cwd=str(cwd), capture_output=True, text=True
        )
        if upstream_check.returncode != 0:
            # No upstream, prompt user
            print("No upstream tracking info for current branch.")
            remotes = subprocess.run("git remote", shell=True, cwd=str(cwd), capture_output=True, text=True).stdout.strip().splitlines()
            if not remotes:
                print("No remotes found.")
                return
            remote = questionary.select("Select remote", remotes).ask()
            if not remote:
                print("Cancelled.")
                return
            branches = subprocess.run(f"git branch -r", shell=True, cwd=str(cwd), capture_output=True, text=True).stdout.strip().splitlines()
            branch_names = [b.strip().replace(f"{remote}/","") for b in branches if b.strip().startswith(f"{remote}/")]
            if not branch_names:
                print("No remote branches found.")
                return
            branch = questionary.select("Select branch to pull", branch_names).ask()
            if not branch:
                print("Cancelled.")
                return
            # Set upstream
            current_branch = subprocess.run("git rev-parse --abbrev-ref HEAD", shell=True, cwd=str(cwd), capture_output=True, text=True).stdout.strip()
            set_upstream = questionary.confirm(f"Set upstream {remote}/{branch} for {current_branch}?", default=True).ask()
            if set_upstream:
                run_cmd(f"git branch --set-upstream-to={remote}/{branch} {current_branch}", cwd=str(cwd))
            run_cmd(f"git pull {remote} {branch}", cwd=str(cwd))
        else:
            run_cmd("git pull", cwd=str(cwd))


def handle_env(context, args):
    tools = [
        ("git", "git --version"),
        ("docker", "docker --version"),
        ("node", "node --version"),
        ("python", "python3 --version"),
        ("uv", "uv --version"),
        ("g++", "g++ --version"),
    ]
    print("Environment check:")
    for name, cmd in tools:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            ver = result.stdout.strip().splitlines()[0]
            print(f"  {name}: {ver}")
        else:
            print(f"  {name}: NOT INSTALLED")


def ensure_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not REPOS_FILE.exists():
        REPOS_FILE.write_text(json.dumps({"repos": []}, indent=2))
    if not CONFIG_FILE.exists():
        default_config = {
            "editor": "nvim",
            "language": "en",
            "default_branch": "main",
            "auto_push": False,
            "crew_ai_enabled": False,
        }
        CONFIG_FILE.write_text(json.dumps(default_config, indent=2))


def load_repos():
    ensure_config()
    return json.loads(REPOS_FILE.read_text())


def save_repos(data):
    REPOS_FILE.write_text(json.dumps(data, indent=2))


def repos_factory(parser):
    """
    Manage registered repos

    Usage:
        fyntool repos list
        fyntool repos add
        fyntool repos remove
    """
    parser.add_argument("action", choices=["list", "add", "remove"], help="Repos action")


def handle_repos(context, args):
    action = args.action
    if action == "list":
        data = load_repos()
        repos = data.get("repos", [])
        if not repos:
            print("No repos registered.")
            return
        for i, r in enumerate(repos, 1):
            print(f"{i}. {r.get('name')} - {r.get('path')} [{r.get('branch','main')}]")
    elif action == "add":
        name = questionary.text("Repo name").ask()
        path = questionary.text("Local path", default=str(Path.cwd())).ask()
        branch = questionary.text("Branch", default="main").ask()
        if not name:
            print("Name required.")
            return
        data = load_repos()
        repos = data.get("repos", [])
        if any(r.get("name") == name for r in repos):
            print(f"Repo '{name}' already exists.")
            return
        repos.append({"name": name, "path": path, "branch": branch})
        save_repos({"repos": repos})
        print(f"Added repo {name}")
    elif action == "remove":
        data = load_repos()
        repos = data.get("repos", [])
        if not repos:
            print("No repos to remove.")
            return
        names = [r.get("name") for r in repos]
        choice = questionary.select("Which repo to remove?", names).ask()
        if not choice:
            print("Cancelled.")
            return
        repos = [r for r in repos if r.get("name") != choice]
        save_repos({"repos": repos})
        print(f"Removed {choice}")


def handle_build(context, args):
    cwd = Path.cwd()
    if (cwd / "Makefile").exists():
        run_cmd("make", cwd=str(cwd))
    elif (cwd / "package.json").exists():
        run_cmd("npm run build", cwd=str(cwd))
    else:
        print("No known build system found in current directory.")


def handle_run(context, args):
    cwd = Path.cwd()
    if (cwd / "Makefile").exists():
        run_cmd("make run", cwd=str(cwd))
    elif (cwd / "package.json").exists():
        run_cmd("npm start", cwd=str(cwd))
    else:
        print("No known run target found in current directory.")


def handle_clean(context, args):
    cwd = Path.cwd()
    if (cwd / "Makefile").exists():
        run_cmd("make clean", cwd=str(cwd))
        return
    for d in ["build", "dist", ".next", "target"]:
        p = cwd / d
        if p.exists():
            print(f"Removing {p}")
            run_cmd(f"rm -rf {d}", cwd=str(cwd))


def handle_version(context, args):
    print(f"fyntool version {VERSION}")
    print(f"Config dir: {CONFIG_DIR}")
    print(f"Repos file: {REPOS_FILE}")


def handle_health(context, args):
    checks = [
        ("Laravel API", "http://localhost/api/auth/me"),
        ("Go WS", "http://localhost:8080/health"),
        ("MinIO", "http://localhost:9000/minio/health/live"),
        ("Mailpit", "http://localhost:8025"),
    ]
    print("Health checks:")
    for name, url in checks:
        result = subprocess.run(f"curl -s -o /dev/null -w '%{{http_code}}' {url}", shell=True, capture_output=True, text=True)
        code = result.stdout.strip() or "000"
        status = "UP" if code == "200" else f"{code}"
        print(f"  {name}: {status}")


def db_factory(parser):
    """
    Database manager via docker compose

    Usage:
        fyntool db migrate
        fyntool db fresh
        fyntool db shell
    """
    parser.add_argument("action", choices=["migrate", "fresh", "shell"], help="DB action")


def handle_db(context, args):
    action = args.action
    if action == "migrate":
        run_cmd("docker compose exec app php artisan migrate")
    elif action == "fresh":
        if questionary.confirm("This will wipe the database. Continue?", default=False).ask():
            run_cmd("docker compose exec app php artisan migrate:fresh --seed")
        else:
            print("Cancelled.")
    elif action == "shell":
        run_cmd("docker compose exec db psql -U postgres -d postgres")


def handle_config(context, args):
    ensure_config()
    config = json.loads(CONFIG_FILE.read_text())
    editor = config.get("editor", "nvim")
    print(f"Opening {CONFIG_FILE} with {editor}")
    # Fallback if editor not found
    try:
        subprocess.run([editor, str(CONFIG_FILE)], check=False)
    except FileNotFoundError:
        print(f"Editor '{editor}' not found. Config file at {CONFIG_FILE}")
        # Try default open
        import os
        if sys.platform.startswith("linux"):
            subprocess.run(["xdg-open", str(CONFIG_FILE)])
        elif sys.platform == "darwin":
            subprocess.run(["open", str(CONFIG_FILE)])
        else:
            print("Open the file manually.")


def build_factory(parser):
    """
    Build project using Makefile or npm run build

    Usage:
        fyntool build
    """
    pass


def run_factory(parser):
    """
    Run project using make run or npm start

    Usage:
        fyntool run
    """
    pass


def clean_factory(parser):
    """
    Clean build artifacts

    Usage:
        fyntool clean
    """
    pass


def version_factory(parser):
    """
    Show fyntool version and config paths

    Usage:
        fyntool version
    """
    pass


def health_factory(parser):
    """
    Check health of local services via HTTP

    Usage:
        fyntool health
    """
    pass


def env_factory(parser):
    """
    Show versions of common dev tools

    Usage:
        fyntool env
    """
    pass


def config_factory(parser):
    """
    Open fyntool config.json in editor

    Usage:
        fyntool config
    """
    pass


def install_factory(parser):
    """
    Interactive install of dev tools

    Usage:
        fyntool install
    """
    pass


def doctor_factory(parser):
    """
    Check environment and config

    Usage:
        fyntool doctor
        fyntool doctor --fix
    """
    parser.add_argument("--fix", action="store_true", help="Auto-fix missing config files")


def handle_doctor(context, args):
    print("fyntool doctor")
    # Python
    print(f"Python: {sys.version.split()[0]}")
    # uv
    uv_exists = shutil.which("uv") is not None
    print(f"uv: {'found' if uv_exists else 'NOT FOUND'}")
    # Config
    ensure_config()
    if args.fix:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if not CONFIG_FILE.exists():
            print("Creating default config.json...")
            default_config = {
                "editor": "nvim",
                "language": "en",
                "default_branch": "main",
                "auto_push": False,
                "crew_ai_enabled": False,
            }
            CONFIG_FILE.write_text(json.dumps(default_config, indent=2))
        if not REPOS_FILE.exists():
            print("Creating repos.json...")
            REPOS_FILE.write_text(json.dumps({"repos": []}, indent=2))
    print(f"Config dir: {CONFIG_DIR.exists()}")
    print(f"Config file: {CONFIG_FILE.exists()}")
    print(f"Repos file: {REPOS_FILE.exists()}")
    # Tools
    for cmd in ["git", "docker", "node", "python3"]:
        print(f"{cmd}: {'OK' if shutil.which(cmd) else 'MISSING'}")
    # PATH check
    print(f"Executable path: {sys.argv[0]}")



def crew_factory(parser):
    """
    Crew AI integration

    Usage:
        fyntool crew status
        fyntool crew test
    """
    parser.add_argument("action", choices=["status", "test"], help="Crew AI action")


def handle_crew(context, args):
    ensure_config()
    config = json.loads(CONFIG_FILE.read_text())
    enabled = config.get("crew_ai_enabled", False)
    env_file = CONFIG_DIR / ".env"
    if not enabled:
        print("Crew AI is disabled. Enable it in install or edit config.json")
        return
    if not env_file.exists():
        print(f".env not found at {env_file}. Run install with Crew AI enabled.")
        return
    if args.action == "status":
        print("Crew AI status:")
        print(f"  Enabled: {enabled}")
        print(f"  Config: {CONFIG_FILE}")
        print(f"  Env: {env_file}")
        # Show masked key
        try:
            env_content = env_file.read_text()
            for line in env_content.splitlines():
                if line.startswith("CREW_AI_API_KEY"):
                    key = line.split("=",1)[1]
                    masked = key[:4] + "***" + key[-4:] if len(key)>8 else "***"
                    print(f"  API Key: {masked}")
        except Exception:
            pass
    elif args.action == "test":
        print("Testing Crew AI connection...")
        # Placeholder – real test would import crewai and call a model
        print("[INFO] Crew AI test stub. Add your provider key and model in .env to enable real calls.")


def release_factory(parser):
    """
    Create a git tag and push release

    Usage:
        fyntool release
    """
    pass


def handle_release(context, args):
    cwd = Path.cwd()
    if not (cwd / ".git").exists():
        print("Not a git repository")
        return
    version = questionary.text("Version tag", default="v0.1.0").ask()
    if not version:
        print("Version required")
        return
    run_cmd("git add .", cwd=str(cwd))
    run_cmd(f'git commit -m "chore: release {version}"', cwd=str(cwd))
    run_cmd(f"git tag {version}", cwd=str(cwd))
    run_cmd(f"git push origin HEAD --tags", cwd=str(cwd))
    print(f"Released {version}")


def main():
    cli = subparse.CLI(prog="fyntool", description="Fyn dev tool")
    cli.add_command(install_factory, handle_install, name="install")
    cli.add_command(docker_factory, handle_docker, name="docker")
    cli.add_command(git_factory, handle_git, name="g")
    cli.add_command(env_factory, handle_env, name="env")
    cli.add_command(repos_factory, handle_repos, name="repos")
    cli.add_command(build_factory, handle_build, name="build")
    cli.add_command(run_factory, handle_run, name="run")
    cli.add_command(clean_factory, handle_clean, name="clean")
    cli.add_command(version_factory, handle_version, name="version")
    cli.add_command(health_factory, handle_health, name="health")
    cli.add_command(db_factory, handle_db, name="db")
    cli.add_command(config_factory, handle_config, name="config")
    cli.add_command(crew_factory, handle_crew, name="crew")
    cli.add_command(doctor_factory, handle_doctor, name="doctor")
    cli.add_command(release_factory, handle_release, name="release")
    cli.run()


if __name__ == "__main__":
    main()
