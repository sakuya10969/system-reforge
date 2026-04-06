# 要件定義書

## はじめに

System ReforgeにおけるZIPアップロード機能の要件を定義する。レガシーコード（COBOLなど）をZIPファイルでアップロードし、S3に原本保存し、ソースファイルのメタデータをDBに登録する機能である。バックエンド（FastAPI + S3 + PostgreSQL）とフロントエンド（React + Mantine + React Dropzone）の両方をカバーする。

## 用語集

- **Upload_API**: ZIPファイルのアップロードを受け付けるREST APIエンドポイント
- **S3_Client**: AWS S3へのファイルアップロード・取得を行うインフラストラクチャコンポーネント
- **ZIP_Extractor**: ZIPファイルを展開し、ソースファイルを抽出するコンポーネント
- **SourceFile**: ZIPファイル内の個別ソースファイルを表すエンティティ（id, project_id, file_path, language, s3_key, size_bytes, created_at）
- **SourceFile_Repository**: ソースファイルメタデータの永続化を担うリポジトリインターフェース
- **Upload_Page**: ZIPファイルのアップロードUIを提供するフロントエンドページ
- **Upload_Dropzone**: ドラッグ&ドロップまたはクリックでZIPファイルを選択するUIコンポーネント

## 要件

### 要件 1: ZIPファイルアップロードAPI

**ユーザーストーリー:** 解析担当者として、レガシーコードのZIPファイルをアップロードしたい。解析対象のソースコードをシステムに登録するためである。

#### 受け入れ基準

1. WHEN ユーザーが有効なZIPファイルをプロジェクトIDとともに送信した場合、THE Upload_API SHALL ZIPファイルを受け取り、展開し、各ソースファイルをS3に保存し、メタデータをDBに登録して、アップロード結果を返却する
2. WHEN ZIPファイルのContent-Typeがapplication/zipまたはapplication/x-zip-compressedでない場合、THE Upload_API SHALL バリデーションエラーを返却しアップロードを拒否する
3. WHEN 存在しないproject_idが指定された場合、THE Upload_API SHALL エラーコード"NOT_FOUND"を返却する
4. WHEN ZIPファイルが空（ソースファイルを含まない）の場合、THE Upload_API SHALL バリデーションエラーを返却する

### 要件 2: S3原本保存

**ユーザーストーリー:** 解析担当者として、アップロードしたソースコードの原本をS3に保管したい。解析時にS3からソースコードを取得するためである。

#### 受け入れ基準

1. WHEN ZIPファイルが展開された場合、THE S3_Client SHALL 各ソースファイルを `{project.s3_prefix}/sources/{file_path}` のキーでS3に保存する
2. WHEN S3へのアップロードが失敗した場合、THE Upload_API SHALL エラーを返却し、部分的にアップロードされたファイルの整合性を保つ
3. THE S3_Client SHALL アップロード時にファイルサイズ（バイト数）を取得する

### 要件 3: ソースファイルメタデータ登録

**ユーザーストーリー:** 解析担当者として、アップロードしたソースファイルのメタデータをDBに登録したい。ファイル一覧の管理と解析ジョブの入力にするためである。

#### 受け入れ基準

1. WHEN ソースファイルがS3に保存された場合、THE SourceFile_Repository SHALL 各ファイルのメタデータ（id, project_id, file_path, language, s3_key, size_bytes, created_at）をDBに一括登録する
2. WHEN ファイルの拡張子からプログラミング言語を判定できる場合、THE ZIP_Extractor SHALL 拡張子に基づいて言語を設定する（例: .cbl, .cob → COBOL, .jcl → JCL, .py → Python）
3. WHEN ファイルの拡張子から言語を判定できない場合、THE ZIP_Extractor SHALL 言語を"unknown"に設定する

### 要件 4: ZIPファイル展開

**ユーザーストーリー:** 解析担当者として、ZIPファイル内のソースファイルを正しく展開したい。各ファイルを個別に解析対象として登録するためである。

#### 受け入れ基準

1. WHEN ZIPファイルが展開される場合、THE ZIP_Extractor SHALL ディレクトリ構造を保持したファイルパスを抽出する
2. WHEN ZIPファイル内にディレクトリエントリのみ（ファイルなし）が含まれる場合、THE ZIP_Extractor SHALL ディレクトリエントリを除外し、ファイルエントリのみを処理する
3. WHEN ZIPファイルが破損している場合、THE Upload_API SHALL エラーを返却しアップロードを拒否する
4. WHEN ZIPファイル内に隠しファイル（.で始まるファイル名）やシステムファイル（__MACOSX等）が含まれる場合、THE ZIP_Extractor SHALL 隠しファイルとシステムファイルを除外する

### 要件 5: アップロードレスポンス

**ユーザーストーリー:** フロントエンド開発者として、アップロード結果の詳細を取得したい。アップロード完了後にユーザーに結果を表示するためである。

#### 受け入れ基準

1. THE Upload_API SHALL アップロード成功時に `{"data": {"project_id": "...", "uploaded_files": [...], "total_files": N, "total_size_bytes": N}}` 形式でレスポンスを返却する
2. THE Upload_API SHALL uploaded_filesの各要素に `{"file_path": "...", "language": "...", "s3_key": "...", "size_bytes": N}` を含める
3. THE Upload_API SHALL エラーレスポンスを `{"error": {"code": "...", "message": "..."}}` 形式で返却する

### 要件 6: アップロードページ（フロントエンド）

**ユーザーストーリー:** 解析担当者として、ブラウザ上でZIPファイルをアップロードしたい。直感的な操作でソースコードを登録するためである。

#### 受け入れ基準

1. WHEN ユーザーがアップロードページにアクセスした場合、THE Upload_Page SHALL ドラッグ&ドロップ対応のアップロードエリアを表示する
2. WHEN ユーザーがZIPファイルをドロップまたは選択した場合、THE Upload_Dropzone SHALL ファイル名とサイズを表示し、アップロードボタンを有効化する
3. WHEN ユーザーがZIP以外のファイルを選択した場合、THE Upload_Dropzone SHALL エラーメッセージを表示しファイルを拒否する
4. WHEN アップロードが進行中の場合、THE Upload_Page SHALL プログレス表示を行い、重複送信を防止する
5. WHEN アップロードが成功した場合、THE Upload_Page SHALL アップロード結果（ファイル数、合計サイズ）を表示する
6. WHEN アップロードでエラーが発生した場合、THE Upload_Page SHALL エラーメッセージを表示する
