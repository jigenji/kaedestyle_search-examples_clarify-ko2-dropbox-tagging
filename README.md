# Dropbox API Testing

Dropbox APIの動作検証プロジェクト

## 概要

このプロジェクトは、Dropbox APIを使用してファイルのアップロードとタグ付け機能を検証するためのものです。Poetry を使用して依存関係を管理し、OAuth 2.0認証フローを実装しています。

## ファイル構成

### メインスクリプト
- `dropbox_test.py` - Dropbox APIの主要な機能（ファイルアップロード、タグ付け、タグ一覧表示）をテストするメインスクリプト

### OAuth認証関連
- `generate_token_env.py` - OAuth 2.0認証フローを開始し、認証URLを生成するスクリプト
- `finish_oauth.py` - 認証コードからアクセストークンを取得するスクリプト
- `generate_token.py` - インタラクティブにApp Key/Secretを入力してトークンを生成する初期版スクリプト

### ユーティリティ
- `check_permissions.py` - 現在のトークンの権限を確認するスクリプト
- `setup_oauth.py` - OAuth設定のガイドを表示するヘルパースクリプト

### 設定ファイル
- `pyproject.toml` - Poetry プロジェクト設定（依存関係: dropbox, python-dotenv）
- `poetry.lock` - 依存関係のロックファイル
- `.gitignore` - Git除外設定（.env、__pycache__等）

### その他
- `oauth_url.txt` - OAuth認証URLの一時保存ファイル（generate_token_env.pyが生成）

## セットアップ手順

1. 依存関係のインストール
```bash
poetry install
```

2. Dropbox App の作成
- [Dropbox App Console](https://www.dropbox.com/developers/apps) でアプリを作成
- 必要な権限を設定:
  - `files.content.write`
  - `files.content.read`
  - `files.metadata.write`
  - `files.metadata.read`

3. 環境変数の設定（.envファイル）
```
DROPBOX_APP_KEY=your_app_key
DROPBOX_APP_SECRET=your_app_secret
```

4. OAuth認証フローの実行
```bash
poetry run python generate_token_env.py
# ブラウザで認証後、認証コードを.envに追加
poetry run python finish_oauth.py
# 生成されたトークンを.envのDROPBOX_ACCESS_TOKENに設定
```

## テスト実行結果

### 実行コマンド
```bash
poetry run python dropbox_test.py
```

### 実行結果（2025年7月27日 担当者確認済み）
```
=== Dropbox API 検証ツール ===

Dropboxへの接続に成功しました！

1. ファイルアップロードのテスト
----------------------------------------
アップロード中: test_upload.txt -> /test_upload.txt
アップロード成功: /test_upload.txt

2. タグ追加のテスト
----------------------------------------
タグ追加中: /test_upload.txt <- タグ: テスト
タグ追加成功: テスト
現在のタグ: ['テスト']
タグ追加中: /test_upload.txt <- タグ: Python
タグ追加成功: Python
現在のタグ: ['テスト', 'Python']
タグ追加中: /test_upload.txt <- タグ: API検証
タグ追加成功: API検証
現在のタグ: ['テスト', 'Python', 'API検証']

3. タグ一覧の確認
----------------------------------------
ファイル '/test_upload.txt' のタグ:
  - テスト
  - python
  - api検証

ローカルのテストファイル 'test_upload.txt' を削除しました
```

### 確認事項（✅ 全て確認済み）
- ✅ ファイル（test_upload.txt）が Dropbox にアップロードされていることを確認
- ✅ アップロードされたファイルに3つのタグ（テスト、Python、API検証）が付けられていることを確認
- ✅ タグの一覧表示機能が正常に動作することを確認
- ✅ 日本語タグ（テスト、API検証）が正しく処理されることを確認

## 注意事項

- `.env`ファイルは機密情報を含むため、Gitには含まれていません
- Dropboxでは英字のタグは自動的に小文字に変換されます（例: Python → python）
- OAuth認証コードは一度しか使用できないため、エラーが発生した場合は再度認証フローを実行してください