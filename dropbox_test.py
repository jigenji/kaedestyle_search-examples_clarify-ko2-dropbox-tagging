#!/usr/bin/env python3
import os
import dropbox
from dropbox.files import WriteMode, GetMetadataError
from dropbox.exceptions import ApiError, AuthError
from dotenv import load_dotenv

load_dotenv()

class DropboxTester:
    def __init__(self):
        self.access_token = os.getenv('DROPBOX_ACCESS_TOKEN')
        if not self.access_token:
            raise ValueError("DROPBOX_ACCESS_TOKENが設定されていません。.envファイルを確認してください。")
        
        try:
            self.dbx = dropbox.Dropbox(self.access_token)
            self.dbx.users_get_current_account()
            print("Dropboxへの接続に成功しました！")
        except AuthError:
            raise ValueError("無効なアクセストークンです。正しいトークンを設定してください。")
    
    def upload_file(self, local_path, dropbox_path):
        """ローカルファイルをDropboxにアップロード"""
        try:
            with open(local_path, 'rb') as f:
                print(f"アップロード中: {local_path} -> {dropbox_path}")
                file_metadata = self.dbx.files_upload(
                    f.read(),
                    dropbox_path,
                    mode=WriteMode('overwrite'),
                    autorename=True
                )
                print(f"アップロード成功: {file_metadata.path_display}")
                return file_metadata
        except FileNotFoundError:
            print(f"エラー: ファイルが見つかりません: {local_path}")
            return None
        except ApiError as e:
            print(f"APIエラー: {e}")
            return None
    
    def add_tag(self, file_path, tag):
        """Dropboxファイルにタグを追加"""
        try:
            print(f"タグ追加中: {file_path} <- タグ: {tag}")
            
            # 既存のタグを取得
            try:
                existing_tags = self.dbx.files_tags_get([file_path])
                current_tags = []
                if existing_tags.paths_to_tags:
                    for path_tags in existing_tags.paths_to_tags:
                        if path_tags.path == file_path:
                            current_tags = list(path_tags.tags)
                            break
            except:
                current_tags = []
            
            # 新しいタグを追加
            if tag not in current_tags:
                current_tags.append(tag)
                # files_tags_addメソッドは文字列のタグを直接受け取る
                self.dbx.files_tags_add(file_path, tag)
                print(f"タグ追加成功: {tag}")
                print(f"現在のタグ: {current_tags}")
            else:
                print(f"タグ '{tag}' は既に存在します")
                
            return True
            
        except ApiError as e:
            print(f"タグ追加エラー: {e}")
            return False
    
    def list_tags(self, file_path):
        """ファイルのタグを一覧表示"""
        try:
            tags_result = self.dbx.files_tags_get([file_path])
            if tags_result.paths_to_tags:
                for path_tags in tags_result.paths_to_tags:
                    if path_tags.path == file_path:
                        print(f"ファイル '{file_path}' のタグ:")
                        tag_texts = []
                        for tag in path_tags.tags:
                            # タグオブジェクトからテキストを抽出
                            try:
                                if hasattr(tag, 'user_generated_tag'):
                                    tag_text = tag.user_generated_tag.tag_text
                                elif hasattr(tag, 'tag_text'):
                                    tag_text = tag.tag_text
                                else:
                                    tag_text = str(tag)
                            except AttributeError:
                                tag_text = str(tag)
                            print(f"  - {tag_text}")
                            tag_texts.append(tag_text)
                        return tag_texts
            print(f"ファイル '{file_path}' にはタグがありません")
            return []
        except ApiError as e:
            print(f"タグ取得エラー: {e}")
            return []


def main():
    print("=== Dropbox API 検証ツール ===\n")
    
    try:
        tester = DropboxTester()
        
        # テスト用ファイルの作成
        test_file = "test_upload.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("これはDropbox APIのテスト用ファイルです。\n")
            f.write("ファイルアップロードとタグ付けの動作を確認します。")
        
        # 1. ファイルのアップロード
        print("\n1. ファイルアップロードのテスト")
        print("-" * 40)
        dropbox_path = "/test_upload.txt"
        metadata = tester.upload_file(test_file, dropbox_path)
        
        if metadata:
            # 2. タグの追加
            print("\n2. タグ追加のテスト")
            print("-" * 40)
            tester.add_tag(dropbox_path, "テスト")
            tester.add_tag(dropbox_path, "Python")
            tester.add_tag(dropbox_path, "API検証")
            
            # 3. タグの確認
            print("\n3. タグ一覧の確認")
            print("-" * 40)
            tester.list_tags(dropbox_path)
        
        # テストファイルの削除
        os.remove(test_file)
        print(f"\nローカルのテストファイル '{test_file}' を削除しました")
        
    except ValueError as e:
        print(f"設定エラー: {e}")
    except Exception as e:
        print(f"予期しないエラー: {e}")


if __name__ == "__main__":
    main()