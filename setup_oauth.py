#!/usr/bin/env python3
"""
Dropbox OAuth 2.0 セットアップスクリプト
正しい権限を持つアクセストークンを生成します
"""

print("=== Dropbox OAuth 2.0 セットアップ ===\n")
print("このスクリプトは、正しい権限を持つアクセストークンを生成するためのガイドです。\n")

print("【重要】Dropboxの仕様変更により、App Consoleから生成される")
print("トークンには必要な権限が含まれていない場合があります。\n")

print("【解決方法】")
print("1. Dropbox App Consoleにアクセス: https://www.dropbox.com/developers/apps")
print("2. あなたのアプリを選択")
print("3. 'Settings'タブを開く")
print("4. 'OAuth 2'セクションを確認\n")

print("【オプション1: Scoped App（推奨）】")
print("もしアプリが'Scoped access'の場合:")
print("- 'Permissions'タブで必要な権限を全て有効にする")
print("- その後、generate_token.pyを使用してOAuth フローでトークンを生成\n")

print("【オプション2: Full Dropbox App】") 
print("もしアプリが'Full Dropbox'アクセスの場合:")
print("- 古いタイプのアプリなので、全ての権限を持つトークンが生成されるはず")
print("- App Consoleから直接トークンを生成可能\n")

print("【確認方法】")
print("App Consoleの'Settings'タブで、アプリのアクセスタイプを確認してください。")
print("'Permission type'が表示されているはずです。\n")

choice = input("アプリのタイプを選択してください (1: Scoped App, 2: Full Dropbox): ")

if choice == "1":
    print("\n=== Scoped App用の手順 ===")
    print("1. generate_token.pyを編集して、APP_KEYとAPP_SECRETを設定")
    print("2. poetry run python generate_token.py を実行")
    print("3. ブラウザで認証を完了")
    print("4. 生成されたトークンを.envファイルに設定")
elif choice == "2":
    print("\n=== Full Dropbox App用の手順 ===")
    print("1. App Consoleの'Settings'タブを開く")
    print("2. 'Generated access token'セクションで'Generate'をクリック")
    print("3. 生成されたトークンを.envファイルに設定")
else:
    print("\n正しい選択肢を入力してください。")