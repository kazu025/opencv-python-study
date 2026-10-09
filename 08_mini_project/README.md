# 小さなOpenCVプロジェクト

色検出・動体検出・動画保存など、これまで学習した機能を組み合わせます。
カメラ映像を録画し、その動画に画像処理を適用して保存します。

## サンプル一覧

| ファイル | 学習内容 |
| --- | --- |
| [01_color_object_tracker.py](01_color_object_tracker.py) | 青色物体の検出・中心点・移動軌跡の表示 |
| [02_motion_detection.py](02_motion_detection.py) | 背景差分による動体検出 |
| [03_face_detection.py](03_face_detection.py) | 顔検出（現在は保留） |
| [04_save_video.py](04_save_video.py) | カメラ映像をMP4として保存 |
| [05_play_video.py](05_play_video.py) | 保存した動画の読み込みと再生 |
| [06_save_grayscale_video.py](06_save_grayscale_video.py) | グレースケール動画の保存 |
| [07_save_threshold_video.py](07_save_threshold_video.py) | 二値化した動画の保存 |
| [08_save_edge_video.py](08_save_edge_video.py) | Cannyエッジ検出結果の保存 |
| [09_save_contour_video.py](09_save_contour_video.py) | 輪郭の外接長方形を描画して保存 |
| [10_save_blue_tracking_video.py](10_save_blue_tracking_video.py) | 青色物体の外接長方形と中心点を保存 |
| [11_save_motion_video.py](11_save_motion_video.py) | 動体検出結果を保存 |
| [12_save_tracking_trail_video.py](12_save_tracking_trail_video.py) | 青色物体の移動軌跡を保存 |
| [13_add_video_info.py](13_add_video_info.py) | フレーム番号と動画内の経過時間を表示 |
| [14_resize_video.py](14_resize_video.py) | 動画の幅と高さを半分にして保存 |
| [15_compare_video.py](15_compare_video.py) | 元映像とグレースケール映像を左右に並べて保存 |

## 準備

環境の準備は[トップREADME](../README.md)を参照してください。

カメラを使用するサンプルでは、PC内蔵カメラまたはUSBカメラを使用します。
カメラ番号は `cv2.VideoCapture(0)` の `0` で指定します。
複数のカメラがある場合は、番号を `1` などに変更してください。

動画の保存先として、次のディレクトリを用意してください。

```text
images/private/
```

まず `04_save_video.py` を実行し、次の動画を作成します。

```text
images/private/camera_record.mp4
```

`05`〜`15` のサンプルは、この動画を入力として使用します。

`images/private/` は `.gitignore` の除外対象です。
入力動画と出力動画はGitHubに含まれないため、手元で用意してください。

## 実行方法

リポジトリ直下で実行してください。

カメラ映像を録画します。

```powershell
.\.venv\Scripts\python.exe .\08_mini_project\04_save_video.py
```

保存した動画を再生します。

```powershell
.\.venv\Scripts\python.exe .\08_mini_project\05_play_video.py
```

実行するファイル名を変更すると、ほかのサンプルを試せます。

表示ウィンドウを選択し、`q` を押すと終了します。
動画ファイルを処理するサンプルは、動画の末尾でも終了します。
途中で終了した場合、そこまでの映像が保存されます。

## 処理の流れ

1. `VideoCapture()` でカメラまたは動画を開く
2. 入力映像の幅・高さ・FPSを取得する
3. `VideoWriter()` で保存先と動画形式を設定する
4. `read()` で1フレームを取得する
5. フレームに画像処理や描画を適用する
6. `write()` で保存し、`imshow()` で表示する
7. 終了時に `release()` で入力と出力を解放する

グレースケール・二値化・エッジ検出の結果は1チャンネル画像です。
今回の保存コードでは、`COLOR_GRAY2BGR` で3チャンネルに変換してから書き込みます。
変換後も見た目は白黒のままです。

## 調整する値

- `fps`：保存する動画の1秒あたりのフレーム数
- `threshold_value`：二値化のしきい値
- `500`：描画対象にする輪郭の最小面積
- `lower_blue` / `upper_blue`：青色のHSV範囲
- `cv2.Canny()` の `50` / `150`：エッジ検出のしきい値
- `deque(maxlen=50)`：保持する中心点の最大数
- `width` / `height`：保存する動画の幅と高さ

HSVによる色検出は照明や撮影環境によって結果が変わります。
映像を見ながら範囲を調整してください。

## 検出結果について

青色物体の検出では、各フレームで最も面積の大きい青色の輪郭を選びます。
複数の青色物体がある場合は、検出対象が切り替わることがあります。

背景差分による動体検出は、カメラを固定して試してください。
処理開始直後は背景を学習しているため、広い範囲が検出されることがあります。

`13_add_video_info.py` の経過時間は、フレーム番号とFPSから計算した動画内の時間です。

## 保存する動画について

出力形式はMP4、圧縮方式は `mp4v` を指定しています。
保存するフレームのサイズは、`VideoWriter()` に指定したサイズと一致させます。

同じサンプルを再実行すると、同名の出力動画を上書きします。
これらのコードでは音声は保存しません。

`waitKey()` は表示とキー入力に使います。
保存動画の再生速度は、書き込んだフレーム数と指定したFPSによって決まります。

## 顔検出について

`03_face_detection.py` は、現在の環境で
`cv2.CascadeClassifier` が利用できないため保留しています。

## カメラや動画が開けない場合

- カメラが接続されているか確認する
- Windowsのカメラ設定で、デスクトップアプリのアクセスを許可する
- カメラを使用中のほかのアプリを閉じる
- カメラ番号を変更する
- `images/private/camera_record.mp4` が存在するか確認する

動画が保存されない場合は、保存先ディレクトリと書き込み権限を確認してください。