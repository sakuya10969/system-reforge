# 要件定義書

## はじめに

System Reforgeにおける要件レビュー・エクスポート機能の要件を定義する。業務ルール抽出機能によって生成された要件定義データを一覧表示し、レビュー・編集・ステータス管理を行い、Markdown形式でエクスポートする機能である。バックエンド（FastAPI + PostgreSQL）とフロントエンド（React + Mantine + React Hook Form + Zod + React Markdown）の両方をカバーする。

## 用語集

- **Requirement**: 要件を表すエンティティ。id, job_id, title, description, category, priority, status, source_rules, created_at, updated_atを持つ
- **Requirement_API**: 要件の一覧取得・編集・エクスポートを提供するREST APIエンドポイント
- **Requirement_Repository**: 要件の永続化を担うリポジトリインターフェース
- **Requirements_Page**: 要件レビューページ。要件一覧の表示・編集・エクスポートを行う
- **Requirement_Editor**: React Hook Form + Zodベースの要件編集フォームコンポーネント
- **Markdown_Exporter**: 要件一覧をMarkdown形式に変換するサービス
- **Markdown_Preview**: React Markdownを使用したMarkdownプレビューコンポーネント
- **Requirement_Status**: 要件のステータスを表す列挙値（draft / reviewed / approved）
- **Requirement_Priority**: 要件の優先度を表す列挙値（high / medium / low）

## 要件

### 要件 1: 要件一覧取得API

**ユーザーストーリー:** 解析担当者として、解析ジョブの要件一覧を取得したい。業務ルールから生成された要件定義を確認するためである。

#### 受け入れ基準

1. WHEN ユーザーが有効なjob_idで要件一覧を要求した場合、THE Requirement_API SHALL 該当ジョブの全要件をcreated_atの昇順で返却する
2. WHEN 存在しないjob_idが指定された場合、THE Requirement_API SHALL HTTPステータス404とエラーコード"NOT_FOUND"を返却する
3. WHEN ジョブに要件が存在しない場合、THE Requirement_API SHALL 空の配列を返却する

### 要件 2: 要件編集API

**ユーザーストーリー:** 解析担当者として、要件の内容を編集したい。抽出された要件を正確な表現に修正するためである。

#### 受け入れ基準

1. WHEN ユーザーが有効なrequirement_idとリクエストボディで要件を更新した場合、THE Requirement_API SHALL title、description、category、priority、statusを更新し、updated_atを現在時刻に設定して返却する
2. WHEN 存在しないrequirement_idが指定された場合、THE Requirement_API SHALL HTTPステータス404とエラーコード"NOT_FOUND"を返却する
3. WHEN titleが空文字列またはホワイトスペースのみで送信された場合、THE Requirement_API SHALL HTTPステータス422とバリデーションエラーを返却する
4. WHEN descriptionが空文字列またはホワイトスペースのみで送信された場合、THE Requirement_API SHALL HTTPステータス422とバリデーションエラーを返却する
5. WHEN priorityに無効な値が指定された場合、THE Requirement_API SHALL HTTPステータス422とバリデーションエラーを返却する
6. WHEN statusに無効な値が指定された場合、THE Requirement_API SHALL HTTPステータス422とバリデーションエラーを返却する

### 要件 3: 要件エクスポートAPI

**ユーザーストーリー:** 解析担当者として、要件一覧をMarkdown形式でエクスポートしたい。要件定義書として外部に共有するためである。

#### 受け入れ基準

1. WHEN ユーザーが有効なjob_idでエクスポートを要求した場合、THE Requirement_API SHALL 該当ジョブの全要件をMarkdown形式の文字列として返却する
2. WHEN エクスポートされたMarkdownに要件が含まれる場合、THE Markdown_Exporter SHALL 各要件のtitle、description、category、priority、statusを含むMarkdownテキストを生成する
3. WHEN 存在しないjob_idが指定された場合、THE Requirement_API SHALL HTTPステータス404とエラーコード"NOT_FOUND"を返却する
4. WHEN ジョブに要件が存在しない場合、THE Markdown_Exporter SHALL ヘッダーのみのMarkdownテキストを生成する

### 要件 4: Requirementドメインモデル

**ユーザーストーリー:** システムとして、要件データを正しく管理したい。データの整合性を保証するためである。

#### 受け入れ基準

