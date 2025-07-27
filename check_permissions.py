#!/usr/bin/env python3
import os
import dropbox
from dotenv import load_dotenv

load_dotenv()

def check_permissions():
    access_token = os.getenv('DROPBOX_ACCESS_TOKEN')
    if not access_token:
        print("エラー: DROPBOX_ACCESS_TOKENが設定されていません")
        return
    
    try:
        dbx = dropbox.Dropbox(access_token)
        
        # アカウント情報を取得
        account = dbx.users_get_current_account()
        print(f"アカウント: {account.name.display_name}")
        print(f"Email: {account.email}")
        
        # トークンのスコープを確認
        print("\n現在のトークンが持つ権限:")
        # この情報は実際にAPIを使ってみないと確認できないため、
        # テストアップロードを試みます
        
        print("\n権限テスト中...")
        
        # 小さなテストファイルをアップロード
        try:
            dbx.files_upload(b"test", "/permission_test.txt")
            print("✓ files.content.write - ファイルアップロード権限: OK")
            
            # アップロードしたファイルを削除
            dbx.files_delete_v2("/permission_test.txt")
            print("✓ files.metadata.write - ファイル削除権限: OK")
        except Exception as e:
            print(f"✗ ファイル操作権限: エラー - {e}")
        
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    check_permissions()