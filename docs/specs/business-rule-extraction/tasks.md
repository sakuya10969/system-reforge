# 実装計画: 業務ルール抽出

## 概要

業務ルール抽出機能の実装。バックエンド（FastAPI + SQLAlchemy + PostgreSQL + httpx）で構造化中間データからLLMを使った業務ルール抽出・API提供を、フロントエンド（React + Mantine + TanStack Table）で業務ルール一覧表示を実装する。LLMクライアントはインターフェースで抽象化し、スタブ実装を提供する。

## タスク

- [ ] 1. ドメイン層の実装
  - [ ] 1.1 BusinessRuleエンティティとRuleType列挙型を実装する
    - `server/domain/models/business_rule.py` を作成
    - RuleType列挙型（condition, calculation, validation）を定義
    - BusinessRuleデータクラスを実装（descriptionの空文字バリデーション付き）
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  - [ ]* 1.2 ドメインモデルバリデーションのプロパティテストを実装する
    - **Property 7: ドメインモデルバリデーション**
    - Hypothesisで任意のrule_type文字列を生成し、有効な値のみBusinessRule生成が成功することを検証
    - 空文字列・ホワイトスペースのみのdescriptionでValueErrorが発生することを検証
    - **Validates: Requirements 4.2, 4.3**
  - [ ] 1.3 BusinessRuleRepositoryインターフェースを実装する
    - `server/domain/repositories/business_rule_repository.py` を作成
    - create_many, find_by_jobメソッドを定義（find_by_jobはrule_typeフィルタ対応）
    - _Requirements: 1.5, 3.1, 3.4_
  - [ ] 1.4 MeaningExtractionServiceインターフェースとLLMClientインターフェースを実装する
    - `server/domain/services/meaning_extraction_service.py` を作成（IntermediateData, ExtractedRule, MeaningExtractionService）
    - `server/domain/services/llm_client.py` を作成（LLMClient抽象クラス）
    - _Requirements: 1.1, 1.2, 2.1, 2.2_

- [ ] 2. インフラストラクチャ層の実装
  - [ ] 2.1 BusinessRuleModelを追加する
    - `server/infrastructure/database/models.py` にBusinessRuleModelを追加
    - job_idとsource_file_idにインデックスを設定
    - _Requirements: 4.1, 4.4_
  - [ ] 2.2 Alembicマイグレーションを作成する
    - business_rulesテーブルの作成マイグレーションを生成
    - _Requirements: 4.1_
  - [ ] 2.3 SQLAlchemyBusinessRuleRepositoryを実装する
    - `server/infrastructure/database/repositories/business_rule_repository.py` を作成
    - BusinessRuleModel ↔ BusinessRule のマッピング
    - find_by_jobはcreated_at昇順ソート、rule_typeフィルタ対応
    - _Requirements: 1.5, 3.1, 3.4_
  - [ ] 2.4 StubLLMClientを実装する
    - `server/infrastructure/llm/llm_client.py` にStubLLMClientを作成
    - 固定の業務ルールデータ（condition, calculation, validation各1件）を返却
    - _Requirements: 2.1, 2.2, 2.3_
  - [ ] 2.5 DefaultMeaningExtractionServiceを実装する
    - `server/infrastructure/llm/meaning_extraction_service.py` を作成
    - 各IntermediateDataに対してLLMClientを呼び出し、結果を集約
    - エラー発生時は抽出済みルールを保持し、ログ出力して処理継続
    - _Requirements: 1.1, 1.2, 1.3, 1.4_
  - [ ]* 2.6 LLMエラー時の部分結果保持のプロパティテストを実装する
    - **Property 3: LLMエラー時の部分結果保持**
    - Hypothesisで任意のN個のIntermediateDataを生成し、K番目でエラーが発生するLLMClientモックを使用
    - エラー前後の抽出結果が保持されることを検証
    - **Validates: Requirements 1.4**

- [ ] 3. チェックポイント - ドメイン層・インフラ層の確認
  - すべてのテストが通ることを確認し、不明点があればユーザーに質問する。

- [ ] 4. アプリケーション層の実装
  - [ ] 4.1 ExtractBusinessRulesUseCaseを実装する
    - `server/application/extract_business_rules.py` を作成
    - ジョブ存在確認、MeaningExtractionService呼び出し、BusinessRule変換・保存
    - _Requirements: 1.1, 1.3, 1.5_
  - [ ]* 4.2 抽出→保存→取得ラウンドトリップのプロパティテストを実装する
    - **Property 1: 抽出→保存→取得ラウンドトリップ**
    - モックリポジトリを使用し、抽出されたルールの数と内容が保存・取得後に一致することを検証
    - **Validates: Requirements 1.1, 1.3, 1.5**
  - [ ] 4.3 GetBusinessRulesUseCaseを実装する
    - `server/application/get_business_rules.py` を作成
    - ジョブ存在確認、業務ルール一覧取得（rule_typeフィルタ対応、created_at昇順）
    - _Requirements: 3.1, 3.2, 3.3, 3.4_
  - [ ]* 4.4 業務ルール一覧取得のプロパティテストを実装する
    - **Property 5: 業務ルール一覧の昇順ソート**
    - **Property 6: APIのrule_typeフィルタリング**
    - Hypothesisで任意のN個の業務ルールを生成し、ソート順とフィルタリング結果を検証
    - **Validates: Requirements 3.1, 3.4**

