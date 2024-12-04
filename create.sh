#!/bin/bash

# 環境設定
TOPOLOGY_FILE="Geant2012.gml"
CONFIG_DIR="./configs"
IMAGE_NAME="hydrokhoos/ndn-all:arm"
NETWORK_NAME="ndn-network"
LOG_FILE="./create.log"

# ログ出力設定
exec > >(tee -i $LOG_FILE)
exec 2>&1

# エラーメッセージの出力と終了
error_exit() {
  echo "Error: $1" >&2
  exit 1
}

# 必要なファイルとコマンドの確認
[ ! -f "$TOPOLOGY_FILE" ] && error_exit "Topology file '$TOPOLOGY_FILE' not found. Please provide a valid GML file."
[ ! -d "$CONFIG_DIR" ] && error_exit "Configuration directory '$CONFIG_DIR' not found. Please generate NLSR configs first."
command -v docker >/dev/null 2>&1 || error_exit "Docker is not installed or not in the PATH."

# ネットワーク作成
echo "Creating Docker network: $NETWORK_NAME"
docker network create $NETWORK_NAME 2>/dev/null || echo "Docker network '$NETWORK_NAME' already exists."

# ノード作成
echo "Starting NDN nodes..."
for file in $(ls $CONFIG_DIR/nlsr_*.conf); do
  name=$(basename "$file" .conf)
  name="${name#nlsr_}"
  docker run -dit --name $name --network $NETWORK_NAME $IMAGE_NAME 2>/dev/null # コンテナ起動
  docker exec $name bash -c "ndnsec key-gen /$name | ndnsec cert-install -" 2>/dev/null # セキュリティ関連
  docker exec $name bash -c "ndnsec cert-dump -i /$name > default.ndncert"
  docker exec $name bash -c "mkdir -p /usr/local/etc/ndn/keys"
  docker exec $name bash -c "mv default.ndncert /usr/local/etc/ndn/keys/default.ndncert"
  docker cp nfd.conf $name:/nfd.conf  # NFD confファイルをコピー
  docker cp $file $name:/nlsr.conf  # NLSR confファイルをコピー
  docker exec -d $name bash -c "nfd -c /nfd.conf 2> /nfd.log"  # NFDスタート
done

# トポロジー接続処理
echo "Configuring node connections..."
for file in $(ls $CONFIG_DIR/nlsr_*.conf); do
  name=$(basename "$file" .conf)
  name="${name#nlsr_}"
  neibors=$(cat $file | grep face-uri | awk '{print $2}')
  for face in $neibors; do
    docker exec $name nfdc face create $face 2>/dev/null  # 隣接ルータとのface作成
  done
  docker exec -d $name bash -c "nlsr -f /nlsr.conf"  # NLSR起動
done

echo "NDN network setup completed successfully!"
