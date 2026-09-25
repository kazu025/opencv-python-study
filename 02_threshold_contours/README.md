# 二値化と輪郭

番号順に実行して学習するOpenCVサンプルです。

## サンプル一覧

| ファイル | 学習内容 |
| --- | --- |
| [01_threshold.py](01_threshold.py) | しきい値128による二値化 |
| [02_find_contours.py](02_find_contours.py) | 外側の輪郭の検出と描画 |
| [03_contour_area.py](03_contour_area.py) | 面積による小さな輪郭の除外 |
| [04_bounding_rect.py](04_bounding_rect.py) | 外接長方形の位置と大きさ |
| [05_rect_center.py](05_rect_center.py) | 外接長方形の中心座標 |
| [06_moments_centroid.py](06_moments_centroid.py) | 輪郭の重心と外接長方形の中心の比較 |
| [07_min_area_rect.py](07_min_area_rect.py) | 回転を許した最小面積長方形 |
| [08_rect_direction.py](08_rect_direction.py) | 長辺の向きと角度の可視化 |
| [09_rect_direction_inverted.py](09_rect_direction_inverted.py) | 白背景・黒図形を反転二値化し、長辺の向きを可視化 |

## 入力と前提

`01`〜`08` は `images/private/sample02.jpg`（黒背景・明るい対象物）を使用します。`01` は画素 `[100, 200]` を参照するため、高さ101・幅201ピクセル以上が必要です。

`09` は `images/private/sample03.jpg`（白背景・黒い図形）を使用し、反転二値化します。面積で除外する例では500ピクセル以上の輪郭が対象です。

## 実行

環境の準備は[トップREADME](../README.md)を参照してください。リポジトリ直下で実行します。

```powershell
.\.venv\Scripts\python.exe .\02_threshold_contours\01_threshold.py
```

実行するファイル名を切り替えてください。画像ウィンドウにフォーカスを合わせてキーを押すと終了します。
