# 画像の基礎

番号順に実行して学習するOpenCVサンプルです。

## サンプル一覧

| ファイル | 旧ファイル名 | 学習内容 |
| --- | --- | --- |
| [01_read_image.py](01_read_image.py) | image_view_00.py | 画像の読み込み・表示、配列の型・サイズ・画素値 |
| [02_pixel_value_grayscale.py](02_pixel_value_grayscale.py) | image_view_01.py | BGR画素値とグレースケール変換 |

## 入力と前提

`images/private/sample01.jpg` を用意します。画素 `[100, 200]` を参照するため、高さ101・幅201ピクセル以上が必要です。

## 実行

環境の準備は[トップREADME](../README.md)を参照してください。リポジトリ直下で実行します。

```powershell
.\.venv\Scripts\python.exe .\01_basic_image\01_read_image.py
```

実行するファイル名を切り替えてください。画像ウィンドウにフォーカスを合わせてキーを押すと終了します。
