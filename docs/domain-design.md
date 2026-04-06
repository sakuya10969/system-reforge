# ドメイン設計

## エンティティ一覧

### Project（プロジェクト）

レガシーコード解析の単位。1つのZIPアップロードに対応する。

| 属性 | 型 | 説明 |
|------|-----|------|
| id | UUID | 一意識別子 |
| name | str | プロジェクト名 |
| description | str | 説明 |
| s3_prefix | str | S3保存先プレフィックス |
| created_at | datetime | 作成日時 |
| updated_at | datetime | 更新日時 |

### SourceFile（ソースファイル）

ZIP内の個別ソースファイル。S3に原本保存される。

| 属性 | 型 | 説明 |
|------|-----|------|
| id | UUID | 一意識別子 |
| project_id | UUID | 所属プロジェクト |
| file_path | str | ZIP内の相対パス |
| language | str | 言語種別（COBOL等） |
| s3_key | str | S3オブジェクトキー |
| size_bytes | int | ファイルサイズ |

### AnalysisJob（解析ジョブ）

非同期で実行される解析処理の単位。

| 属性 | 型 | 説明 |
|------|-----|------|
| id | UUID | 一意識別子 |
| project_id | UUID | 対象プロジェクト |
| status | JobStatus | pending / running / completed / failed |
| started_at | datetime | 開始日時 |
| completed_at | datetime | 完了日時 |
| error_message | str | エラーメッセージ |

ステータス遷移:
```
pending → running → completed
                  → failed
```

### DependencyEdge（依存関係）

プログラム間の呼び出し・参照関係。

| 属性 | 型 | 説明 |
|------|-----|------|
| id | UUID | 一意識別子 |
| job_id | UUID | 解析ジョブ |
| source_file_id | UUID | 呼び出し元 |
| target_file_id | UUID | 呼び出し先 |
| dependency_type | str | CALL / COPY / INCLUDE 等 |
| metadata | dict | 追加情報 |

### BusinessRule（業務ルール）

ソースコードから抽出された業務ロジック。

| 属性 | 型 | 説明 |
|------|-----|------|
| id | UUID | 一意識別子 |
| job_id | UUID | 解析ジョブ |
| source_file_id | UUID | 抽出元ファイル |
| rule_type | str | condition / calculation / validation |
| description | str | 自然言語での業務ルール記述 |
| source_location | dict | ソースコード上の位置 |
| raw_logic | str | 中間データ形式の元ロジック |

### Requirement（要件）

業務ルールから生成された要件定義。

| 属性 | 型 | 説明 |
|------|-----|------|
| id | UUID | 一意識別子 |
| job_id | UUID | 解析ジョブ |
| title | str | 要件タイトル |
| description | str | 要件の詳細記述 |
| category | str | 分類 |
| priority | str | high / medium / low |
| status | str | draft / reviewed / approved |
| source_rules | list[UUID] | 元になった業務ルールのID |

---

## リポジトリインターフェース

domain層で定義し、infrastructure層で実装する。

### ProjectRepository

```python
class ProjectRepository(ABC):
    async def create(self, project: Project) -> Project
    async def find_by_id(self, project_id: UUID) -> Project | None
    async def find_all(self, page: int, per_page: int) -> tuple[list[Project], int]
    async def delete(self, project_id: UUID) -> None
```

### SourceFileRepository

```python
class SourceFileRepository(ABC):
    async def create_many(self, files: list[SourceFile]) -> list[SourceFile]
    async def find_by_project(self, project_id: UUID) -> list[SourceFile]
    async def find_by_id(self, file_id: UUID) -> SourceFile | None
```

### AnalysisJobRepository

```python
class AnalysisJobRepository(ABC):
    async def create(self, job: AnalysisJob) -> AnalysisJob
    async def find_by_id(self, job_id: UUID) -> AnalysisJob | None
    async def find_by_project(self, project_id: UUID) -> list[AnalysisJob]
    async def update_status(self, job_id: UUID, status: str, error_message: str | None = None) -> None
```

### BusinessRuleRepository

```python
class BusinessRuleRepository(ABC):
    async def create_many(self, rules: list[BusinessRule]) -> list[BusinessRule]
    async def find_by_job(self, job_id: UUID) -> list[BusinessRule]
```

### RequirementRepository

```python
class RequirementRepository(ABC):
    async def create_many(self, requirements: list[Requirement]) -> list[Requirement]
    async def find_by_job(self, job_id: UUID) -> list[Requirement]
    async def find_by_id(self, requirement_id: UUID) -> Requirement | None
    async def update(self, requirement: Requirement) -> Requirement
```

---

## ドメインサービス

### AnalysisService

解析処理のドメインロジックを担当。ワーカーから呼び出される。

責務:
- ソースコードのパース → 構造化中間データ生成
- 依存関係の抽出
- 処理フローの構築

### MeaningExtractionService

LLMを使った意味抽出のドメインロジック。

責務:
- 中間データからの業務ルール抽出
- 業務ルールから要件への変換
- LLMにはソースコードを直接渡さない（中間データのみ）

---

## 集約の境界

| 集約ルート | 含まれるエンティティ |
|-----------|-------------------|
| Project | SourceFile |
| AnalysisJob | DependencyEdge, BusinessRule, Requirement |

- ProjectとAnalysisJobは独立した集約
- AnalysisJobの結果（依存関係、業務ルール、要件）はジョブ単位でまとめて管理
