# 要件定義書

## はじめに

System Reforgeにおける業務ルール抽出機能の要件を定義する。解析ジョブの結果として生成された構造化中間データ（AST、依存関係、フロー情報）からLLMを使用して業務ルール（条件分岐・計算ロジック・バリデーション）を抽出し、自然言語で記述する機能である。バックエンド（FastAPI + PostgreSQL + LLMクライアント）とフロントエンド（React + Mantine + TanStack Table）の両方をカバーする。

## 用語集

- **BusinessRule**: 業務ルールを表すエンティティ。id, job_id, source_file_id, rule_type, description, source_location, raw_logic, created_atを持つ
- **BusinessRule_API**: 業務ルールの一覧取得を提供するREST APIエンドポイント
- **BusinessRule_Repository**: 業務ルールの永続化を担うリポジトリインターフェース
- **MeaningExtraction_Service**: 構造化中間データからLLMを使用して業務ルールを抽出するドメインサービス
- **LLM_Client**: LLM APIとの通信を担うインフラストラクチャコンポーネント（インターフェースで抽象化）
- **Rule_Table_Widget**: TanStack Tableベースの業務ルール一覧表示ウィジェット
- **Analysis_Page**: 解析結果ページ。既存ページに業務ルールタブを追加する
- **Rule_Type**: 業務ルールの種別を表す列挙値（condition / calculation / validation）
- **Intermediate_Data**: 解析ジョブが生成した構造化中間データ（AST、依存関係、フロー情報）。LLMへの入力として使用される

## 要件

### 要件 1: 業務ルール抽出処理

**ユーザーストーリー:** システムとして、解析ジョブ完了後に構造化中間データから業務ルールを抽出したい。レガシーコードの業務ロジックを自然言語で記述するためである。

#### 受け入れ基準

1. WHEN 解析ジョブが完了した場合、THE MeaningExtraction_Service SHALL 構造化中間データ（AST、依存関係、フロー情報）をLLM_Clientに渡して業務ルールを抽出する
2. THE MeaningExtraction_Service SHALL ソースコードを直接LLM_Clientに渡さず、構造化中間データのみを入力として使用する
3. WHEN LLM_Clientが業務ルールを返却した場合、THE MeaningExtraction_Service SHALL 各ルールにrule_type（condition / calculation / validation）を分類して返却する
4. WHEN LLM_Clientとの通信でエラーが発生した場合、THE MeaningExtraction_Service SHALL エラーを記録し、抽出済みのルールを保持した上でエラーを報告する
5. THE MeaningExtraction_Service SHALL 抽出した業務ルールをBusinessRule_Repositoryを通じてDBに一括保存する

### 要件 2: LLMクライアント

**ユーザーストーリー:** システムとして、LLM APIとの通信を抽象化したい。LLMプロバイダの変更に柔軟に対応するためである。

#### 受け入れ基準

1. THE LLM_Client SHALL インターフェース（抽象クラス）として定義され、具体的なLLMプロバイダに依存しない
2. THE LLM_Client SHALL 構造化中間データを受け取り、抽出された業務ルールのリストを返却するメソッドを提供する
3. THE LLM_Client SHALL スタブ実装を提供し、固定の業務ルールデータを返却する

### 要件 3: 業務ルール一覧取得API

**ユーザーストーリー:** 解析担当者として、解析ジョブの業務ルール一覧を取得したい。抽出された業務ロジックを確認するためである。

#### 受け入れ基準

1. WHEN ユーザーが有効なjob_idで業務ルール一覧を要求した場合、THE BusinessRule_API SHALL 該当ジョブの全業務ルールをcreated_atの昇順で返却する
2. WHEN 存在しないjob_idが指定された場合、THE BusinessRule_API SHALL エラーコード"NOT_FOUND"を返却する
3. WHEN ジョブに業務ルールが存在しない場合、THE BusinessRule_API SHALL 空の配列を返却する
4. WHEN rule_typeクエリパラメータが指定された場合、THE BusinessRule_API SHALL 指定されたrule_typeの業務ルールのみを返却する

### 要件 4: BusinessRuleドメインモデル

**ユーザーストーリー:** システムとして、業務ルールデータを正しく管理したい。データの整合性を保証するためである。

#### 受け入れ基準

1. THE BusinessRule SHALL id、job_id、source_file_id、rule_type、description、source_location、raw_logic、created_atの属性を持つ
2. THE BusinessRule SHALL rule_typeとして"condition"、"calculation"、"validation"のいずれかを受け入れる
3. THE BusinessRule SHALL descriptionが空文字列の場合にバリデーションエラーを発生させる
4. THE BusinessRule SHALL source_locationをJSONB形式（line_start, line_end, section等）で保持する

### 要件 5: レスポンス形式

**ユーザーストーリー:** フロントエンド開発者として、統一されたAPIレスポンス形式を利用したい。レスポンスの解析処理を共通化するためである。

#### 受け入れ基準

1. THE BusinessRule_API SHALL 成功レスポンスを `{"data": [...]}` 形式で返却する
2. THE BusinessRule_API SHALL エラーレスポンスを `{"error": {"code": "...", "message": "..."}}` 形式で返却する

### 要件 6: 業務ルールテーブル表示（フロントエンド）

**ユーザーストーリー:** 解析担当者として、業務ルール一覧をテーブル形式で確認したい。抽出された業務ロジックを一覧で把握するためである。

#### 受け入れ基準

1. WHEN ユーザーが解析結果ページの業務ルールタブにアクセスした場合、THE Analysis_Page SHALL APIから業務ルール一覧を取得してRule_Table_Widgetで表示する
2. THE Rule_Table_Widget SHALL 各業務ルールのrule_type、description、ソースファイル名、source_locationをテーブル形式で表示する
3. THE Rule_Table_Widget SHALL rule_typeに応じたバッジ色分け表示を行う（condition: 青、calculation: 緑、validation: オレンジ）
4. WHEN 業務ルールが0件の場合、THE Rule_Table_Widget SHALL 空状態のメッセージを表示する
5. WHEN API通信中の場合、THE Analysis_Page SHALL ローディング状態を表示する
6. WHEN API通信でエラーが発生した場合、THE Analysis_Page SHALL エラーメッセージを表示する

### 要件 7: 業務ルールフィルタリング（フロントエンド）

**ユーザーストーリー:** 解析担当者として、業務ルールをrule_typeでフィルタリングしたい。特定の種別（条件分岐・計算・バリデーション）に絞って確認するためである。

#### 受け入れ基準

1. WHEN ユーザーがrule_typeフィルタを選択した場合、THE Rule_Table_Widget SHALL 選択されたrule_typeの業務ルールのみを表示する
2. WHEN フィルタが解除された場合、THE Rule_Table_Widget SHALL 全業務ルールを表示する
3. THE Rule_Table_Widget SHALL TanStack Tableのカラムフィルタ機能を使用してフィルタリングを実装する

### 要件 8: 業務ルールテーブルのソート（フロントエンド）

**ユーザーストーリー:** 解析担当者として、業務ルールテーブルをソートしたい。特定の基準で並べ替えて確認するためである。

#### 受け入れ基準

1. WHEN ユーザーがカラムヘッダーをクリックした場合、THE Rule_Table_Widget SHALL 該当カラムで昇順・降順のソートを切り替える
2. THE Rule_Table_Widget SHALL TanStack Tableのソート機能を使用してソートを実装する
