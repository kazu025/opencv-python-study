# OpenCV Python Study

Python・OpenCV・NumPyで画像処理の基礎を学ぶための23本のサンプルです（第1〜5章。補助スクリプトを除く）。

## 学習の順序

| 章 | 内容 | 本数 |
| --- | --- | --- |
| [01_basic_image](01_basic_image/README.md) | 読み込み・表示・画素値・グレースケール | 2 |
| [02_threshold_contours](02_threshold_contours/README.md) | 二値化・輪郭・面積・中心・重心・回転長方形の向き | 9 |
| [03_shape_detection](03_shape_detection/README.md) | 多角形近似・縦横比・円形度による図形判定 | 1 |
| [04_color_detection_hsv](04_color_detection_hsv/README.md) | HSVマスク・カラー抽出・物体検出 | 4 |
| [05_edge_detection](05_edge_detection/README.md) | Cannyエッジ検出・閾値比較・GaussianBlur・輪郭取得・面積フィルタ | 7 |

## ディレクトリ構成

```text
008-OpenCV/
├── 01_basic_image/
├── 02_threshold_contours/
├── 03_shape_detection/
├── 04_color_detection_hsv/
├── 05_edge_detection/
├── docs/
├── images/
├── scripts/
├── .gitignore
├── README.md
└── requirements.txt
```

## 第5章：エッジ検出から面積フィルタまで

[05_edge_detection](05_edge_detection/README.md)では、コード内で生成した図形を使い、
Cannyの閾値、背景との明暗差、GaussianBlurの有無とカーネルサイズによる違いを比較します。
さらに、エッジ画像から輪郭を取得し、面積・外接長方形を調べ、小さい輪郭を除外します。

最後の`07_contour_filter.py`では、検出した5つの輪郭のうち、
面積条件を通過した大きな長方形と円の2つに赤い輪郭を描きます。
端末に表示する「検出した輪郭数」はフィルタ前の件数です。
今回の図形では面積閾値を500から1000に変更しても、条件を通過する輪郭は2つのままです。

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

`sample03.jpg`は[scripts/create_test_images.py](scripts/create_test_images.py)で生成できます。
この補助スクリプトは、同名の画像がすでにある場合には上書きせず停止します。
第4・5章はコード内で画像を生成するので、画像ファイルなしで実行できます。

## 実行例

```powershell
.\.venv\Scripts\python.exe .\01_basic_image\01_read_image.py
.\.venv\Scripts\python.exe .\04_color_detection_hsv\04_multi_color_detection.py
.\.venv\Scripts\python.exe .\05_edge_detection\07_contour_filter.py
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
`scripts/create_test_images.py`は、第2章09と第3章で使う図形画像を生成する補助スクリプトです。
