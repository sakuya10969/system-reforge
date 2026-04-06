# Client

React Router v7 ベースのフロントエンド。

## 開発

```bash
bun install
bun run dev
```

デフォルトでは `http://localhost:5173` で起動する。

## API 接続

SSR 実行時にも FastAPI へ正しく接続できるよう、API ベース URL は相対パスではなくオリジン指定で解決する。

開発時は `client/.env.local` などに以下を設定する。

```bash
VITE_API_ORIGIN=http://localhost:8000
```

未設定時は `http://localhost:8000` を使用する。

## 型チェック

```bash
bun run typecheck
```
