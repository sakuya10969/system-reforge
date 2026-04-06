# 実装計画: ZIPアップロード

## 概要

バックエンド（FastAPI + SQLAlchemy + boto3 + PostgreSQL）とフロントエンド（React + Mantine + React Dropzone + React Query）でZIPアップロード機能を実装する。クリーンアーキテクチャとFSDに従い、ドメイン層から順に積み上げる。project-management仕様が実装済みの前提。

## タスク

- [x] 1. バックエンドDomain層
  - [x] 1.1 SourceFileドメインモデル作成
    - `server/domain/models/source_file.py` にSourceFileデータクラスを実装
    - `server/domain/models/__init__.py` でエクスポート
    - _Requirements: 3.1_
  - [x] 1.2 SourceFileRepositoryインターフェース作成
    - `server/domain/repositories/source_file_repository.py` に抽象クラスを実装
    - create_many, find_by_project, find_by_id メソッドを定義
    - _Requirements: 3.1_
  - [x] 1.3 ドメイン例外クラス追加
    - `server/domain/exceptions.py` にInvalidZipFileError、EmptyZipFileErrorを追加
    - _Requirements: 1.2, 1.4, 4.3_

- [x] 2. ZIP展開・言語判定ロジック実装
  - [x] 2.1 ZIP_Extractor実装
    - `server/application/sources/zip_extractor.py` を作成
    - LANGUAGE_MAP定義、detect_language関数、is_excluded_entry関数、extract_zip関数を実装
    - 隠しファイル（.始まり）、システムファイル（__MACOSX等）、ディレクトリエントリの除外
    - 破損ZIPの場合はInvalidZipFileError、空ZIPの場合はEmptyZipFileErrorを送出
    - _Requirements: 3.2, 3.3, 4.1, 4.2, 4.3, 4.4_
  - [ ]* 2.2 言語判定のプロパティテスト
    - **Property 3: 拡張子→言語マッピング**
    - **Validates: Requirements 3.2, 3.3**
  - [ ]* 2.3 ZIPエントリフィルタリングのプロパティテスト
    - **Property 4: ZIPエントリフィルタリング**
    - **Validates: Requirements 4.1, 4.2, 4.4**

- [x] 3. Infrastructure層実装
  - [x] 3.1 SourceFileModelテーブル定義追加
    - `server/infrastructure/database/models.py` にSourceFileModelを追加
    - project_idへのFK、インデックス設定
    - _Requirements: 3.1_
  - [x] 3.2 SQLAlchemySourceFileRepository実装
    - `server/infrastructure/database/repositories/source_file_repository.py` を作成
    - create_many（bulk insert）、find_by_project、find_by_idを実装
    - _Requirements: 3.1_
  - [x] 3.3 S3Client実装
    - `server/infrastructure/storage/s3_client.py` を作成
    - upload_file、generate_s3_keyメソッドを実装
    - S3キーフォーマット: `{s3_prefix}/sources/{file_path}`
    - _Requirements: 2.1, 2.3_
  - [ ]* 3.4 S3キー生成のプロパティテスト
    - **Property 2: S3キー生成フォーマット**
    - **Validates: Requirements 2.1**

- [x] 4. Application層実装
  - [x] 4.1 UploadSourceUseCase実装
    - `server/application/sources/upload_source.py` を作成
    - プロジェクト存在確認 → ZIP展開 → S3アップロード → DB一括登録 → 結果返却
    - UploadResult、UploadedFileInfoデータクラスを定義
    - _Requirements: 1.1, 1.3, 2.1, 2.2, 3.1_
  - [ ]* 4.2 アップロードラウンドトリップのプロパティテスト
    - **Property 1: アップロードラウンドトリップ**
    - **Validates: Requirements 1.1, 2.3, 3.1**

