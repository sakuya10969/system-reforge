# Implementation Plan: 要件レビュー・エクスポート

## Overview

業務ルール抽出後に生成された要件定義データの一覧表示・編集・ステータス管理・Markdownエクスポート機能を実装する。バックエンドはクリーンアーキテクチャ（domain → application → api / infrastructure）、フロントエンドはFSD（entities → features → pages）の順で構築する。

## Tasks

- [x] 1. バックエンド: ドメイン層の実装
  - [x] 1.1 Requirementドメインモデルの作成
    - `server/domain/models/requirement.py` にRequirementStatus、RequirementPriority列挙型とRequirementエンティティを実装
    - `__post_init__`でtitle/descriptionの空チェック、status/priorityの列挙値チェックを実装
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_
  - [ ]* 1.2 Requirementドメインモデルのプロパティテスト
    - **Property 4: ドメインモデルの空フィールドバリデーション**
    - **Property 5: ドメインモデルの列挙値バリデーション**
    - **Validates: Requirements 4.2, 4.3, 4.4, 4.5**
  - [x] 1.3 RequirementRepositoryインターフェースの作成
    - `server/domain/repositories/requirement_repository.py` にfind_by_job、find_by_id、updateメソッドを定義
    - _Requirements: 1.1, 2.1_
  - [x] 1.4 RequirementNotFoundError例外クラスの作成
    - `server/domain/exceptions.py` にRequirementNotFoundErrorを追加
    - _Requirements: 2.2_
  - [x] 1.5 MarkdownExporterドメインサービスの作成
    - `server/domain/services/markdown_exporter.py` にto_markdownメソッドを実装
    - ヘッダー「# 要件定義書」、各要件を「##」見出し、title/description/category/priority/statusをリスト形式で出力
    - 空リスト時はヘッダーのみ
    - _Requirements: 5.1, 5.2, 5.3, 5.4_
  - [ ]* 1.6 MarkdownExporterのプロパティテスト
    - **Property 6: Markdownエクスポートの完全性**
    - **Property 7: Markdownエクスポートのセクション数ラウンドトリップ**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 3.2**

- [x] 2. バックエンド: インフラストラクチャ層の実装
  - [x] 2.1 Alembicマイグレーションの作成
    - requirementsテーブルの作成マイグレーション（id, job_id, title, description, category, priority, status, source_rules, created_at, updated_at）
    - idx_requirements_job_id、idx_requirements_statusインデックス
    - _Requirements: 4.1_
  - [x] 2.2 SQLAlchemyテーブルモデルの作成
    - `server/infrastructure/database/models.py` にRequirementModelを追加
    - _Requirements: 4.1_
  - [x] 2.3 SQLAlchemyRequirementRepositoryの実装
    - `server/infrastructure/database/repositories/requirement_repository.py` にfind_by_job（created_at昇順）、find_by_id、updateを実装
    - RequirementModel ↔ Requirement のマッピング
    - _Requirements: 1.1, 2.1_

- [x] 3. バックエンド: アプリケーション層の実装
  - [x] 3.1 GetRequirementsUseCaseの実装
    - `server/application/requirements/get_requirements.py` にジョブ存在確認 → 要件一覧取得ロジックを実装
    - _Requirements: 1.1, 1.2, 1.3_
  - [x] 3.2 UpdateRequirementUseCaseの実装
    - `server/application/requirements/update_requirement.py` に要件存在確認 → フィールド更新 → updated_at設定 → 保存ロジックを実装
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_
  - [x] 3.3 ExportRequirementsUseCaseの実装
    - `server/application/requirements/export_requirements.py` にジョブ存在確認 → 要件取得 → Markdown生成ロジックを実装
    - _Requirements: 3.1, 3.2, 3.3, 3.4_
  - [ ]* 3.4 ユースケースのユニットテスト
    - GetRequirements: 正常系、ジョブ未検出、空リスト
    - UpdateRequirement: 正常系、要件未検出、バリデーションエラー
    - ExportRequirements: 正常系、ジョブ未検出、空リスト
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 3.1, 3.3, 3.4_

