import random
import unittest
from random import shuffle

import cv2 as cv
import numpy as np

from data_generator import generate_trimap
from trimap_dict import trimap_init, trimap_add, trimap_get


class TestStringMethods(unittest.TestCase):

    def test_generate_trimap(self):
        alpha = cv.imread('mask/035A4301.jpg', 0)
        trimap = generate_trimap(alpha)

    def test_isupper(self):
        num_fgs = 431
        num_bgs = 43100
        num_bgs_per_fg = 100
        num_valid_samples = 8620
        names = []
        bcount = 0
        for fcount in range(num_fgs):
            for i in range(num_bgs_per_fg):
                names.append(str(fcount) + '_' + str(bcount) + '.png')
                bcount += 1

        valid_names = random.sample(names, num_valid_samples)
        train_names = [n for n in names if n not in valid_names]
        shuffle(valid_names)
        shuffle(train_names)

        with open('valid_names.txt', 'w') as file:
            file.write('\n'.join(valid_names))

        with open('train_names.txt', 'w') as file:
            file.write('\n'.join(train_names))

    def test_split(self):
        trimap_init()

        alpha = cv.imread('images/0_0_alpha.png')
        trimap = cv.imread('images/0_0_trimap.png')

        trimap_add(alpha, trimap)
        new_trimap = trimap_get(alpha)

        self.assertTrue(np.array_equal(trimap, new_trimap))


if __name__ == '__main__':
    unittest.main()
