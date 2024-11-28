import cv2
import os

path = os.getcwd() + '/Image/'

# 読み込む画像のパスを指定
path_ = "/Users/haya/Development/aniversity_lecture/mirai_pj/test_pictures/温泉_1_夏_昼.jpg"
# 読み込む画像を選択
img = cv2.imread(path_)

# リサイズ前の画像サイズ出力
print("(高さ,幅,色)="+str(img.shape))

#　リサイズするサイズ（幅、高さ）
size = (600,400)

# 画像の拡大・縮小（INTER_NEAREST)
img_inter_nearest = cv2.resize(img,size,interpolation = cv2.INTER_NEAREST)

# # リサイズ後の画像サイズ出力
print("(高さ, 幅, 色)="+str(img_inter_nearest.shape))

# 画像表示
cv2.imshow("nearest",img_inter_nearest)
cv2.waitKey(0)
cv2.destroyAllWindows()