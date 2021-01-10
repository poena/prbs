#!/user/bin/python
import sys, getopt

def generate_prbs(pseudo_random_state, init_value=None, expression=None, length=10):

    if pseudo_random_state == 'user_define':
        pseudo_random_sequence = real_calculate_prbs(init_value, expression)
    else:
        pseudo_random_dict = {'prbs_7': [0xff, [7, 6]],
                              'prbs_9': [0x1f5, [9, 5]],
                              'prbs_15': [0x7d6e, [15, 14]],
                              'prbs_23': [0x7d6e5d, [23, 18]],
                              'prbs_31': [0x7ffae000, [31, 28]]}
        pseudo_random_sequence = real_calculate_prbs(pseudo_random_dict[pseudo_random_state][0],
                                                     pseudo_random_dict[pseudo_random_state][1],
                                                     length)
    return pseudo_random_sequence

def real_calculate_prbs(value, expression, length):

    #
    get_bin = lambda x, n: format(x, 'b').zfill(n)
    prbs_len = expression[0]
    value_bin = get_bin(value,prbs_len)[0:prbs_len]
    value_list = [int(i) for i in list(value_bin)]
    #print(value_list)
    #
    #pseudo_random_length = (2 << (len(value) - 1))-1
    pseudo_random_length = length 
    #print(pseudo_random_length)

    sequence = []

    #
    for i in range(pseudo_random_length):

        mod_two_add = sum([value_list[t-1] for t in expression])
        xor = mod_two_add % 2

        #
        value_list.insert(0, xor)

        sequence.append(value_list[-1])
        del value_list[-1]

    return sequence

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

def prbs_gen(prbs_mode,prbs_len,prbs_width):
    #result_data = generate_prbs('user_define', '1111', [4, 1])
    #result_data = generate_prbs('user_define', '1111111', [7, 3])
    #result_data = generate_prbs('prbs_31',length=80)
    #result_data = generate_prbs('prbs_23',length=80)

    result_data = generate_prbs(prbs_mode,length=prbs_len)
    result_hex = bin2hex(result_data,prbs_width)
    print(result_hex)
    #print(result_data[0:40])

def cmd_help():
    print("prbs.py --mode='prbs_7' --length=80 --width=32")

def main(argv):
    prbs_mode = 'prbs_7'
    prbs_len = 80
    prbs_width = 32
    try:
        opts, args = getopt.getopt(argv,"hl:m:w:",["length=","mode=","width="])
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
        elif opt in ("-w","--width"):
            prbs_width = int(arg)

    print(prbs_len)
    prbs_gen(prbs_mode,prbs_len,prbs_width)

if __name__ == '__main__':
    main(sys.argv[1:])
