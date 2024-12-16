# ベースイメージとしてNode.jsを使用
FROM node:16-alpine

# 作業ディレクトリを設定
WORKDIR /app

# package.jsonとpackage-lock.jsonをコピー
COPY package*.json ./

# 必要な依存関係をインストール
RUN npm install

# アプリケーションのソースコードをコピー
COPY . .

# ポートを指定（Reactのデフォルトポート）
EXPOSE 3000

# 開発モードでReactアプリを起動
CMD ["npm", "start"]
