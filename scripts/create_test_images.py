from pathlib import Path

import cv2
import numpy as np


# 保存先：リポジトリ直下の images/private/sample03.jpg
output_path = (
    Path(__file__).resolve().parents[1]
    / "images"
    / "private"
    / "sample03.jpg"
)
output_path.parent.mkdir(parents=True, exist_ok=True)

# 既存画像を誤って上書きしない
if output_path.exists():
    raise FileExistsError(
        f"画像がすでにあります。名前を変更してから実行してください: {output_path}"
    )

# 高さ600 × 幅900の白いカラー画像
image = np.full((600, 900, 3), 255, dtype=np.uint8)
black = (0, 0, 0)

# 三角形
triangle = np.array(
    [[150, 60], [60, 240], [240, 240]],
    dtype=np.int32,
)
cv2.fillPoly(image, [triangle], black)

# 正方形
cv2.rectangle(image, (330, 70), (500, 240), black, -1)

# 長方形
cv2.rectangle(image, (600, 100), (840, 230), black, -1)

# 円
cv2.circle(image, (200, 440), 100, black, -1)

# 楕円
cv2.ellipse(
    image,
    (620, 440),   # 中心
    (150, 75),    # 横・縦方向の半径
    20,          # 回転角度
    0, 360,      # 描画範囲
    black,
    -1,          # 塗りつぶし
)

# JPEG形式で保存
if not cv2.imwrite(str(output_path), image):
    raise RuntimeError(f"画像を保存できませんでした: {output_path}")

print(f"保存しました: {output_path}")

cv2.imshow("Sample 03", image)
cv2.waitKey(0)
cv2.destroyAllWindows()