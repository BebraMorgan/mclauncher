import minecraft_launcher_lib
import subprocess
import json
import os
from tqdm import tqdm
import typer
from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn, TimeElapsedColumn

app = typer.Typer()
console = Console()

CONFIG_PATH = os.path.expanduser('~/.config/mclauncher/settings.json')
DEFAULT_CONFIG = {
    "version": "latest",
    "username": "Player"
}

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
            return json.load(f)
    except Exception as e:
        console.print(f"[red]Ошибка при чтении файла настроек: {e}[/red]")
        return DEFAULT_CONFIG

@app.command()
def launch(
    version: str = typer.Option(None, "-v", "--version", help="Версия Minecraft"),
    username: str = typer.Option(None, "-u", "--username", help="Никнейм игрока")
):
    console.print(Panel("[bold cyan]MCLauncher cli by calvian[/bold cyan]", expand=False))

    ensure_config()
    config = load_config()

    version = version or config.get('version', 'latest')
    username = username or config.get('username', 'Player')


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

    options = {
        "username": username,
    }

    command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)

    console.print(f"[bold blue]Запускаем Minecraft с ником [green]{username}[/green] и версией [green]{version}[/green]...[/bold blue]")
    subprocess.call(command)
    console.print("[bold green]Игра завершена.[/bold green]")

if __name__ == "__main__":
    app()
