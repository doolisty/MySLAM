import cv2
import numpy as np
import collections
import matplotlib.pyplot as plt

from random import sample
import pandas as pd

img = cv2.imread("./depth.png", cv2.IMREAD_GRAYSCALE)


# def k_means(pixel, k):
#     # k-means算法具体实现
#     C = sample(pixel, 2)
#     error = 10e3
#     while error > 10e-10:
#         D = np.zeros((len(pixel), k))  # D为样本到每一个中心的距离平方，
#         for i in range(k):
#             cc = []
#             cc.append(C[i])
#             cc = np.array(cc)
#             pixel = np.array(pixel)
#             cc = np.full((len(pixel)), cc)
#             D[:, i] = np.square(pixel - cc)
#         labels = np.argmin(D, axis=1)
#         pix_dataFrame = pd.DataFrame(pixel)
#         C_2 = pix_dataFrame.groupby(labels).mean() # 计算新的中心
#         C = pd.DataFrame(C)
#         error = np.linalg.norm(C_2 - C)
#         C = np.array(C)
#         C_2 = np.array(C_2)
#         C = C_2
#     return labels, C


# find pixel stats
pattern = collections.defaultdict(int)
bucket = [0 for _ in range(26)]

h, w = img.shape
for i in range(h):
    for j in range(w):
        pattern[img[i][j]] += 1
        bucket[img[i][j] // 10] += 1

sorted_stat = sorted([(k, v) for k,v in pattern.items()], key=lambda x: x[1], reverse=True)
print(sorted_stat)
print(f"median = {sorted_stat[len(sorted_stat) // 2]}")
print([f"{i}: {val}" for i, val in enumerate(bucket)])


# k-means process depth map
data = img.reshape((h * w, 1))
data = np.float32(data)
# 定义中心 (type,max_iter,epsilon)
criteria = (cv2.TERM_CRITERIA_EPS +
            cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
# 设置标签
flags = cv2.KMEANS_RANDOM_CENTERS
# K-Means聚类 聚集成4类
compactness, labels, centers = cv2.kmeans(data, 20, None, criteria, 10, flags)
# 生成最终图像
img_kmean_20 = labels.reshape((img.shape[0], img.shape[1]))
# plt.imshow(dst, cmap='gray')
# plt.show()


# blur with conv
ker_size = 2
kernel = np.ones((ker_size, ker_size), np.float32) / ker_size**2
conv_3x3 = cv2.filter2D(img, -1, kernel)
cv2.imwrite("./dip_out/conv_3x3.png", conv_3x3)


# blur with gaussian
gaussian_11x11 = cv2.GaussianBlur(img, (11,11), 0)
cv2.imwrite("./dip_out/gaussian_11x11.png", gaussian_11x11)


# contour extraction
ori_contour = cv2.Canny(img, 10, 70)
gaussian_contour = cv2.Canny(gaussian_11x11, 10, 70)
conv_contour = cv2.Canny(conv_3x3, 10, 70)
kmean_20_contour = cv2.Canny(np.uint8(img_kmean_20), 10, 70)
cv2.imwrite("./dip_out/ori_contour.png", ori_contour)
cv2.imwrite("./dip_out/gaussian_contour.png", gaussian_contour)
cv2.imwrite("./dip_out/conv_contour.png", conv_contour)
cv2.imwrite("./dip_out/kmean_20_contour.png", kmean_20_contour)


bucket_size = 10
# bucket original image
bucketed_img_10 = np.array(img)
for i in range(h):
    for j in range(w):
        bucketed_img_10[i][j] //= bucket_size
        bucketed_img_10[i][j] *= bucket_size
cv2.imwrite("./dip_out/bucketed_img_10.png", bucketed_img_10)


# bucket conv image
bucket_img_10_conv = np.array(conv_3x3)
for i in range(h):
    for j in range(w):
        bucket_img_10_conv[i][j] //= bucket_size
        bucket_img_10_conv[i][j] *= bucket_size
cv2.imwrite("./dip_out/bucket_img_10_conv.png", bucket_img_10_conv)
