# System Reforge

COBOLなどのレガシーシステムのソースコードを解析し、業務ロジックの抽出・要件定義の生成を支援するツール。

コード変換ツールではなく、ソースコードを「読んで理解する」ことに特化している。

```
ソースコード → 構造化中間データ → 業務ルール → 要件定義
```

## 処理フロー

1. ZIPファイルでソースコードをアップロード
2. S3に原本保存
3. 解析ジョブを作成（非同期実行）
4. 構造化データ（AST、依存関係、フロー情報）を生成・DB保存
5. LLMで中間データから業務ルールを抽出（ソースコードは直接渡さない）
6. 要件定義を生成・レビュー・エクスポート

## 技術スタック

| レイヤー | 技術 |
|----------|------|
| フロントエンド | React, React Router v7, Mantine, Vite, Bun |
| バックエンド | FastAPI, SQLAlchemy, Pydantic, uv |
| データベース | PostgreSQL |
| ストレージ | AWS S3 |
| LLM | Amazon Bedrock |

### フロントエンド主要ライブラリ

React Query, Zod, React Hook Form, TanStack Table, React Flow, React Dropzone, React Markdown

### バックエンド主要ライブラリ

asyncpg, Alembic, boto3, httpx

## アーキテクチャ

- フロントエンド: FSD（Feature-Sliced Design）
- バックエンド: クリーンアーキテクチャ（api → application → domain ← infrastructure）
- フロントとバックは完全分離（API経由で通信）

## プロジェクト構成

```
client/          # フロントエンド（React + React Router v7）
server/          # バックエンド（FastAPI）
docs/            # ドキュメント
scripts/         # ユーティリティスクリプト
docker-compose.yml
```

### バックエンド構成

```
server/
├── main.py                    # FastAPIエントリポイント
├── api/                       # プレゼンテーション層（ルーター・スキーマ）
├── application/               # ユースケース層
├── domain/                    # ドメイン層（モデル・リポジトリIF・サービスIF）
├── infrastructure/            # インフラ層（DB・S3・LLM実装）
└── alembic/                   # DBマイグレーション
```

## セットアップ

### 前提条件

- Docker / Docker Compose
- Bun（フロントエンド）
- uv（バックエンド）

### DB起動

```bash
docker-compose up -d
```

### バックエンド

```bash
cd server
uv sync
uv run alembic upgrade head
uv run uvicorn server.main:app --reload --port 8000
```

### フロントエンド

```bash
cd client
bun install
bun run dev
```

## ドキュメント

| ファイル | 内容 |
|----------|------|
| [docs/project-overview.md](docs/project-overview.md) | プロジェクト概要 |
| [docs/tech-stack.md](docs/tech-stack.md) | 技術スタック |
| [docs/architecture-philosophy.md](docs/architecture-philosophy.md) | アーキテクチャ思想 |
| [docs/api-design.md](docs/api-design.md) | APIデザイン |
| [docs/database-design.md](docs/database-design.md) | データベース設計 |
| [docs/domain-design.md](docs/domain-design.md) | ドメイン設計 |

## 仕様（Specs）

| 仕様 | 内容 |
|------|------|
| [project-management](docs/specs/project-management/) | プロジェクトCRUD |
| [zip-upload](docs/specs/zip-upload/) | ZIPアップロード・S3保存 |
| [analysis-job](docs/specs/analysis-job/) | 解析ジョブ管理・非同期実行 |
| [dependency-visualization](docs/specs/dependency-visualization/) | 依存関係・フロー可視化 |
| [business-rule-extraction](docs/specs/business-rule-extraction/) | 業務ルール抽出（LLM連携） |
| [requirements-review](docs/specs/requirements-review/) | 要件レビュー・エクスポート |
