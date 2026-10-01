# カメラ映像の画像処理

PC内蔵カメラやUSBカメラの映像に、グレースケール化・二値化・輪郭検出・色検出を適用します。

## サンプル一覧

| ファイル | 学習内容 |
| --- | --- |
| [01_open_camera.py](01_open_camera.py) | カメラ映像の読み込みと表示 |
| [02_camera_grayscale.py](02_camera_grayscale.py) | グレースケール化 |
| [03_camera_threshold.py](03_camera_threshold.py) | 二値化 |
| [04_camera_contours.py](04_camera_contours.py) | 輪郭検出 |
| [05_camera_contour_area.py](05_camera_contour_area.py) | 面積で小さな輪郭を除外 |
| [06_camera_bounding_rect.py](06_camera_bounding_rect.py) | 外接長方形の描画 |
| [07_camera_rect_center.py](07_camera_rect_center.py) | 外接長方形の中心を表示 |
| [08_camera_moments_centroid.py](08_camera_moments_centroid.py) | 輪郭の重心を表示 |
| [09_camera_min_area_rect.py](09_camera_min_area_rect.py) | 回転した最小面積長方形の描画 |
| [10_camera_shape_detection.py](10_camera_shape_detection.py) | 頂点数と縦横比による簡易図形判定 |
| [11_camera_hsv_blue_detection.py](11_camera_hsv_blue_detection.py) | 青色マスク・カラー抽出・輪郭検出 |
| [12_camera_multi_color_detection.py](12_camera_multi_color_detection.py) | 赤・緑・青・黄色の検出 |
| [13_camera_bitwise_and.py](13_camera_bitwise_and.py) | マスクを使った青色部分のカラー抽出 |
| [14_camera_blue_object_position.py](14_camera_blue_object_position.py) | 青色物体の外接長方形と中心座標 |
| [15_camera_multi_color_center.py](15_camera_multi_color_center.py) | 複数色の外接長方形と中心座標 |

## 準備

環境の準備は[トップREADME](../README.md)を参照してください。

PC内蔵カメラ、または接続したUSBカメラを使用します。
画像・動画ファイルの用意は不要です。

各サンプルでは、カメラ番号を次のように指定します。

```python
camera_number = 0
capture = cv2.VideoCapture(camera_number)
```

複数のカメラがある場合は、番号を `1` などに変更してください。
番号とカメラの対応は環境によって異なります。

## 実行方法

リポジトリ直下で実行してください。

```powershell
.\.venv\Scripts\python.exe .\07_usb_camera\01_open_camera.py
```

実行するファイル名を変更すると、ほかのサンプルを試せます。

表示ウィンドウを選択し、`q` または `Esc` を押すと終了します。
終了時にカメラと表示ウィンドウを閉じます。
これらのサンプルは映像を表示するだけで、録画・保存は行いません。

## 処理の流れ

1. `VideoCapture()` でカメラを開く
2. `read()` で1フレームを取得する
3. フレームに画像処理を適用する
4. `imshow()` で結果を表示する
5. 終了キーが押されるまで繰り返す
6. `release()` でカメラを解放する

第6章の動画処理と同じように、各フレームを静止画像として処理します。

## 調整する値

- `threshold_value = 128`：二値化のしきい値
- `min_area = 500`：描画対象にする輪郭の最小面積
- `lower_blue` / `upper_blue`：青色のHSV範囲
- `color_ranges`：複数色のHSV範囲と描画色

`THRESH_BINARY` は、画素値がしきい値より大きければ白、それ以下なら黒にします。
図形判定のサンプルは `THRESH_BINARY_INV` を使い、明るい背景の暗い図形を対象にします。

HSVによる色検出は照明やカメラの設定で結果が変わるため、
映像を見ながら範囲を調整してください。
現在の赤色の設定は、色相Hの0〜10のみです。
170〜179付近の赤も対象にする場合は、もう1つの範囲のマスクを作って結合します。

## 検出結果について

図形判定は、頂点数と縦横比を使う学習用の簡易判定です。
白い紙に黒い図形を描くなど、背景と対象が分かれた環境で試してください。
複雑な背景や不規則な形では、誤判定することがあります。

各フレームで輪郭を検出しているため、同じ物体を継続して追跡する機能はありません。
中心や重心が大きく動く場合は、背景の混入や輪郭の分裂・結合も確認してください。

## カメラが開けない場合

- カメラが接続されているか確認する
- Windowsのカメラ設定で、デスクトップアプリのアクセスを許可する
- カメラを使用中のほかのアプリを閉じる
- `camera_number` を変更する