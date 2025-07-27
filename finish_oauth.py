#!/usr/bin/env python3
import os
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

def finish_oauth():
    print("=== Dropbox OAuth 2.0 トークン取得 ===\n")
    
    # 環境変数から取得
    APP_KEY = os.getenv('DROPBOX_APP_KEY')
    APP_SECRET = os.getenv('DROPBOX_APP_SECRET')
    AUTH_CODE = os.getenv('DROPBOX_AUTH_CODE')
    
    if not APP_KEY or not APP_SECRET:
        print("エラー: DROPBOX_APP_KEYとDROPBOX_APP_SECRETが設定されていません")
        return
    
    if not AUTH_CODE:
        print("エラー: DROPBOX_AUTH_CODEが設定されていません")
        print("generate_token_env.pyを実行して認証コードを取得してください")
        return
    
    try:
        # OAuth2フローの再開
        auth_flow = DropboxOAuth2FlowNoRedirect(
            APP_KEY,
            APP_SECRET,
            token_access_type=TOKEN_ACCESS_TYPE,
            scope=SCOPES
        )
        
        # フローを開始（URLは使わない）
        auth_flow.start()
        
        # アクセストークンを取得
        print("トークンを取得中...")
        oauth_result = auth_flow.finish(AUTH_CODE.strip())
        
        print("\n成功！")
        print("=" * 60)
        print("以下のトークンを.envファイルのDROPBOX_ACCESS_TOKENに設定してください:")
        print("-" * 60)
        print(oauth_result.access_token)
        print("-" * 60)
        
        # リフレッシュトークンがある場合
        if hasattr(oauth_result, 'refresh_token') and oauth_result.refresh_token:
            print("\nリフレッシュトークン (長期利用用):")
            print(oauth_result.refresh_token)
        
        # 付与された権限を表示
        print("\n付与された権限:")
        if hasattr(oauth_result, 'scope') and oauth_result.scope:
            for scope in oauth_result.scope.split(' '):
                if scope:
                    print(f"  ✓ {scope}")
        
        print("\n※ このトークンは安全に保管してください")
        
    except Exception as e:
        print(f"\nエラー: {e}")
        print("\n考えられる原因:")
        print("1. 認証コードが無効または期限切れ")
        print("2. App KeyまたはApp Secretが正しくない")
        print("3. 認証コードは一度しか使用できません")
        print("\ngenerate_token_env.pyを再実行して新しい認証コードを取得してください")

if __name__ == "__main__":
    finish_oauth()