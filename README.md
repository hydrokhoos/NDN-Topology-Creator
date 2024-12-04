# NDN-Topology-Creator

このレポジトリは、ネットワークトポロジーファイル（GML形式）を使用して、NLSR（Named Link State Routing）のコンフィグファイルを生成し、NDN（Named Data Networking）ネットワークを構築するためのツールを提供します。

## 前提条件
- Python 3.x
- Docker

## 使い方
### 1. トポロジーファイル (GML) をダウンロード
サンプルとして[Topology_Zoo](https://topology-zoo.org)からGeantのGMLファイルをダウンロードします。
```bash
wget --no-check-certificate https://topology-zoo.org/files/Geant2012.gml
```

### 2. トポロジーの確認
ダウンロードしたトポロジーファイルを以下のコマンドで確認します。
```bash
python3 gml_show.py Geant2012.gml
```
networkxとmatplotlibが必要です。

### 3. NLSRコンフィグファイルの作成
以下のコマンドで、ネットワークトポロジーに基づいたNLSRの設定ファイルを生成します。
```bash
python3 create_conf.py
```

### 4. NDNネットワークの構築
Dockerを使用してNDNネットワークを構築します。以下のコマンドを実行してください。
```bash
./create.sh
```

### 5. コンテナの削除と後処理
NDNネットワークを削除する場合は以下のコマンドを実行します。
```bash
./delete.sh
```
生成されたNLSR設定ファイルも削除する場合は以下を実行してください。
```bash
rm configs/nlsr_*.conf
```

## リンク
- [Topology Zoo](https://topology-zoo.org)
- [Named Data Networking (NDN)](https://named-data.net)
- [NLSR Documentation](https://named-data.net/doc/NLSR/current/)