- [ ] 5. API層の実装
  - [ ] 5.1 Pydanticスキーマを実装する
    - `server/api/schemas/business_rule.py` を作成
    - SourceLocationSchema、BusinessRuleResponse、BusinessRuleListResponseを定義
    - _Requirements: 5.1, 5.2_
  - [ ] 5.2 業務ルールルーターを実装する
    - `server/api/routes/analysis.py` に GET /api/v1/jobs/{job_id}/business-rules を追加
    - rule_typeクエリパラメータ対応
    - _Requirements: 3.1, 3.2, 3.3, 3.4_
  - [ ] 5.3 依存性注入を追加する
    - `server/api/dependencies.py` にget_business_rule_repository、get_meaning_extraction_service、get_llm_clientを追加
    - _Requirements: 2.1_
  - [ ] 5.4 ルーターをmain.pyに登録する（既存ルーターへの追加の場合は不要）
    - _Requirements: 3.1_
  - [ ]* 5.5 API統合テストを実装する
    - **Property 4: 存在しないjob_idへのNOT_FOUND**
    - **Property 8: レスポンス形式の統一性**
    - httpx AsyncClientでAPIエンドポイントをテスト
    - **Validates: Requirements 3.2, 5.1, 5.2**

- [ ] 6. チェックポイント - バックエンド全体の確認
  - すべてのテストが通ることを確認し、不明点があればユーザーに質問する。

- [ ] 7. フロントエンド entities/business-rule の実装
  - [ ] 7.1 BusinessRule型定義を実装する
    - `client/app/entities/business-rule/model.ts` を作成
    - RuleType型、SourceLocation型、BusinessRule型を定義
    - _Requirements: 4.1, 4.2_
  - [ ] 7.2 BusinessRule APIクライアントを実装する
    - `client/app/entities/business-rule/api.ts` を作成
    - listByJob（rule_typeフィルタ対応）を実装
    - _Requirements: 3.1, 3.4_
  - [ ] 7.3 React Queryフックを実装する
    - `client/app/entities/business-rule/hooks.ts` を作成
    - useBusinessRules（jobId, ruleType?）を実装
    - _Requirements: 6.1_
  - [ ] 7.4 index.tsでエクスポートする
    - `client/app/entities/business-rule/index.ts` を作成

- [ ] 8. フロントエンド widgets/rule-table の実装
  - [ ] 8.1 RuleTypeBadgeコンポーネントを実装する
    - `client/app/widgets/rule-table/ui/RuleTypeBadge.tsx` を作成
    - rule_typeに応じたバッジ色分け（condition:blue、calculation:green、validation:orange）
    - _Requirements: 6.3_
  - [ ] 8.2 業務ルールテーブルウィジェットを実装する
    - `client/app/widgets/rule-table/ui/RuleTable.tsx` を作成
    - TanStack Tableでカラム定義（種別、説明、ソースファイル、位置）
    - カラムフィルタ（rule_type）とソート機能を実装
    - 0件時の空状態メッセージ、ローディング中のSkeleton表示
    - _Requirements: 6.2, 6.4, 6.5, 7.1, 7.2, 7.3, 8.1, 8.2_
  - [ ] 8.3 index.tsでエクスポートする
    - `client/app/widgets/rule-table/index.ts` を作成
  - [ ]* 8.4 テーブル表示のプロパティテストを実装する
    - **Property 9: テーブル表示の完全性**
    - **Property 10: UIフィルタリングのラウンドトリップ**
    - fast-checkでランダムなBusinessRuleデータを生成し、レンダリング結果に必要情報と正しいバッジ色が含まれることを検証
    - フィルタ適用・解除後のデータ整合性を検証
    - **Validates: Requirements 6.2, 6.3, 7.1, 7.2**

- [ ] 9. フロントエンド pages/analysis への統合
  - [ ] 9.1 解析結果ページに業務ルールタブを追加する
    - `client/app/pages/analysis/ui.tsx` を修正
    - Mantine Tabsで業務ルールタブを追加
    - RuleTableWidgetを配置
    - ローディング・エラー状態の表示
    - _Requirements: 6.1, 6.5, 6.6_

- [ ] 10. 最終チェックポイント - 全体の確認
  - すべてのテストが通ることを確認し、不明点があればユーザーに質問する。

## 備考

- `*` マーク付きのタスクはオプションであり、MVP実装時にスキップ可能
- 各タスクは特定の要件にトレースされている
- チェックポイントで段階的に検証を行う
- プロパティテストはユニバーサルな正当性を検証し、ユニットテストは具体的なエッジケースを検証する
- LLMクライアントはStubLLMClientで代替し、実際のLLMプロバイダ接続は別途実装する
- 解析ジョブのワーカー（RunAnalysisUseCase）からExtractBusinessRulesUseCaseを呼び出す統合は、analysis-job仕様の更新として別途対応する
