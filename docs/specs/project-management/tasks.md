# 実装計画: プロジェクト管理（Project CRUD）

## 概要

バックエンド（FastAPI + SQLAlchemy + PostgreSQL）とフロントエンド（React + Mantine + React Query）の両方でプロジェクトCRUD機能を実装する。クリーンアーキテクチャとFSDに従い、ドメイン層から順に積み上げる。

## タスク

- [ ] 1. バックエンド基盤セットアップ
  - [ ] 1.1 DB接続・SQLAlchemy AsyncSession設定
    - `server/infrastructure/database/connection.py` を作成
    - AsyncEngine、async_sessionmaker、get_sessionジェネレータを実装
    - PostgreSQL接続文字列: `postgresql+asyncpg://admin:password@localhost:5432/system-reforge`
    - _Requirements: なし（基盤）_
  - [ ] 1.2 Projectドメインモデル作成
    - `server/domain/models/project.py` にProjectデータクラスを実装
    - `server/domain/models/__init__.py` でエクスポート
    - _Requirements: 1.1_
  - [ ] 1.3 ProjectRepositoryインターフェース作成
    - `server/domain/repositories/project_repository.py` に抽象クラスを実装
    - create, find_by_id, find_all, delete メソッドを定義
    - `server/domain/repositories/__init__.py` でエクスポート
    - _Requirements: 1.1, 2.1, 3.1, 4.1_
  - [ ] 1.4 ドメイン例外クラス作成
    - `server/domain/exceptions.py` にProjectNotFoundErrorを実装
    - _Requirements: 3.2, 4.2_

- [ ] 2. Infrastructure層実装
  - [ ] 2.1 SQLAlchemyテーブルモデル作成
    - `server/infrastructure/database/models.py` にProjectModelを実装
    - UUID主キー、name、description、s3_prefix、created_at、updated_atカラム
    - _Requirements: 1.1_
  - [ ] 2.2 SQLAlchemyProjectRepository実装
    - `server/infrastructure/database/repositories/project_repository.py` を作成
    - ProjectRepositoryインターフェースを実装
    - find_allはcreated_at降順ソート、OFFSET/LIMITでページネーション
    - ドメインモデルとSQLAlchemyモデル間の変換を実装
    - _Requirements: 1.1, 2.1, 2.2, 2.4, 3.1, 4.1_
  - [ ]* 2.3 リポジトリのプロパティテスト
    - **Property 1: 作成→取得ラウンドトリップ**
    - **Validates: Requirements 1.1, 1.4, 3.1**
  - [ ]* 2.4 リポジトリのプロパティテスト（ページネーション）
    - **Property 3: ページネーションの正確性**
    - **Validates: Requirements 2.1, 2.2**
  - [ ]* 2.5 リポジトリのプロパティテスト（ソート順）
    - **Property 4: 一覧の降順ソート**
    - **Validates: Requirements 2.4**
  - [ ]* 2.6 リポジトリのプロパティテスト（削除）
    - **Property 6: 削除→取得でNOT_FOUND**
    - **Validates: Requirements 4.1**

- [ ] 3. Application層実装
  - [ ] 3.1 CreateProjectUseCase実装
    - `server/application/create_project.py` を作成
    - UUID生成、s3_prefix自動設定（`projects/{uuid}`）、タイムスタンプ設定
    - 名前のバリデーション（空文字・ホワイトスペースのみ・255文字超を拒否）
    - _Requirements: 1.1, 1.2, 1.3, 1.4_
  - [ ] 3.2 ListProjectsUseCase実装
    - `server/application/list_projects.py` を作成
    - page/per_pageのデフォルト値設定（page=1, per_page=20）
    - _Requirements: 2.1, 2.2, 2.3_
  - [ ] 3.3 GetProjectUseCase実装
    - `server/application/get_project.py` を作成
    - 存在しない場合はProjectNotFoundErrorを送出
    - _Requirements: 3.1, 3.2_
  - [ ] 3.4 DeleteProjectUseCase実装
    - `server/application/delete_project.py` を作成
    - 存在しない場合はProjectNotFoundErrorを送出
    - _Requirements: 4.1, 4.2_
  - [ ]* 3.5 ユースケースのプロパティテスト（バリデーション）
    - **Property 2: 無効入力のバリデーション拒否**
    - **Validates: Requirements 1.2, 1.3**
  - [ ]* 3.6 ユースケースのプロパティテスト（NOT_FOUND）
    - **Property 5: 存在しないIDへのNOT_FOUND**
    - **Validates: Requirements 3.2, 4.2**

