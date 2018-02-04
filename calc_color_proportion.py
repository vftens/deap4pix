from PIL import Image
import operator
import numpy as np


def get_color_proportion(img):
    cp = {}

    for pixel in img.getdata():
        if pixel in cp:
            cp[pixel] += 1
        else:
            cp[pixel] = 1

    sum_cp = sum(cp.values())

    for k in cp:
        cp[k] /= sum_cp

    return cp


def get_diff_by_pixels(img1, img2, weights_mask):
    d1 = np.array(img1).reshape(img1.size[1], img1.size[0], 4)
    d2 = np.array(img2).reshape(img2.size[1], img2.size[0], 4)
    diff = np.invert(d1 == d2).astype(int)
    diff = diff.sum(axis=2)
    return (diff.flatten() * weights_mask).sum()


def get_mse_by_pixels(img1, img2, weights_mask):
    d1 = np.array(img1.getdata())
    d2 = np.array(img2.getdata())
    mse = ((d1 - d2) ** 2).mean(axis=1)
    return np.log1p((mse * weights_mask).mean())


if __name__ == "__main__":
    # sorted_cp = sorted(get_color_proportion(img).items(), key=operator.itemgetter(1), reverse=True)
    # for color, count in sorted_cp:
    #     print(color, count)
    img = Image.open('out.png')
    img_test = Image.open('tmp.png')
    color_proportion = get_color_proportion(img)
    wm = np.array([color_proportion[x] for x in img.getdata()])
    print('Equal images: ', get_diff_by_pixels(img, img, weights_mask=wm))
    print('Different images: ', get_diff_by_pixels(img, img_test, weights_mask=wm))
