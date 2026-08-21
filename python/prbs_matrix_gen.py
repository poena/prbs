#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : prbs_matrix_gen.py
# Author            : Changsong Li <poena@163.com>
# Date              : 02.12.2020
# Last Modified Date: 02.12.2020
# Last Modified By  : Changsong Li <poena@163.com>
import sys, getopt
import numpy as np

np.set_printoptions(threshold=np.inf)

pseudo_predefine_dict = {'prbs_7': [0x7f, [7, 6]],
                         'prbs_9': [0x1ff, [9, 5]],
                         'prbs_15': [0x7fff, [15, 14]],
                         'prbs_23': [0x7fffff, [23, 18]],
                         'prbs_31': [0x7fffffff, [31, 28]]}

def add_prbs_mode(prbs_seed,prbs_expr):
    if(prbs_seed == None): 
        pseudo_predefine_dict['user_define'] = [0x1, prbs_expr]
    else:
        pseudo_predefine_dict['user_define'] = [prbs_seed, prbs_expr]

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

def companion_matrix(prbs_type,lfsr_type='fibonacci'):
    """One-step GF(2) state transition matrix, MSB-first state vector."""
    prbs_size = prbs_type[0]

    if lfsr_type == 'galois':
        # Right shift; the bit shifted out toggles every tap position,
        # including the degree term feeding back into the top bit.
        A = np.eye(prbs_size,k=-1,dtype='int')
        for x in prbs_type:
            A[prbs_size-x,-1] ^= 1
    else:
        # Left shift; XOR of the tapped bits feeds back into the bottom bit.
        A = np.eye(prbs_size,k=1,dtype='int')
        for x in prbs_type:
            A[-1,prbs_size-x] = 1

    return A

def base_matrix_gen(prbs_type,parallel_width,lfsr_type='fibonacci'):

    #print(prbs_type)
    prbs_size = prbs_type[0]

    para_grp = (parallel_width+prbs_size-1)//prbs_size

    #print(prbs_size)

    MM = np.zeros([para_grp*prbs_size,prbs_size],dtype='int')
    A = companion_matrix(prbs_type,lfsr_type)

    #print(A)
    #M[0:prbs_size,:] = A;
    #M = A;
    for j in range(para_grp):
        for i in range(prbs_size):
            if(i==0 and j==0):
                print("init")
                M = A
            else:
                M = np.matmul(M,A)
                M = np.mod(M,2)
        #print(M)
        MM[j*prbs_size:(j+1)*prbs_size] = M

    #MM = M
    #for i in range(prbs_size):
    #    M = np.matmul(M,A)
    #    M = np.mod(M,2)
    #print(M)

    return MM[0:parallel_width,:]

def get_base_matrix(prbs_mode,parallel_width,lfsr_type='fibonacci'):
    prbs_expr = pseudo_predefine_dict[prbs_mode]
    prbs_type = prbs_expr[1]
    M = base_matrix_gen(prbs_type,parallel_width,lfsr_type)
    return M

def prbs_next(curr_state,prbs_mode,parallel_width,lfsr_type='fibonacci'):
    prbs_expr = pseudo_predefine_dict[prbs_mode]
    prbs_len = prbs_expr[1][0]
    print(['prbs_len:',prbs_len])

    get_bin = lambda x, n: format(x, 'b').zfill(n)
    value_bin = get_bin(curr_state,prbs_len)[0:prbs_len]
    value_list = [int(i) for i in list(value_bin)]
    M = base_matrix_gen(prbs_expr[1],parallel_width,lfsr_type)
    print(np.array(value_list))
    print(M)
    Nx = np.matmul(M,value_list)

    result_hex = bin2hex(np.mod(Nx,2),parallel_width)
    print(result_hex)
    return result_hex

def prbs_gen(prbs_mode,prbs_len,init_value,prbs_width,lfsr_type='fibonacci'):
    if(init_value == None):
        curr_state = pseudo_predefine_dict[prbs_mode][0]
    else:
        curr_state = init_value
    print(curr_state)
    for l in range(1):
        next_state = prbs_next(curr_state,prbs_mode,prbs_width,lfsr_type)
        curr_state = int(next_state[-1],16)&0x7fffffff
    #prbs_next(0xff,'prbs_7')

def cmd_help():
    print('For pre define mode:')
    print("  prbs_matrix_gen.py --mode='prbs_7' --length=80 --width=32")
    print('For user_define mode:')
    print("  prbs_matrix_gen.py --mode='user_define' --expression='[23,21,16,8,5,2]' --length=80 --width=64 --seed=0x1dbfbc")
    print('For galois LFSR structure (default is fibonacci):')
    print("  prbs_matrix_gen.py --mode='prbs_7' --length=80 --width=32 --type='galois'")

def main(argv):
    prbs_mode = 'prbs_7'
    prbs_len = 160
    prbs_width = 32
    prbs_seed = None
    prbs_expr = None
    lfsr_type = 'fibonacci'
    try:
        opts, args = getopt.getopt(argv,"hl:m:e:w:s:t:",["length=","mode=","expression=","width=","seed=","type="])
    except getopt.GetoptError:
        cmd_help()
    for opt, arg in opts:
        if opt == '-h':
            cmd_help()
            sys.exit()
        elif opt in ("-l","--length"):
            prbs_len = int(arg)
        elif opt in ("-m","--mode"):
            prbs_mode = arg
        elif opt in ("-e","--expression"):
            prbs_expr = eval(arg)
        elif opt in ("-w","--width"):
            prbs_width = int(arg)
        elif opt in ("-s","--seed"):
            prbs_seed = int(arg,16)
        elif opt in ("-t","--type"):
            lfsr_type = arg
            if lfsr_type not in ('fibonacci','galois'):
                print(f"unknown lfsr type: {lfsr_type}, expect 'fibonacci' or 'galois'")
                sys.exit(1)

    if(prbs_mode == 'user_define'):
        add_prbs_mode(prbs_seed,prbs_expr)

    #print([prbs_mode,prbs_len,prbs_width,prbs_seed])
    print(f"run in mode: {prbs_mode}, length : {prbs_len}, width: {prbs_width}, expression: {prbs_expr}, lfsr: {lfsr_type}")
    prbs_gen(prbs_mode,prbs_len,prbs_seed,prbs_width,lfsr_type)

if __name__ == '__main__':
    main(sys.argv[1:])
