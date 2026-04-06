# アーキテクチャ思想

## 全体方針

- フロントエンドとバックエンドは完全に分離（API経由で通信）
- フロントエンドはFSD（Feature-Sliced Design）で責務分離
- バックエンドはクリーンアーキテクチャでレイヤー分離
- 過剰な抽象化は禁止。実装優先で、必要になったら抽象化する

---

## フロントエンド：FSD（Feature-Sliced Design）

### レイヤー構成（上位 → 下位）

| レイヤー | 役割 | 例 |
|----------|------|-----|
| app | エントリポイント・プロバイダ・グローバル設定 | root.tsx, providers |
| processes | アプリレベルの複合フロー | 解析ジョブ全体フロー |
| pages | ルート単位のページ | upload, analysis, dependencies, requirements |
| widgets | ページ内の独立UIブロック | job-list, flow-graph, rule-table |
| features | ユーザー操作に対応する機能単位 | upload-zip, start-analysis, export-requirements |
| entities | ドメインモデル・API型定義 | project, job, source-file, business-rule, requirement |
| shared | 共通ユーティリティ | api, ui, lib, config |

### ルール

- 依存方向は上位 → 下位のみ（pages → widgets → features → entities → shared）
- 同一レイヤー内のモジュール間は直接参照しない
- 各モジュールは `index.ts` で公開APIを定義する
- 逆方向の依存は禁止

### 状態管理の分離

| 状態の種類 | 管理方法 |
|-----------|---------|
| サーバー状態（APIデータ） | React Query |
| UI状態（モーダル開閉、選択状態） | Jotai or Zustand |
| フォーム状態 | React Hook Form + Zod |

React Queryがサーバー状態のキャッシュ・同期を担当するため、グローバルストアにAPIデータを入れない。

---

## バックエンド：クリーンアーキテクチャ

### レイヤー構成

```
api → application → domain ← infrastructure
```

| レイヤー | 役割 | 依存先 |
|----------|------|--------|
| api | FastAPIルーター。リクエスト受付・レスポンス返却 | application |
| application | ユースケース。ビジネスフローの調整 | domain |
| domain | エンティティ・ビジネスルール。フレームワーク非依存 | なし |
| infrastructure | DB・S3・LLMなど外部連携の実装 | domain（インターフェース実装） |

### ルール

- api層はapplication層のユースケースを呼び出すだけ。ビジネスロジックを書かない
- application層はドメインモデルとリポジトリインターフェースを使う。インフラの具体実装を知らない
- domain層は外部ライブラリに依存しない。純粋なPythonで書く
- infrastructure層はdomain層で定義されたリポジトリインターフェースを実装する
- 依存性注入でinfrastructure → domain の接続を行う（FastAPIのDepends）

### 非同期処理の原則

- 解析処理はAPIで同期実行しない。バックグラウンドタスク（FastAPIのBackgroundTasksなど）で実行
- APIはジョブを作成して即座にレスポンスを返す
- フロントエンドはポーリングまたはWebSocketでジョブ状態を監視

### LLMの利用原則

- LLMは意味抽出専用。コード生成やコード変換には使わない
- LLMにソースコードを直接渡さない。構造化された中間データ（AST、依存関係、フロー情報）を入力とする
- 中間データの生成は省略しない
