#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : prbs_matrix_gen.py
# Author            : Changsong Li <poena@163.com>
# Date              : 02.12.2020
# Last Modified Date: 02.12.2020
# Last Modified By  : Changsong Li <poena@163.com>

import numpy as np

pseudo_predefine_dict = {'prbs_7': [0xff, [7, 6]],
                         'prbs_9': [0x1f5, [9, 5]],
                         'prbs_15': [0x7d6e, [15, 14]],
                         'prbs_23': ['0x7d6e5d', [23, 18]],
                         'prbs_31': ['0x7ffae000', [31, 18]]}


def base_matrix_gen(prbs_type):

    print(prbs_type)
    prbs_size = prbs_type[0]
    prbs_idx = prbs_type

    print(prbs_size)

    A = np.eye(prbs_size,k=1)
    for x in prbs_idx:
        A[-1,prbs_size-x] = 1

    print(A)
    M = A;
    for i in range(prbs_size-1):
        M = np.matmul(M,A)
        M = np.mod(M,2)
    print(M)

    #for i in range(prbs_size):
    #    M = np.matmul(M,A)
    #    M = np.mod(M,2)
    #print(M)

    return M

def prbs_next(curr_state,prbs_mode):
    prbs_expr = pseudo_predefine_dict[prbs_mode]
    prbs_len = prbs_expr[1][0]
    print(['prbs_len:',prbs_len])

    get_bin = lambda x, n: format(x, 'b').zfill(n)
    value_bin = get_bin(curr_state,prbs_len)[0:prbs_len]
    value_list = [int(i) for i in list(value_bin)]
    M = base_matrix_gen(prbs_expr[1])
    print(np.array(value_list))
    print(M)
    Nx = np.matmul(M,value_list)
    print(np.mod(Nx,2))


if __name__ == '__main__':
    #base_matrix_gen(pseudo_predefine_dict['prbs_7'])
    #base_matrix_gen(pseudo_predefine_dict['prbs_23'])
    prbs_next(0x01,'prbs_7')
    #prbs_next(0xff,'prbs_7')

