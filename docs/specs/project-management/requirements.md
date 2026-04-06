# 要件定義書

## はじめに

System Reforgeにおけるプロジェクト管理機能の要件を定義する。プロジェクトはレガシーコード解析の基本単位であり、ユーザーはプロジェクトを作成・一覧表示・詳細確認・削除できる。バックエンド（FastAPI + PostgreSQL）とフロントエンド（React + Mantine）の両方をカバーする。

## 用語集

- **Project**: レガシーコード解析の単位。名前、説明、S3プレフィックスを持つエンティティ
- **Project_API**: プロジェクトのCRUD操作を提供するREST APIエンドポイント群
- **Project_List_Page**: プロジェクト一覧を表示するフロントエンドページ
- **Project_Form**: プロジェクト作成時の入力フォームコンポーネント
- **Project_Repository**: プロジェクトのデータ永続化を担うリポジトリインターフェース
- **Pagination**: 一覧取得時のページ分割機能（page, per_page, total）

## 要件

### 要件 1: プロジェクト作成

**ユーザーストーリー:** 解析担当者として、新しいプロジェクトを作成したい。レガシーコードの解析対象を管理するためである。

#### 受け入れ基準

1. WHEN ユーザーがプロジェクト名と説明を入力して送信した場合、THE Project_API SHALL UUIDを生成し、s3_prefixを自動設定し、プロジェクトをデータベースに保存して、作成されたプロジェクトデータを返却する
2. WHEN プロジェクト名が空文字またはホワイトスペースのみの場合、THE Project_API SHALL バリデーションエラーを返却し、プロジェクトを作成しない
3. WHEN プロジェクト名が255文字を超える場合、THE Project_API SHALL バリデーションエラーを返却する
4. THE Project_API SHALL プロジェクト作成時にcreated_atとupdated_atを現在時刻で自動設定する

### 要件 2: プロジェクト一覧取得

**ユーザーストーリー:** 解析担当者として、既存のプロジェクト一覧を確認したい。解析対象を選択するためである。

#### 受け入れ基準

1. WHEN ユーザーがプロジェクト一覧を要求した場合、THE Project_API SHALL ページネーション付きでプロジェクト一覧を返却する
2. WHEN pageまたはper_pageパラメータが指定された場合、THE Project_API SHALL 指定されたページのプロジェクトと総件数を返却する
3. WHEN pageまたはper_pageが未指定の場合、THE Project_API SHALL デフォルト値（page=1, per_page=20）を使用する
4. THE Project_API SHALL プロジェクト一覧をcreated_atの降順で返却する