- [x] 5. API層実装
  - [x] 5.1 Pydanticスキーマ作成
    - `server/api/schemas/upload.py` を作成
    - UploadedFileResponse、UploadResultResponseを定義
    - _Requirements: 5.1, 5.2, 5.3_
  - [x] 5.2 エラーハンドラ追加
    - `server/api/error_handlers.py` にInvalidZipFileError、EmptyZipFileErrorのハンドラを追加
    - _Requirements: 1.2, 1.4, 4.3_
  - [x] 5.3 アップロードルーター実装
    - `server/api/routes/upload.py` を作成
    - POST /api/v1/projects/{project_id}/upload（multipart/form-data）
    - Content-Typeバリデーション（application/zip, application/x-zip-compressed）
    - ユースケースを呼び出し、レスポンススキーマで返却
    - _Requirements: 1.1, 1.2, 1.3_
  - [x] 5.4 FastAPIアプリケーション設定更新
    - `server/main.py` にアップロードルーターを登録
    - _Requirements: なし（基盤）_
  - [ ]* 5.5 レスポンス形式のプロパティテスト
    - **Property 6: レスポンス形式の統一性**
    - **Validates: Requirements 5.1, 5.2, 5.3**
  - [ ]* 5.6 存在しないプロジェクトのプロパティテスト
    - **Property 5: 存在しないプロジェクトへのNOT_FOUND**
    - **Validates: Requirements 1.3**

- [x] 6. チェックポイント - バックエンドテスト確認
  - すべてのテストが通ることを確認し、不明点があればユーザーに質問する。

- [x] 7. Alembicマイグレーション
  - [x] 7.1 source_filesテーブルマイグレーション作成
    - source_filesテーブルの作成マイグレーションファイルを作成
    - project_idへのFK制約、idx_source_files_project_idインデックスを含む
    - _Requirements: 3.1_

- [x] 8. フロントエンドエンティティ層
  - [x] 8.1 SourceFileエンティティ作成
    - `client/app/entities/source-file/model.ts` に型定義（SourceFile, UploadResult, UploadedFile）
    - `client/app/entities/source-file/index.ts` でエクスポート
    - _Requirements: 5.1, 5.2_

- [x] 9. フロントエンドアップロード機能実装
  - [x] 9.1 アップロードAPI・フック作成
    - `client/app/features/upload-zip/api.ts` にuploadZip関数（multipart/form-data送信、onUploadProgress対応）
    - `client/app/features/upload-zip/hooks.ts` にuseUploadZipミューテーションフック
    - `client/app/features/upload-zip/index.ts` でエクスポート
    - _Requirements: 1.1, 6.4_
  - [x] 9.2 Upload_Dropzoneコンポーネント実装
    - `client/app/features/upload-zip/ui.tsx` を作成
    - React Dropzone使用、accept: application/zip, application/x-zip-compressed
    - ファイル選択後にファイル名・サイズ表示、アップロードボタン
    - プログレスバー、成功時の結果表示、エラー時のエラーメッセージ表示
    - 重複送信防止（アップロード中はボタン無効化）
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_
  - [ ]* 9.3 フロントエンドファイルバリデーションのプロパティテスト
    - **Property 7: フロントエンドファイルバリデーション**
    - **Validates: Requirements 6.3**

- [x] 10. アップロードページ実装
  - [x] 10.1 アップロードページ作成
    - `client/app/pages/upload/ui.tsx` を作成
    - URLパラメータからproject_id取得
    - Upload_Dropzoneコンポーネント配置
    - アップロード結果表示エリア
    - `client/app/pages/upload/index.ts` でエクスポート
    - _Requirements: 6.1, 6.5_
  - [x] 10.2 ルーティング設定
    - `client/app/routes.ts` にアップロードページのルートを追加
    - _Requirements: 6.1_
  - [ ]* 10.3 フロントエンドユニットテスト
    - Upload_Dropzoneの表示テスト（初期状態、ファイル選択後、アップロード中、完了、エラー）
    - _Requirements: 6.1, 6.2, 6.4, 6.5, 6.6_

- [x] 11. 最終チェックポイント - 全テスト確認
  - すべてのテストが通ることを確認し、不明点があればユーザーに質問する。

## 備考

- `*` 付きのタスクはオプション（スキップ可能）
- 各タスクは特定の要件にトレースされている
- チェックポイントで段階的に検証を行う
- プロパティテストは正当性プロパティの普遍的な検証を行う
- ユニットテストは具体的な例とエッジケースを検証する
- project-management仕様の実装（projects テーブル、ProjectRepository等）が完了している前提
