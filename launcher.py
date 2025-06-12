import minecraft_launcher_lib
import subprocess
import json
import os
import typer
import webbrowser
from rich.console import Console
from rich.panel import Panel
from tqdm import tqdm

app = typer.Typer()
console = Console()

CONFIG_PATH = os.path.expanduser('~/.config/mclauncher/settings.json')
DEFAULT_CONFIG = {
    "version": "latest",
    "username": "Player",
    "mojang_login": False
}

CLIENT_ID = "00000000402b5328"  # Стандартный Microsoft client ID для Minecraft
REDIRECT_URI = "https://login.live.com/oauth20_desktop.srf"  # Официальный redirect URI для desktop приложений

def ensure_config():
    if not os.path.isfile(CONFIG_PATH):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        try:
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
            console.print(f"[green]Файл настроек создан по пути: {CONFIG_PATH}[/green]")
        except Exception as e:
            console.print(f"[red]Ошибка при создании файла настроек: {e}[/red]")

def load_config():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
            if "mojang_login" not in config:
                config["mojang_login"] = False
            return config
    except Exception as e:
        console.print(f"[red]Ошибка при чтении файла настроек: {e}[/red]")
        return DEFAULT_CONFIG

def microsoft_login():
    # Получаем URL авторизации, state и code_verifier (PKCE)
    login_url, state, code_verifier = minecraft_launcher_lib.microsoft_account.get_secure_login_data(CLIENT_ID, REDIRECT_URI)

    console.print(f"[blue]Откройте в браузере для авторизации:[/blue] [underline]{login_url}[/underline]")
    webbrowser.open(login_url)

    # Пользователь вручную вставляет URL редиректа после авторизации
    redirect_response = typer.prompt("После входа в браузере скопируйте и вставьте сюда URL, на который вы были перенаправлены")

    # Извлекаем auth_code из URL и проверяем state
    auth_code = minecraft_launcher_lib.microsoft_account.parse_auth_code_url(redirect_response, state)

    # Завершаем авторизацию, получаем токены и профиль
    login_data = minecraft_launcher_lib.microsoft_account.complete_login(
        CLIENT_ID,
        None,
        REDIRECT_URI,
        auth_code,
        code_verifier
    )
    return login_data

@app.command()
def launch(
    version: str = typer.Option(None, "-v", "--version", help="Версия Minecraft"),
    username: str = typer.Option(None, "-u", "--username", help="Никнейм игрока"),
    mojang_login: bool = typer.Option(None, "--mojang-login", help="Войти через Mojang/Microsoft аккаунт")
):
    console.print(Panel("[bold cyan]MCLauncher cli by calvian[/bold cyan]", expand=False))

    ensure_config()
    config = load_config()

    version = version or config.get('version', 'latest')
    username = username or config.get('username', 'Player')

    if mojang_login is None:
        mojang_login = config.get('mojang_login', False)

    access_token = None
    selected_profile = None

    if mojang_login:
        try:
            login_data = microsoft_login()
            console.print(f"[blue]Данные входа:[/blue] {login_data}")
            access_token = login_data.get('access_token') or login_data.get('accessToken')
            if not access_token:
                console.print("[red]Ошибка: access_token не найден в ответе авторизации[/red]")
                raise typer.Exit(code=1)
            selected_profile = login_data['selectedProfile']
            username = selected_profile['name']
            console.print(f"[green]Успешный вход! Никнейм: {username}[/green]")
        except Exception as e:
            console.print(f"[red]Ошибка авторизации: {e}[/red]")
            raise typer.Exit(code=1)

    def set_status(text):
        console.print(f"[yellow]{text}[/yellow]")

    pbar = None
    last_progress = 0

    def set_max(value):
        nonlocal pbar, last_progress
        if pbar is not None:
            pbar.close()
        pbar = tqdm(total=value, unit='files', ncols=70)
        last_progress = 0

    def set_progress(value):
        nonlocal pbar, last_progress
        if pbar:
            delta = value - last_progress
            if delta > 0:
                pbar.update(delta)
                last_progress = value
            if value >= pbar.total:
                pbar.close()

    callback = {
        "setStatus": set_status,
        "setProgress": set_progress,
        "setMax": set_max
    }

    minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

    if version == 'latest':
        with console.status("[bold green]Получаем последнюю стабильную версию...[/bold green]", spinner="dots"):
            version = minecraft_launcher_lib.utils.get_latest_version()["release"]

    with console.status(f"[bold green]Устанавливаем версию {version}...[/bold green]", spinner="line"):
        minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directory, callback=callback)

    options = {}
    if mojang_login and access_token and selected_profile:
        options = {
            "username": username,
            "uuid": selected_profile['id'],
            "accessToken": access_token,
            "userType": "mojang"
        }
    else:
        options = {
            "username": username,
        }

    command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)

    console.print(f"[bold blue]Запускаем Minecraft с ником [green]{username}[/green] и версией [green]{version}[/green]...[/bold blue]")
    subprocess.call(command)
    console.print("[bold green]Игра завершена.[/bold green]")

if __name__ == "__main__":
    app()
