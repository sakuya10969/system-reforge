# 実装計画: 依存関係・フロー可視化

## 概要

依存関係・フロー可視化機能の実装。バックエンド（FastAPI + SQLAlchemy + PostgreSQL）で依存関係データのAPI提供を、フロントエンド（React + Mantine + React Flow + dagre）でインタラクティブなグラフ可視化を実装する。analysis-job仕様が実装済みの前提で、既存のAnalysisJob・SourceFileコンポーネントを活用する。

## タスク

- [x] 1. ドメイン層の実装
  - [x] 1.1 DependencyEdgeエンティティとDependencyType列挙型を実装する
    - `server/domain/models/dependency_edge.py` を作成
    - DependencyType列挙型（CALL, COPY, INCLUDE）を定義
    - DependencyEdgeデータクラスを定義（id, job_id, source_file_id, target_file_id, dependency_type, metadata）
    - _Requirements: 4.1, 4.2_
  - [ ]* 1.2 DependencyEdgeドメインモデルのプロパティテストを実装する
    - **Property 4: DependencyEdgeドメインモデルの妥当性**
    - Hypothesisで任意のDependencyEdgeを生成し、dependency_typeが有効な値のみであることを検証
    - **Validates: Requirements 4.1, 4.2**
  - [x] 1.3 DependencyEdgeRepositoryインターフェースを実装する
    - `server/domain/repositories/dependency_edge_repository.py` を作成
    - find_by_job、create_manyメソッドを定義
    - _Requirements: 1.1_

- [x] 2. インフラストラクチャ層の実装
  - [x] 2.1 DependencyEdgeModelを追加する
    - `server/infrastructure/database/models.py` にDependencyEdgeModelを追加
    - job_idにインデックスを設定
    - _Requirements: 1.1, 4.1_
  - [x] 2.2 Alembicマイグレーションを作成する
    - dependency_edgesテーブルの作成マイグレーションを生成
    - _Requirements: 1.1_
  - [x] 2.3 SQLAlchemyDependencyEdgeRepositoryを実装する
    - `server/infrastructure/database/repositories/dependency_edge_repository.py` を作成
    - DependencyEdgeModel ↔ DependencyEdge のマッピング
    - find_by_jobはjob_idでフィルタ
    - _Requirements: 1.1_

- [x] 3. チェックポイント - ドメイン層・インフラ層の確認
  - すべてのテストが通ることを確認し、不明点があればユーザーに質問する。

- [x] 4. アプリケーション層の実装
  - [x] 4.1 GetDependencyGraphUseCaseを実装する
    - `server/application/analysis/get_dependency_graph.py` を作成
    - GraphNode、GraphEdge、DependencyGraphResultデータクラスを定義
    - ジョブ存在確認、依存関係データ取得、ソースファイル取得、ノード・エッジ形式への変換
    - _Requirements: 1.1, 1.2, 1.4, 1.5_
  - [ ]* 4.2 GetDependencyGraphUseCaseのプロパティテストを実装する
    - **Property 1: 依存関係データのラウンドトリップ**
    - 任意のソースファイル群とDependencyEdge群を生成し、変換結果のnodes/edgesが入力データと一致することを検証
    - **Validates: Requirements 1.1, 1.4, 1.5**
  - [x] 4.3 GetFlowDataUseCaseを実装する
    - `server/application/analysis/get_flow_data.py` を作成
    - FlowNode、FlowDataResultデータクラスを定義
    - 依存関係データからツリー構造への変換ロジック（ルートノード特定、再帰的ツリー構築）
    - _Requirements: 2.1, 2.4_
  - [ ]* 4.4 GetFlowDataUseCaseのプロパティテストを実装する
    - **Property 3: フローデータのツリー構造整合性**
    - 任意の依存関係エッジ集合を生成し、ツリー構造のルートノードが他から呼ばれていないことを検証
    - **Validates: Requirements 2.1, 2.4**
  - [x] 4.5 GetSourceFilesForJobUseCaseを実装する
    - `server/application/analysis/get_source_files_for_job.py` を作成
    - ジョブ存在確認、project_idからソースファイル一覧取得
    - _Requirements: 3.1, 3.2_

- [x] 5. API層の実装
  - [x] 5.1 Pydanticスキーマを実装する
    - `server/api/schemas/analysis.py` に追加（または新規作成）
    - GraphNodeResponse、GraphEdgeResponse、DependencyGraphResponse、DependencyGraphDataを定義
    - FlowNodeResponse、FlowDataResponse、FlowDataDataを定義
    - SourceFileResponse、SourceFileListResponseを定義
    - _Requirements: 5.1, 5.2, 5.3_
  - [x] 5.2 依存関係ルーターを実装する
    - `server/api/routes/analysis.py` に追加（または新規作成）
    - GET /api/v1/jobs/{job_id}/source-files（ソースファイル一覧）
    - GET /api/v1/jobs/{job_id}/dependencies（依存関係グラフ）
    - GET /api/v1/jobs/{job_id}/flow（処理フロー）
    - _Requirements: 1.1, 2.1, 3.1_
  - [x] 5.3 依存性注入を追加する
    - `server/api/dependencies.py` にget_dependency_edge_repositoryを追加
    - _Requirements: 1.1_
  - [x] 5.4 ルーターをmain.pyに登録する
    - `server/main.py` に依存関係ルーターを追加（未登録の場合）
    - _Requirements: 1.1_
  - [ ]* 5.5 API統合テストを実装する
    - **Property 2: 存在しないjob_idへのNOT_FOUND**
    - **Property 5: レスポンス形式の統一性**
    - httpx AsyncClientでAPIエンドポイントをテスト
    - **Validates: Requirements 1.2, 2.2, 3.2, 5.1, 5.2, 5.3**

