# 動画処理

動画ファイルをフレーム単位で読み込み、静止画像で学んだ処理を動画へ適用します。

## サンプル一覧

### 基本動画処理

| ファイル | 学習内容 |
| --- | --- |
| [01_read_video.py](01_basic_video/01_read_video.py) | 動画の読み込みとフレーム表示 |
| [02_video_grayscale.py](01_basic_video/02_video_grayscale.py) | フレームのグレースケール化 |
| [03_video_threshold.py](01_basic_video/03_video_threshold.py) | フレームの二値化 |

### 輪郭・図形検出

| ファイル | 学習内容 |
| --- | --- |
| [04_video_contours.py](02_video_contours/04_video_contours.py) | フレームから輪郭を検出 |
| [05_contour_area.py](02_video_contours/05_contour_area.py) | 面積で小さな輪郭を除外 |
| [06_bounding_rect.py](02_video_contours/06_bounding_rect.py) | 外接長方形を描画 |
| [07_rect_center.py](02_video_contours/07_rect_center.py) | 外接長方形の中心を表示 |
| [08_moments_centroid.py](02_video_contours/08_moments_centroid.py) | 輪郭の重心を表示 |
| [09_min_area_rect.py](02_video_contours/09_min_area_rect.py) | 回転長方形を描画 |
| [10_shape_detection.py](02_video_contours/10_shape_detection.py) | 動画中の図形を判定 |

### 色検出

| ファイル | 学習内容 |
| --- | --- |
| [11_hsv_blue_detection.py](03_video_color/11_hsv_blue_detection.py) | 青色領域の検出 |
| [12_multi_color_detection.py](03_video_color/12_multi_color_detection.py) | 複数色の検出 |
| [13_bitwise_and.py](03_video_color/13_bitwise_and.py) | 青色部分のカラー抽出 |
| [14_blue_object_position.py](03_video_color/14_blue_object_position.py) | 青色物体の位置・中心 |
| [15_multi_color_center.py](03_video_color/15_multi_color_center.py) | 複数色の中心座標 |

## 入力動画

動画ファイルを `images/private/sample01.mp4` に保存してください。
`images/private/` は `.gitignore` の対象なので、個人動画はGitHubへpushされません。

## 実行例

```powershell
.\.venv\Scripts\python.exe .\06_video\01_basic_video\01_read_video.py
```

動画ウィンドウにフォーカスを合わせて `q` または `Esc` を押すと終了します。
