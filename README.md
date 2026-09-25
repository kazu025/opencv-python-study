# OpenCV Python Study

Python・OpenCV・NumPyで画像処理の基礎を学ぶための16本のサンプルです。

## 学習の順序

| 章 | 内容 | 本数 |
| --- | --- | --- |
| [01_basic_image](01_basic_image/README.md) | 読み込み・表示・画素値・グレースケール | 2 |
| [02_threshold_contours](02_threshold_contours/README.md) | 二値化・輪郭・面積・中心・重心・回転長方形の向き | 9 |
| [03_shape_detection](03_shape_detection/README.md) | 多角形近似・縦横比・円形度による図形判定 | 1 |
| [04_color_detection_hsv](04_color_detection_hsv/README.md) | HSVマスク・カラー抽出・物体検出 | 4 |

各章のREADMEに旧ファイル名と新ファイル名の対応を記載しています。
旧 `image_view_10.py` は反転二値化による方向検出なので、第2章に分類しています。

## 環境の準備（Windows / PowerShell）

Pythonをインストールし、リポジトリ直下で以下を実行します。
`py` がない環境では、インストールしたPythonの実行ファイルを指定してください。

```powershell
Set-Location F:\008-OpenCV
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

既存の `.venv` が起動しない場合は、作成元のPythonが利用できるか確認し、
必要に応じて仮想環境を作り直してください。
依存バージョンは [requirements.txt](requirements.txt) に記載しています。
画像表示にはデスクトップ環境とGUI対応のOpenCVが必要です。

## 入力画像

画像は各スクリプトの場所からリポジトリ直下を求めて読み込むため、作業ディレクトリに依存しません。
個人画像は配布しません。以下を各自 `images/private/` に用意してください。

| ファイル | 用途・条件 |
| --- | --- |
| sample01.jpg | 第1章。高さ101・幅201ピクセル以上のカラー画像 |
| sample02.jpg | 第2章01〜08。黒背景に明るい対象物。高さ101・幅201ピクセル以上 |
| sample03.jpg | 第2章09と第3章。白背景に黒い図形 |

整理時点ではローカルに `sample01.jpg` と `sample02.jpg` があり、`sample03.jpg` は未配置です。
第4章はコード内で画像を生成するので、画像ファイルなしで実行できます。

## 実行例

```powershell
.\.venv\Scripts\python.exe .\01_basic_image\01_read_image.py
.\.venv\Scripts\python.exe .\04_color_detection_hsv\04_multi_color_detection.py
```

画像ウィンドウにフォーカスを合わせてキーを押すと終了します。
読み込みエラーが出る場合は、入力画像の配置とファイル名を確認してください。

## Gitで管理しないファイル

[.gitignore](.gitignore) で `.venv/`、`__pycache__/`、`*.pyc`、`.vscode/`、
`images/private/`、`images/downloaded/` を除外しています。
個人画像は `images/private/` に保存してください。
すでに追跡されているファイルには除外設定が効かないため、次の両方を確認できます。

```powershell
git check-ignore -v images/private/sample01.jpg
git ls-files images/private images/downloaded
```

後者は何も表示されない状態が正常です。
`images/generated/` は公開可能な生成画像、`scripts/` は補助スクリプト、`docs/` は学習メモ用の予約ディレクトリです。
現時点で画像生成用の補助スクリプトはありません。
