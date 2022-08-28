from PIL import Image
import numpy as np
import time
import matplotlib.pyplot as plt
from params_of_program import *


def two_for_high_y(x_, y_, array):
    for j_ in range(0, y_):  # Пробегаем по координате y
        for i_ in range(0, x_):  # Пробегаем по коорденате x
            if not np.array_equal(array[j_][i_], [255, 255, 255]):
                return j_


def two_for_low_y(x_, y_, array):
    for j_ in range(y_ - 1, -1, -1):  # Пробегаем по координате y
        for i_ in range(0, x_):  # Пробегаем по коорденате x
            if not np.array_equal(array[j_][i_], [255, 255, 255]):
                return j_


def two_for_left_x(x_, y_, array):
    for i_ in range(0, x_):       # Пробегаем по координате x
        for j_ in range(0, y_):   # Пробегаем по коорденате y
            if not np.array_equal(array[j_][i_], [255, 255, 255]):
                return i_


def two_for_right_x(x_, y_, array):
    for i_ in range(x_ - 1, -1, -1):        # Пробегаем по координате x
        for j_ in range(0, y_):             # Пробегаем по коорденате y
            if not np.array_equal(array[j_][i_], [255, 255, 255]):
                return i_


def cropped_img(img_file):
    with Image.open(img_file) as img:
        img.load()

    (x, y) = img.size  # Через атрибут size получаем кортеж с двумя элементами (размер изображения по x и y)
    # print('крайнеий х =', x, 'крайний у =', y)
    img_array = np.asarray(img)
    # print(img_array[1][1])
    # Образаем план до первого черного пикселя в строке сверху, справа, снизу, слева:
    left_x = two_for_left_x(x, y, img_array)
    right_x = two_for_right_x(x, y, img_array)
    high_y = two_for_high_y(x, y, img_array)
    low_y = two_for_low_y(x, y, img_array)
    # print(left_x, high_y, right_x, low_y)
    return img.crop((left_x, high_y, right_x, low_y))


def pic_detect(search_file, template_file, x=0, y=0):
    (dx, dy) = template_file.size
    qqq = search_file.crop((x, y, x + dx, y + dy))
    count = 0
    count_pls = 0
    for ii in range(0, dy - 1):
        for ee in range(0, dx - 1):
            count += 1
            if qqq.getpixel((ee, ii)) == template_file.getpixel((ee, ii)):
                count_pls += 1
    return count_pls / count * 100


def view_creator():
    # z = []
    crop_big = cropped_img(INPUT_LIVING_ROOM_FILE)
    crop_small = cropped_img(INPUT_FINDING_ROOM_FILE)
    gray_crop_big = crop_big.convert("L")  # Grayscale
    img_crop_big = gray_crop_big.convert("1")
    gray_crop_small = crop_small.convert("L")
    img_crop_small = gray_crop_small.convert("1")
    (x_size, y_size) = img_crop_big.size
    # print(x_size, y_size)
    x_ = list(range(0, x_size, STEP))
    y_ = list(range(0, y_size, STEP))
    # print(x_)
    # print(y_)
    x, y = np.meshgrid(np.array(x_), np.array(y_))
    x_len = len(x_)
    y_len = len(y_)
    z = np.zeros((y_len, x_len))
    for ii in range(0, len(y_)):
        for jj in range(0, len(x_)):
            z[ii][jj] = pic_detect(img_crop_big, img_crop_small, x_[jj], y_[ii])
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    ax.plot_wireframe(x, y, z, color="green")     # plot_surface(x, y, z)
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_time = time.time()
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(f"Время начала расчетв: {current_time}.")
    view_creator()
    print("--- %s seconds ---" % (time.time() - start_time))