- [ ] 4. API層実装
  - [ ] 4.1 Pydanticスキーマ作成
    - `server/api/schemas/project.py` を作成
    - ProjectCreateRequest、ProjectResponse、ProjectListResponse、PaginationResponse
    - 成功レスポンスラッパー（DataResponse）、エラーレスポンスラッパー（ErrorResponse）
    - _Requirements: 7.1, 7.2, 7.3_
  - [ ] 4.2 依存性注入設定
    - `server/api/dependencies.py` を作成
    - get_session、get_project_repositoryを実装
    - _Requirements: なし（基盤）_
  - [ ] 4.3 エラーハンドラ実装
    - `server/api/error_handlers.py` を作成
    - ProjectNotFoundError → 404、ValidationError → 422の変換
    - 統一エラーレスポンス形式
    - _Requirements: 3.2, 4.2, 7.2_
  - [ ] 4.4 プロジェクトルーター実装
    - `server/api/routes/projects.py` を作成
    - POST /api/v1/projects、GET /api/v1/projects、GET /api/v1/projects/{project_id}、DELETE /api/v1/projects/{project_id}
    - ユースケースを呼び出し、レスポンススキーマで返却
    - _Requirements: 1.1, 2.1, 3.1, 4.1_
  - [ ] 4.5 FastAPIアプリケーション設定
    - `server/main.py` を更新
    - ルーター登録、エラーハンドラ登録、CORSミドルウェア設定
    - _Requirements: なし（基盤）_
  - [ ]* 4.6 APIエンドポイントのプロパティテスト（レスポンス形式）
    - **Property 7: レスポンス形式の統一性**
    - **Validates: Requirements 7.1, 7.2, 7.3**

- [ ] 5. チェックポイント - バックエンドテスト確認
  - すべてのテストが通ることを確認し、不明点があればユーザーに質問する。

- [ ] 6. Alembicマイグレーション設定
  - [ ] 6.1 Alembic初期設定
    - `server/infrastructure/migrations/` にAlembic設定を作成
    - alembic.ini、env.pyの設定
    - _Requirements: なし（基盤）_
  - [ ] 6.2 projectsテーブルマイグレーション作成
    - projectsテーブルの初期マイグレーションファイルを作成
    - _Requirements: 1.1_

- [ ] 7. フロントエンド基盤セットアップ
  - [ ] 7.1 共通APIクライアント設定
    - `client/app/shared/api/client.ts` を作成
    - ベースURL設定、レスポンス型定義（DataResponse、ErrorResponse、PaginatedResponse）
    - _Requirements: 7.1, 7.2, 7.3_
  - [ ] 7.2 Projectエンティティ層作成
    - `client/app/entities/project/model.ts` に型定義
    - `client/app/entities/project/api.ts` にAPIクライアント関数
    - `client/app/entities/project/hooks.ts` にReact Queryフック（useProjects, useProject, useCreateProject, useDeleteProject）
    - `client/app/entities/project/index.ts` でエクスポート
    - _Requirements: 1.1, 2.1, 3.1, 4.1_

- [ ] 8. フロントエンドUI実装
  - [ ] 8.1 プロジェクト作成フォーム実装
    - `client/app/features/create-project/ui.tsx` を作成
    - Mantine TextInput + Textarea、React Hook Form + Zodバリデーション
    - プロジェクト名必須、255文字以内のバリデーション
    - `client/app/features/create-project/index.ts` でエクスポート
    - _Requirements: 6.1, 6.2, 6.3_
  - [ ]* 8.2 フォームバリデーションのプロパティテスト
    - **Property 8: フロントエンドバリデーション**
    - **Validates: Requirements 6.2**
  - [ ] 8.3 プロジェクト一覧ページ実装
    - `client/app/pages/projects/ui.tsx` を作成
    - Mantine Tableでプロジェクト一覧表示
    - 新規作成ボタン → モーダルでフォーム表示
    - 削除ボタン → 確認ダイアログ後に削除実行
    - ローディング・エラー・空状態の表示
    - `client/app/pages/projects/index.ts` でエクスポート
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_
  - [ ] 8.4 ルーティング設定
    - `client/app/routes.ts` にプロジェクト一覧ページのルートを追加
    - _Requirements: 5.1_
  - [ ]* 8.5 フロントエンドユニットテスト
    - プロジェクト一覧ページの表示テスト（空状態、データあり、ローディング、エラー）
    - プロジェクト作成フォームの送信テスト
    - _Requirements: 5.1, 5.2, 6.1_

- [ ] 9. 最終チェックポイント - 全テスト確認
  - すべてのテストが通ることを確認し、不明点があればユーザーに質問する。

## 備考

- `*` 付きのタスクはオプション（スキップ可能）
- 各タスクは特定の要件にトレースされている
- チェックポイントで段階的に検証を行う
- プロパティテストは正当性プロパティの普遍的な検証を行う
- ユニットテストは具体的な例とエッジケースを検証する
