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

def bin2hex(bin_list,out_len):
    total_len = len(bin_list)
    grp_num = (total_len+out_len-1)//out_len
    rtn_list=[]
    for i in range(grp_num):
        grp_char = ''.join([str(elem) for elem in bin_list[i*out_len:(i+1)*out_len]])
        grp_hex = '{0:#{fill}{width}x}'.format(int(grp_char,2), fill='0', width=(out_len//4+2))
        rtn_list.append(grp_hex)
        #print('{0:#{fill}{width}x}'.format(int(grp_char,2), fill='0', width=(out_len//4+2)))

    return rtn_list

def base_matrix_gen(prbs_type,parallel_width):

    print(prbs_type)
    prbs_size = prbs_type[0]
    prbs_idx = prbs_type

    para_grp = (parallel_width+prbs_size-1)//prbs_size

    print(prbs_size)

    MM = np.zeros([para_grp*prbs_size,prbs_size],dtype='int')
    A = np.eye(prbs_size,k=1,dtype='int')
    for x in prbs_idx:
        A[-1,prbs_size-x] = 1

    print(A)
    #M[0:prbs_size,:] = A;
    M = A;
    for j in range(para_grp):
        for i in range(prbs_size):
            if(i==0 and j==0):
                M = A
            else:
                M = np.matmul(M,A)
                M = np.mod(M,2)
        print(M)
        MM[j*prbs_size:(j+1)*prbs_size] = M

    #MM = M
    #for i in range(prbs_size):
    #    M = np.matmul(M,A)
    #    M = np.mod(M,2)
    #print(M)

    return MM[0:parallel_width,:]

def prbs_next(curr_state,prbs_mode,parallel_width):
    prbs_expr = pseudo_predefine_dict[prbs_mode]
    prbs_len = prbs_expr[1][0]
    print(['prbs_len:',prbs_len])

    get_bin = lambda x, n: format(x, 'b').zfill(n)
    value_bin = get_bin(curr_state,prbs_len)[0:prbs_len]
    value_list = [int(i) for i in list(value_bin)]
    M = base_matrix_gen(prbs_expr[1],parallel_width)
    print(np.array(value_list))
    print(M)
    Nx = np.matmul(M,value_list)

    result_hex = bin2hex(np.mod(Nx,2),parallel_width)
    print(result_hex)
    return result_hex


if __name__ == '__main__':
    #base_matrix_gen(pseudo_predefine_dict['prbs_7'])
    #base_matrix_gen(pseudo_predefine_dict['prbs_23'])
    curr_state = 0x7f
    for l in range(1):
        next_state = prbs_next(curr_state,'prbs_7',80)
        curr_state = int(next_state[-1],16)&0x7f
    #prbs_next(0xff,'prbs_7')

