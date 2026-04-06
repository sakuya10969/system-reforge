# 要件定義書

## はじめに

System Reforgeにおける依存関係・フロー可視化機能の要件を定義する。解析ジョブの結果として生成された依存関係データ（DependencyEdge）をグラフ表示し、プログラム間の呼び出し関係や処理フローを可視化する機能である。バックエンド（FastAPI + PostgreSQL）とフロントエンド（React + Mantine + React Flow）の両方をカバーする。

## 用語集

- **DependencyEdge**: 依存関係を表すエンティティ。source_file_idからtarget_file_idへの依存（CALL / COPY / INCLUDE等）を表現する
- **Dependency_API**: 依存関係グラフデータおよび処理フローデータを提供するREST APIエンドポイント群
- **DependencyEdge_Repository**: 依存関係データの永続化を担うリポジトリインターフェース
- **Flow_Graph_Widget**: React Flowベースの依存関係グラフ可視化ウィジェット
- **Dependencies_Page**: 依存関係可視化ページ。グラフ表示とフィルタリングを提供する
- **Graph_Node**: React Flowのノード。ソースファイルを表現する
- **Graph_Edge**: React Flowのエッジ。依存関係（DependencyEdge）を表現する
- **SourceFile**: 解析対象のソースファイルエンティティ（既存。id, project_id, file_path, language等を持つ）

## 要件

### 要件 1: 依存関係データ取得API

**ユーザーストーリー:** 解析担当者として、解析ジョブの依存関係データを取得したい。プログラム間の呼び出し関係をグラフで可視化するためである。

#### 受け入れ基準

1. WHEN ユーザーが有効なjob_idで依存関係データを要求した場合、THE Dependency_API SHALL 該当ジョブの全DependencyEdgeをノード（ソースファイル）とエッジ（依存関係）の形式で返却する
2. WHEN 存在しないjob_idが指定された場合、THE Dependency_API SHALL エラーコード"NOT_FOUND"を返却する
3. WHEN ジョブに依存関係データが存在しない場合、THE Dependency_API SHALL 空のノード配列と空のエッジ配列を返却する
4. THE Dependency_API SHALL 各ノードにソースファイルのid、file_path、languageを含める
5. THE Dependency_API SHALL 各エッジにsource_file_id、target_file_id、dependency_type、metadataを含める

### 要件 2: 処理フローデータ取得API

**ユーザーストーリー:** 解析担当者として、解析ジョブの処理フローデータを取得したい。プログラムの実行順序と呼び出し階層を把握するためである。

#### 受け入れ基準

1. WHEN ユーザーが有効なjob_idで処理フローデータを要求した場合、THE Dependency_API SHALL 依存関係データをツリー構造（呼び出し階層）に変換して返却する
2. WHEN 存在しないjob_idが指定された場合、THE Dependency_API SHALL エラーコード"NOT_FOUND"を返却する
3. WHEN ジョブにフローデータが存在しない場合、THE Dependency_API SHALL 空のフローデータを返却する
4. THE Dependency_API SHALL フローデータの各ノードにソースファイル情報と呼び出し先リストを含める

### 要件 3: ソースファイル一覧取得API

**ユーザーストーリー:** 解析担当者として、解析ジョブに含まれるソースファイル一覧を取得したい。依存関係グラフのノード情報として利用するためである。

#### 受け入れ基準

1. WHEN ユーザーが有効なjob_idでソースファイル一覧を要求した場合、THE Dependency_API SHALL 該当ジョブのプロジェクトに属するソースファイル一覧を返却する
2. WHEN 存在しないjob_idが指定された場合、THE Dependency_API SHALL エラーコード"NOT_FOUND"を返却する

### 要件 4: DependencyEdgeドメインモデル

**ユーザーストーリー:** システムとして、依存関係データを正しく管理したい。データの整合性を保証するためである。

#### 受け入れ基準

