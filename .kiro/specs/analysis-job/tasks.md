# 実装計画: 解析ジョブ管理

## 概要

解析ジョブ管理機能の実装。バックエンド（FastAPI + SQLAlchemy + PostgreSQL）でジョブのCRUD・非同期実行を、フロントエンド（React + Mantine + React Query）でジョブの状態監視UIを実装する。解析処理の実体はスタブとし、実際のパーサー実装は別仕様で扱う。

## タスク

- [ ] 1. ドメイン層の実装
  - [ ] 1.1 AnalysisJobエンティティとJobStatus列挙型を実装する
    - `server/domain/models/analysis_job.py` を作成
    - JobStatus列挙型（pending, running, completed, failed）を定義
    - VALID_TRANSITIONS辞書を定義
    - AnalysisJobデータクラスにtransition_toメソッドを実装（不正遷移時にInvalidStatusTransitionErrorを発生）
    - _Requirements: 5.1, 5.2_
  - [ ]* 1.2 ステータス遷移のプロパティテストを実装する
    - **Property 5: ステータス遷移の正当性**
    - Hypothesisで全JobStatusペアを生成し、有効な遷移のみ成功することを検証
    - running遷移時のstarted_at、completed遷移時のcompleted_at、failed遷移時のerror_message設定を検証
    - **Validates: Requirements 4.1, 4.2, 4.3, 5.1, 5.2**
  - [ ] 1.3 例外クラスを追加する
    - `server/domain/exceptions.py` にAnalysisJobNotFoundError、InvalidStatusTransitionError、NoSourceFilesErrorを追加
    - _Requirements: 1.3, 1.4, 3.2, 5.2_
  - [ ] 1.4 AnalysisJobRepositoryインターフェースを実装する
    - `server/domain/repositories/analysis_job_repository.py` を作成
    - create, find_by_id, find_by_project, updateメソッドを定義
    - _Requirements: 1.1, 2.1, 3.1_
  - [ ] 1.5 AnalysisServiceインターフェースを実装する
    - `server/domain/services/analysis_service.py` を作成
    - analyzeメソッドを定義（抽象クラス）
    - _Requirements: 4.4_

- [ ] 2. インフラストラクチャ層の実装
  - [ ] 2.1 AnalysisJobModelを追加する
    - `server/infrastructure/database/models.py` にAnalysisJobModelを追加
    - project_idとstatusにインデックスを設定
    - _Requirements: 1.1_
  - [ ] 2.2 Alembicマイグレーションを作成する
    - analysis_jobsテーブルの作成マイグレーションを生成
    - _Requirements: 1.1_
  - [ ] 2.3 SQLAlchemyAnalysisJobRepositoryを実装する
    - `server/infrastructure/database/repositories/analysis_job_repository.py` を作成
    - AnalysisJobModel ↔ AnalysisJob のマッピング
    - find_by_projectはcreated_at降順でソート
    - _Requirements: 1.1, 2.1, 3.1_
  - [ ] 2.4 StubAnalysisServiceを実装する
    - `server/infrastructure/analysis/stub_analysis_service.py` を作成
    - AnalysisServiceインターフェースのスタブ実装（何もしない）
    - _Requirements: 4.4_

- [ ] 3. チェックポイント - ドメイン層・インフラ層の確認
  - すべてのテストが通ることを確認し、不明点があればユーザーに質問する。

- [ ] 4. アプリケーション層の実装
  - [ ] 4.1 StartAnalysisUseCaseを実装する
    - `server/application/start_analysis.py` を作成
    - プロジェクト存在確認、ソースファイル存在確認、ジョブ作成ロジック
    - _Requirements: 1.1, 1.3, 1.4_
  - [ ]* 4.2 StartAnalysisUseCaseのプロパティテストを実装する
    - **Property 3: ソースファイル未登録時の拒否**
    - ソースファイル0件のプロジェクトに対してジョブ作成がNoSourceFilesErrorを発生させることを検証
    - **Validates: Requirements 1.4**
  - [ ] 4.3 ListJobsUseCaseを実装する
    - `server/application/list_jobs.py` を作成
    - プロジェクト存在確認後、ジョブ一覧をcreated_at降順で返却
    - _Requirements: 2.1, 2.2, 2.3_
  - [ ] 4.4 GetJobUseCaseを実装する
    - `server/application/get_job.py` を作成
    - ジョブ取得、存在しない場合はAnalysisJobNotFoundError
    - _Requirements: 3.1, 3.2_
  - [ ] 4.5 RunAnalysisUseCaseを実装する
    - `server/application/run_analysis.py` を作成
    - ステータス遷移（pending→running→completed/failed）、タイムスタンプ設定、Analysis_Service呼び出し
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  - [ ]* 4.6 RunAnalysisUseCaseのユニットテストを実装する
    - 正常完了パス（pending→running→completed）のテスト
    - エラーパス（pending→running→failed）のテスト
    - リポジトリとAnalysisServiceのモックを使用
    - _Requirements: 4.1, 4.2, 4.3_

