#!/usr/bin/env python3
import os
import webbrowser
from dropbox import DropboxOAuth2FlowNoRedirect
from dotenv import load_dotenv

load_dotenv()

# 必要な権限
TOKEN_ACCESS_TYPE = "offline"
SCOPES = [
    "files.content.write",
    "files.content.read", 
    "files.metadata.write",
    "files.metadata.read",
    "account_info.read"
]

def generate_token():
    print("=== Dropbox OAuth 2.0 トークン生成ツール ===\n")
    
    # 環境変数から取得
    APP_KEY = os.getenv('DROPBOX_APP_KEY')
    APP_SECRET = os.getenv('DROPBOX_APP_SECRET')
    
    if not APP_KEY or not APP_SECRET:
        print("エラー: 環境変数が設定されていません\n")
        print("以下の手順で設定してください:")
        print("1. Dropbox App Console (https://www.dropbox.com/developers/apps) にアクセス")
        print("2. あなたのアプリを選択")
        print("3. 'Settings'タブから以下を取得:")
        print("   - App key")
        print("   - App secret (「Show」をクリック)")
        print("\n4. .envファイルに以下を追加:")
        print("   DROPBOX_APP_KEY=your_app_key_here")
        print("   DROPBOX_APP_SECRET=your_app_secret_here")
        return
    
    print("App Key: " + APP_KEY[:10] + "..." if len(APP_KEY) > 10 else APP_KEY)
    print("権限をリクエスト中...\n")
    
    # OAuth2フローの開始
    auth_flow = DropboxOAuth2FlowNoRedirect(
        APP_KEY,
        APP_SECRET,
        token_access_type=TOKEN_ACCESS_TYPE,
        scope=SCOPES
    )
    
    # 認証URLを取得
    authorize_url = auth_flow.start()
    
    print("【手順】")
    print("1. 以下のURLをブラウザで開いてください:")
    print("-" * 60)
    print(authorize_url)
    print("-" * 60)
    
    print("\n2. Dropboxにログインして、アプリを承認してください")
    print("3. 承認後、表示される認証コードをコピーしてください")
    print("4. 認証コードを.envファイルに追加してください:")
    print("   DROPBOX_AUTH_CODE=your_auth_code_here")
    print("\n5. その後、finish_oauth.pyを実行してトークンを取得してください")
    
    # URLをファイルに保存
    with open('oauth_url.txt', 'w') as f:
        f.write(authorize_url)
    print("\n※ URLは oauth_url.txt にも保存されました")

if __name__ == "__main__":
    generate_token()