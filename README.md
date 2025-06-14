# Minecraft CLI Launcher

Простой консольный лаунчер Minecraft, написанный на Python, с поддержкой установки версий, авторизации и прогресс-бара.

---

## Особенности

- Установка и запуск любой версии Minecraft с официальных серверов Mojang
- Поддержка задания версии и ника через аргументы командной строки или файл настроек
- Конфигурационный файл для хранения настроек в `~/.config/mclauncher/settings.json`
- Удобный CLI 
- Автоматическое создание и развертывание виртуального окружения (при установке)

---

## Требования

- Python 3.7 и выше
- Интернет для загрузки файлов Minecraft
- Установленные зависимости (см. `requirements.txt`)

---

## Установка

1. Клонируйте репозиторий:
```
git clone https://github.com/ваш_пользователь/mclauncher.git
cd mclauncher
```


2. Запустите скрипт установки или вручную создайте виртуальное окружение и установите зависимости:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


3. Запустите лаунчер:
```
python launcher.py launch
```


---

## Использование

Запуск с параметрами:
```
python launcher.py launch -v 1.20.1 -u Steve
```

Если параметры не заданы, используются значения из файла настроек `~/.config/mclauncher/settings.json` или дефолтные (`version=latest`, `username=Player`).

---

## Конфигурация

Файл настроек создаётся автоматически при первом запуске:
```
{
"version": "latest",
"username": "Player"
}
```


Вы можете редактировать его вручную для изменения настроек по умолчанию.

---

## Лицензия
```
MIT License. Подробнее смотрите в файле [LICENSE](LICENSE).
```
---

## Важное
```
- Лаунчер **не распространяет** сам Minecraft и скачивает файлы только с официальных серверов Mojang.
- Используйте лаунчер в соответствии с лицензионным соглашением Minecraft.
```
---

## Контакты

Если у вас есть вопросы или предложения, создавайте issue или пишите в PR.

---

*Этот проект создан для удобного запуска Minecraft из командной строки с минимальными настройками.*
