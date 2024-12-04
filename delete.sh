#!/bin/bash

# 設定
NETWORK_NAME="ndn-network"
LOG_FILE="./delete.log"

# ログ出力設定
exec > >(tee -i $LOG_FILE)
exec 2>&1

# エラーメッセージの出力と終了
error_exit() {
    echo "Error: $1" >&2
    exit 1
}

# 必要なコマンドの確認
command -v docker >/dev/null 2>&1 || error_exit "Docker is not installed or not in the PATH."

# コンテナ削除
echo "Stopping and removing NDN containers..."
containers=$(docker ps -a --filter "network=$NETWORK_NAME" --format "{{.ID}}")

if [ -n "$containers" ]; then
    docker stop $containers 2>/dev/null || echo "Warning: Some containers could not be stopped."
    docker rm -f $containers 2>/dev/null || echo "Warning: Some containers could not be removed."
else
    echo "No containers found in network '$NETWORK_NAME'."
fi

# ネットワーク削除
echo "Removing Docker network: $NETWORK_NAME"
docker network rm $NETWORK_NAME 2>/dev/null || echo "Warning: Network '$NETWORK_NAME' does not exist or could not be removed."

# 不要なボリューム削除（オプション）
echo "Cleaning up dangling Docker volumes..."
docker volume prune -f || echo "Warning: Failed to clean up Docker volumes."

# 完了メッセージ
echo "NDN network resources have been successfully cleaned up!"
