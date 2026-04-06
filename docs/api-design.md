# APIデザイン

## 基本方針

- RESTful API（FastAPI）
- レスポンス形式: JSON
- バリデーション: Pydantic
- 認証: 未定（初期フェーズでは認証なし）

## ベースURL

```
/api/v1
```

---

## エンドポイント一覧

### プロジェクト管理

| メソッド | パス | 説明 |
|---------|------|------|
| POST | `/api/v1/projects` | プロジェクト作成 |
| GET | `/api/v1/projects` | プロジェクト一覧取得 |
| GET | `/api/v1/projects/{project_id}` | プロジェクト詳細取得 |
| DELETE | `/api/v1/projects/{project_id}` | プロジェクト削除 |

### ZIPアップロード

| メソッド | パス | 説明 |
|---------|------|------|
| POST | `/api/v1/projects/{project_id}/upload` | ZIPファイルアップロード（multipart/form-data） |

処理フロー:
1. ZIPファイルを受け取る
2. S3に原本保存
3. ソースファイルのメタデータをDBに登録
4. レスポンスでアップロード結果を返す

### 解析ジョブ

| メソッド | パス | 説明 |
|---------|------|------|
| POST | `/api/v1/projects/{project_id}/jobs` | 解析ジョブ作成・開始 |
| GET | `/api/v1/projects/{project_id}/jobs` | ジョブ一覧取得 |
| GET | `/api/v1/jobs/{job_id}` | ジョブ詳細・ステータス取得 |

ジョブステータス:
- `pending` — 作成済み、未開始
- `running` — 解析実行中
- `completed` — 解析完了
- `failed` — 解析失敗

### 解析結果

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/api/v1/jobs/{job_id}/source-files` | 解析対象ソースファイル一覧 |
| GET | `/api/v1/jobs/{job_id}/dependencies` | 依存関係グラフデータ |
| GET | `/api/v1/jobs/{job_id}/flow` | 処理フローデータ |
| GET | `/api/v1/jobs/{job_id}/business-rules` | 業務ルール一覧 |

### 要件

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/api/v1/jobs/{job_id}/requirements` | 要件一覧取得 |
| PUT | `/api/v1/requirements/{requirement_id}` | 要件編集 |
| POST | `/api/v1/jobs/{job_id}/requirements/export` | 要件エクスポート |

---

## 機能一覧

| # | 機能 | 対応エンドポイント | 状態 |
|---|------|-------------------|------|
| 1 | プロジェクト作成 | POST /projects | 未実装 |
| 2 | プロジェクト一覧 | GET /projects | 未実装 |
| 3 | プロジェクト詳細 | GET /projects/{id} | 未実装 |
| 4 | プロジェクト削除 | DELETE /projects/{id} | 未実装 |
| 5 | ZIPアップロード | POST /projects/{id}/upload | 未実装 |
| 6 | 解析ジョブ作成 | POST /projects/{id}/jobs | 未実装 |
| 7 | ジョブ一覧 | GET /projects/{id}/jobs | 未実装 |
| 8 | ジョブ詳細 | GET /jobs/{id} | 未実装 |
| 9 | ソースファイル一覧 | GET /jobs/{id}/source-files | 未実装 |
| 10 | 依存関係グラフ | GET /jobs/{id}/dependencies | 未実装 |
| 11 | 処理フロー | GET /jobs/{id}/flow | 未実装 |
| 12 | 業務ルール一覧 | GET /jobs/{id}/business-rules | 未実装 |
| 13 | 要件一覧 | GET /jobs/{id}/requirements | 未実装 |
| 14 | 要件編集 | PUT /requirements/{id} | 未実装 |
| 15 | 要件エクスポート | POST /jobs/{id}/requirements/export | 未実装 |

---

## レスポンス形式

### 成功時

```json
{
  "data": { ... }
}
```

### エラー時

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Project not found"
  }
}
```

### ページネーション（一覧系）

```json
{
  "data": [ ... ],
  "pagination": {
    "total": 100,
    "page": 1,
    "per_page": 20
  }
}
```
