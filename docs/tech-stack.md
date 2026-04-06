# 技術スタック

## フロントエンド

| カテゴリ | 技術 |
|----------|------|
| UIライブラリ | React |
| ルーティング | React Router v7 |
| UIフレームワーク | Mantine |
| パッケージマネージャ | Bun |
| ビルドツール | Vite |

### 主要ライブラリ

| 用途 | ライブラリ |
|------|-----------|
| サーバー状態管理 | React Query（TanStack Query） |
| バリデーション | Zod |
| フォーム | React Hook Form |
| UI状態管理 | Jotai or Zustand |
| テーブル | TanStack Table |
| グラフ・フロー可視化 | React Flow |
| ファイルアップロード | React Dropzone |
| Markdown表示 | React Markdown |

## バックエンド

| カテゴリ | 技術 |
|----------|------|
| フレームワーク | FastAPI |
| パッケージマネージャ | uv |
| クラウド | AWS |

### 主要ライブラリ

| 用途 | ライブラリ |
|------|-----------|
| HTTPクライアント | httpx |
| バリデーション・スキーマ | Pydantic |
| ORM | SQLAlchemy |
| PostgreSQL非同期ドライバ | asyncpg |
| マイグレーション | Alembic |
| AWS SDK | boto3 |

### 非同期ジョブ

Celery + Redis または Dramatiq

## データベース

| 項目 | 値 |
|------|-----|
| RDBMS | PostgreSQL |
| DB名 | `system-reforge` |
| ユーザー | `admin` |
| パスワード | `password` |

## インフラ

| 用途 | サービス |
|------|---------|
| オブジェクトストレージ | AWS S3 |
| LLM | Amazon Bedrock |
| コンテナ実行 | Amazon ECS on Fargate |
| コンテナ | Docker / Docker Compose |