- [x] 6. チェックポイント - バックエンド全体の確認
  - すべてのテストが通ることを確認し、不明点があればユーザーに質問する。

- [x] 7. フロントエンド entities/dependency の実装
  - [x] 7.1 依存関係の型定義を実装する
    - `client/app/entities/dependency/model.ts` を作成
    - DependencyType、GraphNode、GraphEdge、DependencyGraph、FlowNode、FlowData型を定義
    - _Requirements: 1.4, 1.5_
  - [x] 7.2 依存関係APIクライアントを実装する
    - `client/app/entities/dependency/api.ts` を作成
    - getDependencies、getFlow、getSourceFilesを実装
    - _Requirements: 1.1, 2.1, 3.1_
  - [x] 7.3 React Queryフックを実装する
    - `client/app/entities/dependency/hooks.ts` を作成
    - useDependencyGraph、useFlowData、useSourceFilesを実装
    - _Requirements: 1.1, 2.1, 3.1_
  - [x] 7.4 index.tsでエクスポートする
    - `client/app/entities/dependency/index.ts` を作成

- [x] 8. フロントエンド widgets/flow-graph の実装
  - [x] 8.1 React Flow変換ロジックを実装する
    - `client/app/widgets/flow-graph/lib/transform.ts` を作成
    - toReactFlowNodes、toReactFlowEdges、applyDagreLayoutを実装
    - dagreライブラリで階層レイアウト（top-to-bottom）を計算
    - _Requirements: 6.2, 6.3, 8.1_
  - [ ]* 8.2 React Flow変換ロジックのプロパティテストを実装する
    - **Property 6: グラフノード・エッジの表示完全性**
    - **Property 8: 自動レイアウトの妥当性**
    - fast-checkで任意のGraphNode/GraphEdgeを生成し、変換結果の完全性とレイアウトの妥当性を検証
    - **Validates: Requirements 6.2, 6.3, 8.1**
  - [x] 8.3 フィルタリングロジックを実装する
    - `client/app/widgets/flow-graph/lib/filter.ts` を作成
    - filterEdgesByType関数を実装
    - _Requirements: 7.1, 7.2_
  - [ ]* 8.4 フィルタリングロジックのプロパティテストを実装する
    - **Property 7: フィルタリングの正確性**
    - fast-checkで任意のGraphEdge集合とDependencyType集合を生成し、フィルタ結果の正確性を検証
    - **Validates: Requirements 7.1, 7.2**
  - [x] 8.5 カスタムノードコンポーネントを実装する
    - `client/app/widgets/flow-graph/ui/SourceFileNode.tsx` を作成
    - ファイル名（file_path）と言語（language）を表示
    - Mantineカードスタイルで表示
    - _Requirements: 6.2_
  - [x] 8.6 Flow Graphウィジェットを実装する
    - `client/app/widgets/flow-graph/ui/FlowGraph.tsx` を作成
    - React Flowコンポーネント（SourceFileNodeカスタムノード、dependency_typeラベル付きエッジ）
    - DependencyTypeフィルタ（チェックボックス）
    - レイアウトリセットボタン
    - 空状態メッセージ
    - _Requirements: 6.1, 6.4, 6.5, 6.6, 7.1, 7.2, 7.3, 8.1, 8.2_
  - [x] 8.7 index.tsでエクスポートする
    - `client/app/widgets/flow-graph/index.ts` を作成

- [x] 9. フロントエンド pages/dependencies の実装
  - [x] 9.1 依存関係ページを実装する
    - `client/app/pages/dependencies/ui.tsx` を作成
    - URLパラメータからjob_idを取得
    - useDependencyGraphフックでデータ取得
    - Flow_Graph_Widget配置
    - ローディング・エラー・空状態の表示
    - _Requirements: 6.1, 6.6, 9.1, 9.2_
  - [x] 9.2 ルーティングを設定する
    - `client/app/routes.ts` に依存関係ページのルートを追加
    - _Requirements: 6.1_

- [x] 10. 最終チェックポイント - 全体の確認
  - すべてのテストが通ることを確認し、不明点があればユーザーに質問する。

## 備考

- `*` マーク付きのタスクはオプションであり、MVP実装時にスキップ可能
- 各タスクは特定の要件にトレースされている
- チェックポイントで段階的に検証を行う
- プロパティテストはユニバーサルな正当性を検証し、ユニットテストは具体的なエッジケースを検証する
- dagreライブラリはフロントエンドの依存関係として追加が必要（`bun add dagre @types/dagre`）
- analysis-job仕様の既存コンポーネント（AnalysisJobRepository、SourceFileRepository、例外クラス）を再利用する
