#!/bin/bash

APP_NAME="mclauncher"
INSTALL_DIR="/opt/$APP_NAME"
BIN_PATH="/usr/local/bin/$APP_NAME"
VENV_DIR="$INSTALL_DIR/venv"

echo "Установка $APP_NAME..."

sudo mkdir -p "$INSTALL_DIR"

sudo cp -r ./* "$INSTALL_DIR"

python3 -m venv "$VENV_DIR"

source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$INSTALL_DIR/requirements.txt"
deactivate

sudo tee "$BIN_PATH" >/dev/null <<EOF
#!/bin/bash
source "$VENV_DIR/bin/activate"
python "$INSTALL_DIR/launcher.py" "\$@"
EOF

sudo chmod +x "$BIN_PATH"

echo "Установка завершена."
echo "Запускать лаунчер можно командой: $APP_NAME"