- [x] 4. バックエンド: API層の実装
  - [x] 4.1 Pydanticスキーマの作成
    - `server/api/schemas/requirement.py` にRequirementResponse、RequirementListResponse、RequirementUpdateRequest、RequirementDetailResponse、ExportResponse、ExportDataを実装
    - RequirementUpdateRequestにtitle/description空チェック、priority/statusバリデータを実装
    - _Requirements: 2.3, 2.4, 2.5, 2.6, 9.1, 9.2, 9.3_
  - [x] 4.2 要件APIルーターの実装
    - `server/api/routes/requirements.py` にGET /api/v1/jobs/{job_id}/requirements、PUT /api/v1/requirements/{requirement_id}、POST /api/v1/jobs/{job_id}/requirements/exportを実装
    - FastAPI依存性注入でリポジトリ・ユースケースを注入
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 3.1, 3.3_
  - [x] 4.3 main.pyにルーター登録
    - `server/main.py` に要件ルーターを追加
    - _Requirements: 1.1_

- [x] 5. Checkpoint - バックエンドテスト
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. フロントエンド: entities/requirementの実装
  - [x] 6.1 型定義とZodスキーマの作成
    - `client/app/entities/requirement/model.ts` にRequirement、RequirementStatus、RequirementPriority、RequirementUpdateInput型を定義
    - `client/app/entities/requirement/schema.ts` にrequirementFormSchemaを実装
    - _Requirements: 4.1, 7.2_
  - [x] 6.2 APIクライアントの作成
    - `client/app/entities/requirement/api.ts` にlistByJob、update、exportメソッドを実装
    - _Requirements: 1.1, 2.1, 3.1_
  - [x] 6.3 React Queryフックの作成
    - `client/app/entities/requirement/hooks.ts` にuseRequirements、useUpdateRequirement、useExportRequirementsを実装
    - _Requirements: 1.1, 2.1, 3.1_
  - [x] 6.4 index.tsでpublic APIをエクスポート
    - `client/app/entities/requirement/index.ts` で型、スキーマ、API、フックをエクスポート
    - _Requirements: 1.1_

- [x] 7. フロントエンド: features/export-requirementsの実装
  - [x] 7.1 ExportButtonコンポーネントの作成
    - `client/app/features/export-requirements/ui.tsx` にエクスポートボタンを実装
    - _Requirements: 8.1_
  - [x] 7.2 MarkdownPreviewModalコンポーネントの作成
    - `client/app/features/export-requirements/ui/MarkdownPreviewModal.tsx` にReact Markdownプレビューとダウンロード機能を実装
    - _Requirements: 8.2, 8.3_
  - [x] 7.3 index.tsでpublic APIをエクスポート
    - `client/app/features/export-requirements/index.ts`
    - _Requirements: 8.1_

- [x] 8. フロントエンド: pages/requirementsの実装
  - [x] 8.1 RequirementListコンポーネントの作成
    - `client/app/pages/requirements/ui/RequirementList.tsx` にカード形式の要件一覧を実装
    - status/priorityバッジ色分け表示を実装
    - _Requirements: 6.2, 6.3, 6.4_
  - [x] 8.2 RequirementEditModalコンポーネントの作成
    - `client/app/pages/requirements/ui/RequirementEditModal.tsx` にReact Hook Form + Zodの編集フォームを実装
    - title/descriptionの空チェック、priority/statusのセレクト、成功/エラー通知を実装
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7_
  - [x] 8.3 RequirementsPageの作成
    - `client/app/pages/requirements/ui.tsx` に要件レビューページを実装
    - ローディング、エラー、空状態の表示を実装
    - RequirementList、RequirementEditModal、ExportButton、MarkdownPreviewModalを統合
    - _Requirements: 6.1, 6.5, 6.6, 6.7, 8.1_
  - [x] 8.4 React Routerにルート追加
    - `client/app/routes.ts` に要件レビューページのルートを追加
    - _Requirements: 6.1_
  - [ ]* 8.5 バッジ色マッピングのプロパティテスト
    - **Property 8: バッジ色マッピングの正確性**
    - **Validates: Requirements 6.3, 6.4**
  - [ ]* 8.6 フロントエンドユニットテスト
    - RequirementList: 一覧表示、空状態
    - RequirementEditModal: フォーム表示、バリデーションエラー
    - MarkdownPreviewModal: Markdown表示
    - _Requirements: 6.2, 6.5, 7.1, 7.3, 7.4, 8.2_

- [x] 9. Final checkpoint - 全テスト実行
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- バックエンドはPython（FastAPI + pytest + Hypothesis）、フロントエンドはTypeScript（React + Vitest + fast-check）で実装
