import cv2
import numpy as np
from PIL import Image

# 画像のオーバーレイ
def overlayImage(src, overlay, location):
    overlay_height, overlay_width = overlay.shape[:2]

    # 背景をPIL形式に変換
    src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    pil_src = Image.fromarray(src)
    pil_src = pil_src.convert('RGBA')

    # オーバーレイをPIL形式に変換
    overlay = cv2.cvtColor(overlay, cv2.COLOR_BGRA2RGBA)
    pil_overlay = Image.fromarray(overlay)
    pil_overlay = pil_overlay.convert('RGBA')

    # 画像を合成
    pil_tmp = Image.new('RGBA', pil_src.size, (255, 255, 255, 0))
    pil_tmp.paste(pil_overlay, location, pil_overlay)
    result_image = Image.alpha_composite(pil_src, pil_tmp)

    # OpenCV形式に変換
    return cv2.cvtColor(np.asarray(result_image), cv2.COLOR_RGBA2BGRA)


def main(file_path):
    try:
        # ダウンロードしたファイルを指定
        cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        # 検出する画像ファイル読み込み
        image = cv2.imread("static/" + file_path, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        #cv2.imwrite('grayscale.png', gray)
        # 検出実行
        faces = cascade.detectMultiScale(gray,
                                            # detector options
                                            scaleFactor = 1.1,
                                            minNeighbors = 5,
                                            minSize = (24, 24))
        # 検出結果を描画
        for (x, y, w, h) in faces:
            # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # 重ねる画像
            img = cv2.imread("sabal_mask.png", cv2.IMREAD_UNCHANGED)

            # 画像重ねる。位置調整。サイズ調整
            size = (w*2, h*2+30)
            img = cv2.resize(img, size)

            # 画像のオーバーレイ
            image = overlayImage(image, img, (x - int(w / 2), y - int(h + 20)))
        # 結果を出力
        cv2.imwrite("static/" + file_path, image)

    except Exception as e:
        print(e)
    return 'OK'
