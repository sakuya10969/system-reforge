# データベース設計

## 接続情報

| 項目 | 値 |
|------|-----|
| RDBMS | PostgreSQL |
| DB名 | `system-reforge` |
| ユーザー | `admin` |
| パスワード | `password` |

## ER概要

```
Project 1──* SourceFile
Project 1──* AnalysisJob
AnalysisJob 1──* BusinessRule
AnalysisJob 1──* Requirement
AnalysisJob 1──* DependencyEdge
SourceFile 1──* BusinessRule
```

---

## テーブル定義

### projects

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | UUID | PK | プロジェクトID |
| name | VARCHAR(255) | NOT NULL | プロジェクト名 |
| description | TEXT | | 説明 |
| s3_prefix | VARCHAR(512) | NOT NULL | S3上の保存先プレフィックス |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 作成日時 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 更新日時 |

### source_files

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | UUID | PK | ソースファイルID |
| project_id | UUID | FK → projects.id, NOT NULL | 所属プロジェクト |
| file_path | VARCHAR(1024) | NOT NULL | ZIP内の相対パス |
| language | VARCHAR(50) | NOT NULL | 言語（COBOL等） |
| s3_key | VARCHAR(1024) | NOT NULL | S3オブジェクトキー |
| size_bytes | BIGINT | | ファイルサイズ |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 作成日時 |

### analysis_jobs

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | UUID | PK | ジョブID |
| project_id | UUID | FK → projects.id, NOT NULL | 対象プロジェクト |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | pending / running / completed / failed |
| started_at | TIMESTAMP | | 開始日時 |
| completed_at | TIMESTAMP | | 完了日時 |
| error_message | TEXT | | エラー時のメッセージ |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 作成日時 |

### dependency_edges

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | UUID | PK | エッジID |
| job_id | UUID | FK → analysis_jobs.id, NOT NULL | 解析ジョブ |
| source_file_id | UUID | FK → source_files.id, NOT NULL | 呼び出し元 |
| target_file_id | UUID | FK → source_files.id, NOT NULL | 呼び出し先 |
| dependency_type | VARCHAR(50) | NOT NULL | CALL / COPY / INCLUDE 等 |
| metadata | JSONB | | 追加情報 |

### business_rules

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | UUID | PK | 業務ルールID |
| job_id | UUID | FK → analysis_jobs.id, NOT NULL | 解析ジョブ |
| source_file_id | UUID | FK → source_files.id | 抽出元ファイル |
| rule_type | VARCHAR(50) | NOT NULL | condition / calculation / validation 等 |
| description | TEXT | NOT NULL | 業務ルールの自然言語記述 |
| source_location | JSONB | | ソースコード上の位置情報 |
| raw_logic | TEXT | | 元のコードロジック（中間データ形式） |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 作成日時 |

### requirements

| カラム | 型 | 制約 | 説明 |
|--------|-----|------|------|
| id | UUID | PK | 要件ID |
| job_id | UUID | FK → analysis_jobs.id, NOT NULL | 解析ジョブ |
| title | VARCHAR(500) | NOT NULL | 要件タイトル |
| description | TEXT | NOT NULL | 要件の詳細記述 |
| category | VARCHAR(100) | | 分類（業務ロジック / データ処理 / 入出力 等） |
| priority | VARCHAR(20) | | high / medium / low |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'draft' | draft / reviewed / approved |
| source_rules | UUID[] | | 元になったbusiness_rulesのID配列 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 作成日時 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 更新日時 |

---

## インデックス

| テーブル | カラム | 種類 |
|----------|--------|------|
| source_files | project_id | INDEX |
| analysis_jobs | project_id | INDEX |
| analysis_jobs | status | INDEX |
| dependency_edges | job_id | INDEX |
| business_rules | job_id | INDEX |
| business_rules | source_file_id | INDEX |
| requirements | job_id | INDEX |
| requirements | status | INDEX |
