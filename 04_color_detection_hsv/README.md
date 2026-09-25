# HSV色検出

番号順に実行して学習するOpenCVサンプルです。

## サンプル一覧

| ファイル | 旧ファイル名 | 学習内容 |
| --- | --- | --- |
| [01_hsv_blue_mask.py](01_hsv_blue_mask.py) | image_view_12.py | 青色マスクの作成と青色領域の外接長方形 |
| [02_bitwise_and.py](02_bitwise_and.py) | image_view_13.py | マスクを使った青色部分のカラー抽出 |
| [03_blue_object_detection.py](03_blue_object_detection.py) | image_view_14.py | 青色物体の位置・大きさ・中心の取得 |
| [04_multi_color_detection.py](04_multi_color_detection.py) | image_view_15.py | 赤・緑・青・黄の物体検出 |

## 入力と前提

外部画像は不要です。各スクリプト内で赤い四角形・緑の円・青い四角形・黄色の円を生成します。

OpenCVの8ビットHSVではHは0〜179、S/Vは0〜255です。この例の赤はH=0付近のみを対象としています。

## 実行

環境の準備は[トップREADME](../README.md)を参照してください。リポジトリ直下で実行します。

```powershell
.\.venv\Scripts\python.exe .\04_color_detection_hsv\01_hsv_blue_mask.py
```

実行するファイル名を切り替えてください。画像ウィンドウにフォーカスを合わせてキーを押すと終了します。
