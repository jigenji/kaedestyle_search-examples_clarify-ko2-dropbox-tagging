#!/usr/bin/env python3
import webbrowser
from dropbox import DropboxOAuth2FlowNoRedirect

# アプリの情報（Dropbox App Consoleから取得）
print("\n【手順】")
print("1. https://www.dropbox.com/developers/apps にアクセス")
print("2. あなたのアプリを選択")
print("3. 'Settings'タブから'App key'と'App secret'を確認")
print("4. 以下に入力してください\n")

APP_KEY = input("App key を入力: ").strip()
APP_SECRET = input("App secret を入力: ").strip()

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
    print("\n=== Dropbox アクセストークン生成ツール ===\n")
    
    if not APP_KEY or not APP_SECRET:
        print("エラー: App keyとApp secretが必要です")
        return
    
    # OAuth2フローの開始
    auth_flow = DropboxOAuth2FlowNoRedirect(
        APP_KEY,
        APP_SECRET,
        token_access_type=TOKEN_ACCESS_TYPE,
        scope=SCOPES
    )
    
    # 認証URLを取得
    authorize_url = auth_flow.start()
    
    print("1. 以下のURLをブラウザで開いてください:")
    print(authorize_url)
    print("\n2. Dropboxにログインして、アプリを承認してください")
    print("3. 承認後、表示される認証コードをコピーしてください\n")
    
    # ブラウザを自動で開く
    webbrowser.open(authorize_url)
    
    # 認証コードの入力を待つ
    auth_code = input("認証コードを入力してください: ").strip()
    
    try:
        # アクセストークンを取得
        oauth_result = auth_flow.finish(auth_code)
        
        print("\n成功！以下のアクセストークンを.envファイルに設定してください:")
        print("-" * 60)
        print(f"DROPBOX_ACCESS_TOKEN={oauth_result.access_token}")
        print("-" * 60)
        print("\n※ このトークンは安全に保管してください")
        
        # 付与された権限を表示
        if hasattr(oauth_result, 'scope'):
            print("\n付与された権限:")
            for scope in oauth_result.scope.split(' '):
                print(f"  - {scope}")
                
    except Exception as e:
        print(f"\nエラー: {e}")
        print("認証コードが正しいことを確認してください")

if __name__ == "__main__":
    generate_token()