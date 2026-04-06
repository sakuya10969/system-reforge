# プロジェクト構成

## 全体構成

```
client/          # フロントエンド（React + React Router v7）
server/          # バックエンド（FastAPI）
docker-compose.yml
```

## フロントエンド（FSD）

```
client/app/
├── app/              # エントリポイント・プロバイダ・グローバル設定
│   ├── providers/    # QueryClientProvider, MantineProvider など
│   ├── styles/       # グローバルCSS
│   └── root.tsx      # ルートコンポーネント
│
├── processes/        # アプリレベルの複合フロー（解析ジョブ全体フローなど）
│
├── pages/            # ルート単位のページコンポーネント
│   ├── upload/       # アップロードページ
│   ├── analysis/     # 解析結果ページ
│   ├── dependencies/ # 依存関係可視化ページ
│   └── requirements/ # 要件レビューページ
│
├── widgets/          # ページ内の独立したUIブロック
│   ├── job-list/     # ジョブ一覧ウィジェット
│   ├── flow-graph/   # フロー可視化ウィジェット（React Flow）
│   └── rule-table/   # 業務ルールテーブル（TanStack Table）
│
├── features/         # 機能単位（ユーザー操作に対応）
│   ├── upload-zip/   # ZIPアップロード機能
│   ├── start-analysis/ # 解析開始機能
│   └── export-requirements/ # 要件エクスポート機能
│
├── entities/         # ドメインモデル・API型定義
│   ├── project/      # プロジェクト
│   ├── job/          # 解析ジョブ
│   ├── source-file/  # ソースファイル
│   ├── business-rule/ # 業務ルール
│   └── requirement/  # 要件
│
└── shared/           # 共通ユーティリティ
    ├── api/          # APIクライアント（axios/fetch設定）
    ├── ui/           # 共通UIコンポーネント
    ├── lib/          # ユーティリティ関数
    └── config/       # 環境変数・定数
```

### FSDレイヤールール
- 依存方向: 上位レイヤー → 下位レイヤーのみ（pages → widgets → features → entities → shared）
- 同一レイヤー内のモジュール間は直接参照しない
- 各モジュールは `index.ts` で公開APIを定義

## バックエンド（クリーンアーキテクチャ）

```
server/
├── main.py                # FastAPIアプリケーションエントリポイント
│
├── api/                   # FastAPIルーター（プレゼンテーション層）
│   ├── routes/
│   │   ├── projects.py    # プロジェクトCRUD
│   │   ├── upload.py      # ZIPアップロード
│   │   ├── jobs.py        # 解析ジョブ管理
│   │   ├── analysis.py    # 解析結果取得
│   │   └── requirements.py # 要件取得・編集
│   ├── schemas/           # リクエスト/レスポンスのPydanticスキーマ
│   └── dependencies.py    # FastAPI依存性注入
│
├── application/           # ユースケース層
│   ├── upload_source.py   # ソースアップロード処理
│   ├── start_analysis.py  # 解析ジョブ開始
│   ├── get_analysis_result.py # 解析結果取得
│   └── export_requirements.py # 要件エクスポート
│
├── domain/                # ドメイン層（フレームワーク非依存）
│   ├── models/            # エンティティ・値オブジェクト
│   │   ├── project.py
│   │   ├── source_file.py
│   │   ├── analysis_job.py
│   │   ├── business_rule.py
│   │   └── requirement.py
│   ├── repositories/      # リポジトリインターフェース（抽象クラス）
│   └── services/          # ドメインサービス
│
├── infrastructure/        # インフラ層（外部連携）
│   ├── database/
│   │   ├── connection.py  # SQLAlchemy + asyncpg 接続設定
│   │   ├── models.py      # SQLAlchemyテーブル定義
│   │   └── repositories/  # リポジトリ実装
│   ├── storage/
│   │   └── s3_client.py   # boto3 S3操作
│   ├── llm/
│   │   └── llm_client.py  # LLM API呼び出し（意味抽出専用）
│   └── migrations/        # Alembicマイグレーション
│
└── worker/                # 非同期ジョブ（Celery or Dramatiq）
    ├── celery_app.py      # Celery設定
    ├── tasks/
    │   ├── parse_source.py    # ソースコード解析タスク
    │   ├── build_structure.py # 構造化データ生成タスク
    │   └── extract_meaning.py # LLM意味抽出タスク
    └── parsers/           # 言語別パーサー
        └── cobol_parser.py
```

### クリーンアーキテクチャルール
- 依存方向: api → application → domain ← infrastructure
- domain層は外部ライブラリに依存しない
- infrastructure層はdomain層のインターフェースを実装する
- api層はapplication層のユースケースを呼び出すだけ
- 過剰な抽象化は禁止。実装優先で必要になったら抽象化する

## データベース

- PostgreSQL
- DB名: `system-reforge`
- ユーザー: `admin`
- パスワード: `password`