- [ ] 5. API層の実装
  - [ ] 5.1 Pydanticスキーマを実装する
    - `server/api/schemas/job.py` を作成
    - JobResponse、JobListResponse、JobCreateResponseを定義
    - _Requirements: 6.1, 6.2, 6.3_
  - [ ] 5.2 ジョブルーターを実装する
    - `server/api/routes/jobs.py` を作成
    - POST /api/v1/projects/{project_id}/jobs（ジョブ作成 + BackgroundTasks登録）
    - GET /api/v1/projects/{project_id}/jobs（ジョブ一覧）
    - GET /api/v1/jobs/{job_id}（ジョブ詳細）
    - _Requirements: 1.1, 1.2, 2.1, 3.1_
  - [ ] 5.3 例外ハンドラを追加する
    - `server/api/error_handlers.py` にAnalysisJobNotFoundError、NoSourceFilesError、InvalidStatusTransitionErrorのハンドラを追加
    - _Requirements: 1.3, 1.4, 3.2, 5.2_
  - [ ] 5.4 依存性注入を追加する
    - `server/api/dependencies.py` にget_analysis_job_repository、get_analysis_serviceを追加
    - _Requirements: 1.1_
  - [ ] 5.5 ルーターをmain.pyに登録する
    - `server/main.py` にジョブルーターを追加
    - _Requirements: 1.1_
  - [ ]* 5.6 API統合テストを実装する
    - **Property 1: ジョブ作成→取得ラウンドトリップ**
    - **Property 2: 存在しないIDへのNOT_FOUND**
    - **Property 4: ジョブ一覧の降順ソート**
    - **Property 6: レスポンス形式の統一性**
    - httpx AsyncClientでAPIエンドポイントをテスト
    - **Validates: Requirements 1.1, 1.3, 2.1, 2.2, 3.1, 3.2, 6.1, 6.2, 6.3**

- [ ] 6. チェックポイント - バックエンド全体の確認
  - すべてのテストが通ることを確認し、不明点があればユーザーに質問する。

- [ ] 7. フロントエンド entities/job の実装
  - [ ] 7.1 Job型定義を実装する
    - `client/app/entities/job/model.ts` を作成
    - JobStatus型、Job型を定義
    - _Requirements: 3.1_
  - [ ] 7.2 Job APIクライアントを実装する
    - `client/app/entities/job/api.ts` を作成
    - createJob、listJobs、getJobを実装
    - _Requirements: 1.1, 2.1, 3.1_
  - [ ] 7.3 React Queryフックを実装する
    - `client/app/entities/job/hooks.ts` を作成
    - useJobs（ポーリング付き）、useJob（ポーリング付き）、useCreateJobを実装
    - ポーリング制御: pending/runningの場合のみrefetchInterval=5000ms
    - _Requirements: 7.3, 7.4, 7.5_
  - [ ] 7.4 index.tsでエクスポートする
    - `client/app/entities/job/index.ts` を作成
    - _Requirements: 7.1_
  - [ ]* 7.5 ポーリング制御ロジックのプロパティテストを実装する
    - **Property 7: ポーリング制御**
    - fast-checkで全JobStatusを生成し、ポーリング有効/無効の判定が正しいことを検証
    - **Validates: Requirements 7.3, 7.4, 7.5**

- [ ] 8. フロントエンド features/start-analysis の実装
  - [ ] 8.1 解析開始ボタンコンポーネントを実装する
    - `client/app/features/start-analysis/ui.tsx` を作成
    - useCreateJobミューテーションを使用
    - ローディング中はボタン無効化
    - エラー時にMantine Notificationで通知
    - _Requirements: 7.2_
  - [ ] 8.2 index.tsでエクスポートする
    - `client/app/features/start-analysis/index.ts` を作成

- [ ] 9. フロントエンド widgets/job-list の実装
  - [ ] 9.1 ジョブ一覧ウィジェットを実装する
    - `client/app/widgets/job-list/ui.tsx` を作成
    - Mantine Tableでジョブ一覧表示
    - ステータスバッジの色分け（pending:gray、running:blue、completed:green、failed:red）
    - 0件時の空状態メッセージ
    - ローディング中のSkeleton表示
    - _Requirements: 8.1, 8.2, 8.3_
  - [ ] 9.2 index.tsでエクスポートする
    - `client/app/widgets/job-list/index.ts` を作成
  - [ ]* 9.3 ジョブ一覧ウィジェットのプロパティテストを実装する
    - **Property 8: ジョブ一覧ウィジェットの表示完全性**
    - fast-checkでランダムなジョブデータを生成し、レンダリング結果に必要な情報と正しい色が含まれることを検証
    - **Validates: Requirements 8.1, 8.3**

- [ ] 10. フロントエンド pages/analysis の実装
  - [ ] 10.1 解析ページを実装する
    - `client/app/pages/analysis/ui.tsx` を作成
    - URLパラメータからproject_idを取得
    - Start_Analysisボタン配置
    - Job_List_Widget配置
    - useJobsフックでジョブ一覧取得（ポーリング付き）
    - ローディング・エラー状態の表示
    - _Requirements: 7.1, 7.2, 7.6, 7.7_
  - [ ] 10.2 ルーティングを設定する
    - `client/app/routes.ts` に解析ページのルートを追加
    - _Requirements: 7.1_

- [ ] 11. 最終チェックポイント - 全体の確認
  - すべてのテストが通ることを確認し、不明点があればユーザーに質問する。

## 備考

- `*` マーク付きのタスクはオプションであり、MVP実装時にスキップ可能
- 各タスクは特定の要件にトレースされている
- チェックポイントで段階的に検証を行う
- プロパティテストはユニバーサルな正当性を検証し、ユニットテストは具体的なエッジケースを検証する
- 解析処理の実体（パーサー呼び出し、構造化データ生成）はStubAnalysisServiceで代替する
