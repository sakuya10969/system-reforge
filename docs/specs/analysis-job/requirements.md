# 要件定義書

## はじめに

System Reforgeにおける解析ジョブ管理機能の要件を定義する。アップロード済みのソースコードに対して非同期で解析ジョブを作成・実行し、その進捗とステータスを管理する機能である。バックエンド（FastAPI + PostgreSQL + BackgroundTasks）とフロントエンド（React + Mantine + React Query）の両方をカバーする。

## 用語集

- **AnalysisJob**: 解析ジョブを表すエンティティ。id, project_id, status, started_at, completed_at, error_message, created_atを持つ
- **Job_API**: 解析ジョブの作成・一覧取得・詳細取得を提供するREST APIエンドポイント群
- **Job_Worker**: FastAPI BackgroundTasksで非同期に解析処理を実行するワーカーコンポーネント
- **AnalysisJob_Repository**: 解析ジョブの永続化を担うリポジトリインターフェース
- **Analysis_Service**: ソースコードのパース・構造化中間データ生成を担うドメインサービス
- **Job_List_Widget**: ジョブ一覧を表示するフロントエンドウィジェット
- **Analysis_Page**: 解析結果ページ。ジョブ一覧と状態監視を提供する
- **Job_Status**: ジョブの状態を表す列挙値（pending, running, completed, failed）

## 要件

### 要件 1: 解析ジョブ作成API

**ユーザーストーリー:** 解析担当者として、プロジェクトに対して解析ジョブを作成・開始したい。アップロード済みのソースコードを非同期で解析するためである。

#### 受け入れ基準

1. WHEN ユーザーが有効なproject_idで解析ジョブ作成を要求した場合、THE Job_API SHALL UUIDを生成し、statusを"pending"に設定し、ジョブをDBに保存して、作成されたジョブデータを即座に返却する
2. WHEN 解析ジョブが作成された場合、THE Job_API SHALL FastAPI BackgroundTasksを使用してJob_Workerに解析処理を非同期で委譲する
3. WHEN 存在しないproject_idが指定された場合、THE Job_API SHALL エラーコード"NOT_FOUND"を返却する
4. WHEN プロジェクトにソースファイルが登録されていない場合、THE Job_API SHALL エラーコード"NO_SOURCE_FILES"とメッセージを返却しジョブを作成しない

### 要件 2: 解析ジョブ一覧取得API

**ユーザーストーリー:** 解析担当者として、プロジェクトの解析ジョブ一覧を確認したい。過去の解析履歴と現在の進捗を把握するためである。

#### 受け入れ基準

1. WHEN ユーザーが有効なproject_idでジョブ一覧を要求した場合、THE Job_API SHALL 該当プロジェクトのジョブ一覧をcreated_atの降順で返却する
2. WHEN 存在しないproject_idが指定された場合、THE Job_API SHALL エラーコード"NOT_FOUND"を返却する
3. WHEN プロジェクトにジョブが存在しない場合、THE Job_API SHALL 空の配列を返却する

### 要件 3: 解析ジョブ詳細取得API

**ユーザーストーリー:** 解析担当者として、特定の解析ジョブの詳細とステータスを確認したい。解析の進捗状況を監視するためである。

#### 受け入れ基準

1. WHEN 有効なjob_idが指定された場合、THE Job_API SHALL 該当ジョブの全属性（id, project_id, status, started_at, completed_at, error_message, created_at）を返却する
2. WHEN 存在しないjob_idが指定された場合、THE Job_API SHALL エラーコード"NOT_FOUND"とメッセージを返却する

### 要件 4: 解析ワーカー処理

**ユーザーストーリー:** システムとして、バックグラウンドで解析処理を実行したい。APIのレスポンスをブロックせずにソースコードを解析するためである。

#### 受け入れ基準

1. WHEN Job_Workerが解析処理を開始した場合、THE Job_Worker SHALL ジョブのstatusを"running"に更新し、started_atを現在時刻に設定する
2. WHEN Job_Workerが解析処理を正常に完了した場合、THE Job_Worker SHALL ジョブのstatusを"completed"に更新し、completed_atを現在時刻に設定する
3. WHEN Job_Workerの解析処理中にエラーが発生した場合、THE Job_Worker SHALL ジョブのstatusを"failed"に更新し、error_messageにエラー内容を設定する
4. THE Job_Worker SHALL Analysis_Serviceを呼び出してソースコードの構造化中間データを生成する
5. WHILE ジョブのstatusが"pending"の場合、THE Job_Worker SHALL 解析処理を開始可能な状態として扱う

### 要件 5: ステータス遷移

**ユーザーストーリー:** システムとして、ジョブのステータスを正しく遷移させたい。不正な状態遷移を防止するためである。

#### 受け入れ基準

1. THE AnalysisJob SHALL statusの遷移をpending→running→completedまたはpending→running→failedのみ許可する
2. WHEN 不正なステータス遷移が試みられた場合、THE AnalysisJob SHALL 遷移を拒否しエラーを発生させる

### 要件 6: レスポンス形式

**ユーザーストーリー:** フロントエンド開発者として、統一されたAPIレスポンス形式を利用したい。レスポンスの解析処理を共通化するためである。

#### 受け入れ基準

1. THE Job_API SHALL 成功レスポンスを `{"data": {...}}` 形式で返却する
2. THE Job_API SHALL エラーレスポンスを `{"error": {"code": "...", "message": "..."}}` 形式で返却する
3. THE Job_API SHALL 一覧レスポンスを `{"data": [...]}` 形式で返却する

### 要件 7: 解析ページ（フロントエンド）

**ユーザーストーリー:** 解析担当者として、ブラウザ上で解析ジョブの状態を監視したい。解析の進捗をリアルタイムに把握するためである。

#### 受け入れ基準

1. WHEN ユーザーが解析ページにアクセスした場合、THE Analysis_Page SHALL APIからジョブ一覧を取得して表示する
2. WHEN ユーザーが「解析開始」ボタンをクリックした場合、THE Analysis_Page SHALL APIでジョブ作成を実行し、ジョブ一覧を更新する
3. WHILE ジョブのstatusが"pending"または"running"の場合、THE Analysis_Page SHALL ポーリング（5秒間隔）でジョブ状態を監視し表示を更新する
4. WHEN ジョブのstatusが"completed"に変わった場合、THE Analysis_Page SHALL ポーリングを停止し完了状態を表示する
5. WHEN ジョブのstatusが"failed"に変わった場合、THE Analysis_Page SHALL ポーリングを停止しエラーメッセージを表示する
6. WHEN API通信中の場合、THE Analysis_Page SHALL ローディング状態を表示する
7. WHEN API通信でエラーが発生した場合、THE Analysis_Page SHALL エラーメッセージを表示する

### 要件 8: ジョブ一覧ウィジェット（フロントエンド）

**ユーザーストーリー:** 解析担当者として、ジョブ一覧をテーブル形式で確認したい。各ジョブのステータスと時刻を一目で把握するためである。

#### 受け入れ基準

1. THE Job_List_Widget SHALL 各ジョブのステータス、作成日時、開始日時、完了日時、エラーメッセージをテーブル形式で表示する
2. WHEN ジョブが0件の場合、THE Job_List_Widget SHALL 空状態のメッセージを表示する
3. THE Job_List_Widget SHALL ステータスに応じた色分け表示を行う（pending: グレー、running: 青、completed: 緑、failed: 赤）