1. THE DependencyEdge SHALL id、job_id、source_file_id、target_file_id、dependency_type、metadataの属性を持つ
2. THE DependencyEdge SHALL dependency_typeとして"CALL"、"COPY"、"INCLUDE"のいずれかを受け入れる
3. WHEN source_file_idとtarget_file_idが同一の場合、THE DependencyEdge SHALL 自己参照として有効な依存関係として扱う

### 要件 5: レスポンス形式

**ユーザーストーリー:** フロントエンド開発者として、統一されたAPIレスポンス形式を利用したい。レスポンスの解析処理を共通化するためである。

#### 受け入れ基準

1. THE Dependency_API SHALL 成功レスポンスを `{"data": {...}}` 形式で返却する
2. THE Dependency_API SHALL エラーレスポンスを `{"error": {"code": "...", "message": "..."}}` 形式で返却する
3. THE Dependency_API SHALL 依存関係グラフレスポンスを `{"data": {"nodes": [...], "edges": [...]}}` 形式で返却する

### 要件 6: 依存関係グラフ可視化（フロントエンド）

**ユーザーストーリー:** 解析担当者として、依存関係をインタラクティブなグラフで確認したい。プログラム間の関係を視覚的に把握するためである。

#### 受け入れ基準

1. WHEN ユーザーが依存関係ページにアクセスした場合、THE Dependencies_Page SHALL APIから依存関係データを取得しReact Flowでグラフを表示する
2. WHEN グラフが表示された場合、THE Flow_Graph_Widget SHALL 各ノードにファイル名と言語を表示する
3. WHEN グラフが表示された場合、THE Flow_Graph_Widget SHALL 各エッジに依存関係タイプ（CALL / COPY / INCLUDE）をラベルとして表示する
4. WHEN ユーザーがノードをドラッグした場合、THE Flow_Graph_Widget SHALL ノードの位置を更新しグラフレイアウトを維持する
5. WHEN ユーザーがグラフをズームまたはパンした場合、THE Flow_Graph_Widget SHALL ビューポートを更新する
6. WHEN 依存関係データが0件の場合、THE Dependencies_Page SHALL 空状態のメッセージを表示する

### 要件 7: 依存関係タイプフィルタリング（フロントエンド）

**ユーザーストーリー:** 解析担当者として、依存関係タイプでグラフをフィルタリングしたい。特定の関係（CALL / COPY / INCLUDE）に絞って確認するためである。

#### 受け入れ基準

1. WHEN ユーザーが依存関係タイプのフィルタを選択した場合、THE Flow_Graph_Widget SHALL 選択されたタイプのエッジのみを表示する
2. WHEN フィルタが解除された場合、THE Flow_Graph_Widget SHALL 全エッジを表示する
3. WHEN フィルタ適用後にエッジが0件になった場合、THE Flow_Graph_Widget SHALL フィルタ結果が空であることを示すメッセージを表示する

### 要件 8: グラフレイアウト（フロントエンド）

**ユーザーストーリー:** 解析担当者として、グラフが自動的に見やすくレイアウトされてほしい。手動でノードを配置する手間を省くためである。

#### 受け入れ基準

1. WHEN グラフが初期表示される場合、THE Flow_Graph_Widget SHALL 自動レイアウトアルゴリズムでノードを配置する
2. WHEN ユーザーが「レイアウトリセット」ボタンをクリックした場合、THE Flow_Graph_Widget SHALL 自動レイアウトを再適用する

### 要件 9: ローディング・エラー状態（フロントエンド）

**ユーザーストーリー:** 解析担当者として、データ取得中やエラー時に適切なフィードバックを受けたい。操作状態を把握するためである。

#### 受け入れ基準

1. WHEN API通信中の場合、THE Dependencies_Page SHALL ローディング状態を表示する
2. WHEN API通信でエラーが発生した場合、THE Dependencies_Page SHALL エラーメッセージを表示する
