#!/bin/bash

APP_NAME="mclauncher"
INSTALL_DIR="/opt/$APP_NAME"
BIN_PATH="/usr/local/bin/$APP_NAME"

echo "Удаление $APP_NAME..."

if [ -f "$BIN_PATH" ]; then
  sudo rm "$BIN_PATH"
  echo "Удалён $BIN_PATH"
else
  echo "Исполняемый файл $BIN_PATH не найден"
fi

if [ -d "$INSTALL_DIR" ]; then
  sudo rm -rf "$INSTALL_DIR"
  echo "Удалена директория $INSTALL_DIR"
else
  echo "Директория $INSTALL_DIR не найдена"
fi

echo "Удаление завершено."
