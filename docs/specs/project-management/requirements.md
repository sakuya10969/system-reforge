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

### 要件 3: プロジェクト詳細取得

**ユーザーストーリー:** 解析担当者として、特定のプロジェクトの詳細情報を確認したい。プロジェクトの状態を把握するためである。

#### 受け入れ基準

1. WHEN 有効なproject_idが指定された場合、THE Project_API SHALL 該当プロジェクトの全属性を返却する
2. WHEN 存在しないproject_idが指定された場合、THE Project_API SHALL エラーコード"NOT_FOUND"とメッセージを返却する
3. WHEN 不正な形式のproject_idが指定された場合、THE Project_API SHALL バリデーションエラーを返却する

### 要件 4: プロジェクト削除

**ユーザーストーリー:** 解析担当者として、不要なプロジェクトを削除したい。管理対象を整理するためである。

#### 受け入れ基準

1. WHEN 有効なproject_idで削除が要求された場合、THE Project_API SHALL 該当プロジェクトをデータベースから削除する
2. WHEN 存在しないproject_idで削除が要求された場合、THE Project_API SHALL エラーコード"NOT_FOUND"を返却する

### 要件 5: プロジェクト一覧ページ（フロントエンド）

**ユーザーストーリー:** 解析担当者として、ブラウザ上でプロジェクト一覧を閲覧・操作したい。直感的にプロジェクトを管理するためである。

#### 受け入れ基準

1. WHEN ユーザーがプロジェクト一覧ページにアクセスした場合、THE Project_List_Page SHALL APIからプロジェクト一覧を取得して表示する
2. WHEN プロジェクトが0件の場合、THE Project_List_Page SHALL 空状態のメッセージを表示する
3. WHEN ユーザーが「新規作成」ボタンをクリックした場合、THE Project_List_Page SHALL プロジェクト作成フォームを表示する
4. WHEN ユーザーがプロジェクトの削除ボタンをクリックした場合、THE Project_List_Page SHALL 確認ダイアログを表示し、確認後にAPIで削除を実行して一覧を更新する
5. WHEN API通信中の場合、THE Project_List_Page SHALL ローディング状態を表示する
6. WHEN API通信でエラーが発生した場合、THE Project_List_Page SHALL エラーメッセージを表示する

### 要件 6: プロジェクト作成フォーム（フロントエンド）

**ユーザーストーリー:** 解析担当者として、フォームからプロジェクトを作成したい。必要な情報を入力して登録するためである。

#### 受け入れ基準

1. WHEN ユーザーがフォームに有効な情報を入力して送信した場合、THE Project_Form SHALL APIにプロジェクト作成リクエストを送信し、成功後に一覧ページに遷移する
2. WHEN プロジェクト名が未入力の場合、THE Project_Form SHALL バリデーションエラーを表示し、送信を防止する
3. WHEN API通信でエラーが発生した場合、THE Project_Form SHALL エラーメッセージを表示する

### 要件 7: レスポンス形式

**ユーザーストーリー:** フロントエンド開発者として、統一されたAPIレスポンス形式を利用したい。レスポンスの解析処理を共通化するためである。

#### 受け入れ基準

1. THE Project_API SHALL 成功レスポンスを `{"data": {...}}` 形式で返却する
2. THE Project_API SHALL エラーレスポンスを `{"error": {"code": "...", "message": "..."}}` 形式で返却する
3. THE Project_API SHALL 一覧レスポンスを `{"data": [...], "pagination": {"total": N, "page": N, "per_page": N}}` 形式で返却する