1. THE Requirement SHALL id、job_id、title、description、category、priority、status、source_rules、created_at、updated_atの属性を持つ
2. THE Requirement SHALL statusとして"draft"、"reviewed"、"approved"のいずれかを受け入れる
3. THE Requirement SHALL priorityとして"high"、"medium"、"low"またはNoneを受け入れる
4. THE Requirement SHALL titleが空文字列またはホワイトスペースのみの場合にバリデーションエラーを発生させる
5. THE Requirement SHALL descriptionが空文字列またはホワイトスペースのみの場合にバリデーションエラーを発生させる

### 要件 5: Markdownエクスポート形式

**ユーザーストーリー:** 解析担当者として、エクスポートされたMarkdownが読みやすい形式であることを期待する。要件定義書として利用するためである。

#### 受け入れ基準

1. THE Markdown_Exporter SHALL エクスポートされたMarkdownの先頭に「# 要件定義書」のヘッダーを含める
2. THE Markdown_Exporter SHALL 各要件をMarkdownの見出し（##）とリスト形式で出力する
3. THE Markdown_Exporter SHALL 各要件のtitle、description、category、priority、statusをすべて含める
4. FOR ALL 有効なRequirementリストに対して、Markdown_Exporterで生成したMarkdownをパースした場合、元の要件数と同数の要件セクションが含まれること（ラウンドトリップ特性）

### 要件 6: 要件一覧表示（フロントエンド）

**ユーザーストーリー:** 解析担当者として、要件一覧をページ上で確認したい。生成された要件定義をレビューするためである。

#### 受け入れ基準

1. WHEN ユーザーが要件レビューページにアクセスした場合、THE Requirements_Page SHALL APIから要件一覧を取得して表示する
2. THE Requirements_Page SHALL 各要件のtitle、category、priority、statusを一覧形式で表示する
3. THE Requirements_Page SHALL statusに応じたバッジ色分け表示を行う（draft: グレー、reviewed: 青、approved: 緑）
4. THE Requirements_Page SHALL priorityに応じたバッジ色分け表示を行う（high: 赤、medium: 黄、low: 青）
5. WHEN 要件が0件の場合、THE Requirements_Page SHALL 空状態のメッセージを表示する
6. WHEN API通信中の場合、THE Requirements_Page SHALL ローディング状態を表示する
7. WHEN API通信でエラーが発生した場合、THE Requirements_Page SHALL エラーメッセージを表示する

### 要件 7: 要件編集フォーム（フロントエンド）

**ユーザーストーリー:** 解析担当者として、要件をフォームで編集したい。要件の内容やステータスを修正するためである。

#### 受け入れ基準

1. WHEN ユーザーが要件の編集ボタンをクリックした場合、THE Requirement_Editor SHALL 現在の要件データをフォームに表示する
2. THE Requirement_Editor SHALL React Hook FormとZodスキーマを使用してフォームバリデーションを実行する
3. WHEN titleが空の状態で送信した場合、THE Requirement_Editor SHALL バリデーションエラーメッセージを表示する
4. WHEN descriptionが空の状態で送信した場合、THE Requirement_Editor SHALL バリデーションエラーメッセージを表示する
5. WHEN ユーザーが有効なデータで送信した場合、THE Requirement_Editor SHALL APIを呼び出して要件を更新し、一覧を再取得する
6. WHEN API更新が成功した場合、THE Requirement_Editor SHALL 成功通知を表示してフォームを閉じる
7. WHEN API更新が失敗した場合、THE Requirement_Editor SHALL エラー通知を表示する

### 要件 8: Markdownプレビュー（フロントエンド）

**ユーザーストーリー:** 解析担当者として、エクスポート前にMarkdownのプレビューを確認したい。出力内容を事前に確認するためである。

#### 受け入れ基準

1. WHEN ユーザーがエクスポートボタンをクリックした場合、THE Requirements_Page SHALL エクスポートAPIを呼び出してMarkdownプレビューを表示する
2. THE Markdown_Preview SHALL React Markdownを使用してMarkdownテキストをレンダリングする
3. WHEN ユーザーがダウンロードボタンをクリックした場合、THE Requirements_Page SHALL Markdownテキストを.mdファイルとしてダウンロードする

### 要件 9: レスポンス形式

**ユーザーストーリー:** フロントエンド開発者として、統一されたAPIレスポンス形式を利用したい。レスポンスの解析処理を共通化するためである。

#### 受け入れ基準

1. THE Requirement_API SHALL 成功レスポンスを `{"data": ...}` 形式で返却する
2. THE Requirement_API SHALL エラーレスポンスを `{"error": {"code": "...", "message": "..."}}` 形式で返却する
3. THE Requirement_API SHALL エクスポートレスポンスを `{"data": {"markdown": "..."}}` 形式で返却する
