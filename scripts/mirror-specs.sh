#!/bin/bash
# .kiro/specs/ → docs/specs/ への一方向ミラーリングスクリプト
#
# 正本: .kiro/specs/（Kiro管理）
# ミラー: docs/specs/（読み取り専用）
#
# docs/specs/ を直接編集しないでください。
# 変更は必ず .kiro/specs/ 側で行い、このスクリプトまたはKiroフックで同期してください。
#
# 使い方: bash scripts/mirror-specs.sh

set -euo pipefail

SRC=".kiro/specs"
DEST="docs/specs"

if [ ! -d "$SRC" ]; then
  echo "エラー: ソースディレクトリが見つかりません: $SRC"
  exit 1
fi

mkdir -p "$DEST"

# README.mdはミラー対象外（docs/specs/独自のREADMEを保持）
rsync -av --delete --exclude="README.md" "$SRC/" "$DEST/"

echo "ミラーリング完了: $SRC → $DEST（一方向同期）"
