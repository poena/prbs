#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : prbs_matrix_gen.py
# Author            : Changsong Li <poena@163.com>
# Date              : 02.12.2020
# Last Modified Date: 02.12.2020
# Last Modified By  : Changsong Li <poena@163.com>

import numpy as np

pseudo_predefine_dict = {'prbs_7': ['1111111', [7, 6]],
                         'prbs_9': ['111110101', [9, 5]],
                         'prbs_15': ['111110101101110', [15, 14]],
                         'prbs_16': ['1111101011011100', [16, 12, 3, 1]],
                         'prbs_20': ['11111010110111001011', [20, 3]],
                         'prbs_21': ['111110101101110010111', [21, 2]],
                         'prbs_23': ['11111010110111001011101', [23, 5]]}


def base_matrix_gen(prbs_type):

    prbs_size = len(prbs_type[0])
    prbs_idx = prbs_type[1];

    print(prbs_size);

    A = np.eye(prbs_size,k=1);
    for x in prbs_idx:
        A[-1,prbs_size-x] = 1

    print(A)
    M = A;
    for i in range(prbs_size):
        M = np.matmul(M,A)
        M = np.mod(M,2)
    print(M)
    for i in range(prbs_size):
        M = np.matmul(M,A)
        M = np.mod(M,2)
    print(M)

    return ;


if __name__ == '__main__':
    base_matrix_gen(pseudo_predefine_dict['prbs_7'])
    base_matrix_gen(pseudo_predefine_dict['prbs_23'])
