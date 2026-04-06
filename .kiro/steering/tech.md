# 技術スタック・アーキテクチャ方針

## 処理フロー

```
1. ZIPアップロード（フロント）
2. S3に原本保存（API）
3. 解析ジョブ作成（API → DB）
4. ワーカーが解析実行（非同期）
5. 構造化データ生成・DB保存
6. LLMで意味抽出（中間データを入力）
7. 結果をDB保存
8. フロントで表示
```

## 重要な制約

- S3は原本保管場所。解析対象のソースコードはS3から取得する
- LLMにソースコードを直接読ませない。必ず構造化された中間データを経由する
- 中間データ（AST、依存関係、フロー情報など）は必須。省略しない

## フロントエンド

### ランタイム・ビルド
- React
- React Router v7
- Bun（パッケージマネージャ・ランタイム）
- Vite（ビルド）

### UIフレームワーク
- Mantine

### アーキテクチャ
- FSD（Feature-Sliced Design）

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

### フロントエンド方針
- サーバー状態（API データ）→ React Query で管理
- UI状態（モーダル開閉、選択状態など）→ Jotai or Zustand で軽量管理
- フォーム → React Hook Form + Zod で分離
- 責務分離はFSDレイヤーで実現

## バックエンド

### フレームワーク・ツール
- FastAPI
- uv（パッケージマネージャ）
- AWS（S3、その他必要に応じて）

### アーキテクチャ
- クリーンアーキテクチャ

### データベース
- PostgreSQL
- DB名: `system-reforge`
- ユーザー: `admin`
- パスワード: `password`

### 主要ライブラリ
| 用途 | ライブラリ |
|------|-----------|
| HTTPクライアント | httpx |
| バリデーション・スキーマ | Pydantic |
| ORM | SQLAlchemy |
| PostgreSQL非同期ドライバ | asyncpg |
| マイグレーション | Alembic |
| AWS SDK | boto3 |

### バックエンド方針
- APIルーター（FastAPI）とユースケース（ビジネスロジック）を分離
- ドメインロジックはフレームワーク非依存で実装
- 解析処理はAPIで同期実行しない（バックグラウンドタスクで実行）
- LLMは意味抽出専用。コード生成やコード変換には使わない
