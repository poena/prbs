def generate_prbs(pseudo_random_state, init_value=None, expression=None, length=10):

    if pseudo_random_state == 'user_define':
        pseudo_random_sequence = real_calculate_prbs(init_value, expression)
    else:
        pseudo_random_dict = {'prbs_7': ['1111111', [7, 6]],
                              'prbs_9': ['111110101', [9, 5]],
                              'prbs_15': ['111110101101110', [15, 14]],
                              'prbs_16': ['1111101011011100', [16, 12, 3, 1]],
                              'prbs_20': ['11111010110111001011', [20, 3]],
                              'prbs_21': ['111110101101110010111', [21, 2]],
                              #'prbs_23': ['11111010110111001011101', [23, 18]],
                              'prbs_23': ['01011010100001010100001', [23, 18]],
                              'prbs_31': ['1111111111110101110000000000000', [31, 28]]}
        pseudo_random_sequence = real_calculate_prbs(pseudo_random_dict[pseudo_random_state][0],
                                                     pseudo_random_dict[pseudo_random_state][1],
                                                     length)
    return pseudo_random_sequence

def real_calculate_prbs(value, expression, length):

    #
    value_list = [int(i) for i in list(value)]
    #
    #pseudo_random_length = (2 << (len(value) - 1))-1
    pseudo_random_length = length 
    print(pseudo_random_length)

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

if __name__ == '__main__':
    #result_data = generate_prbs('user_define', '1111', [4, 1])
    #result_data = generate_prbs('user_define', '1111111', [7, 3])
    #result_data = generate_prbs('prbs_31',length=80)
    result_data = generate_prbs('prbs_23',length=80)
    #result_data = generate_prbs('prbs_7',length=80)
    print(result_data)
    #print(result_data[0:40])

    '''
    result_data.reverse();
    #result_data = result_data+result_data
    for i in range(127):
        #print("Start %d:%d--%d."%(i,40*i%127,(40*i+40)%167))
        print(i)
        result_str = ''.join(str(e) for e in result_data[0:40])
        result_data = result_data[40:127]+result_data[0:40]
        #print result_data
        print(hex(int(result_str,2)))


    result_str = ''.join(str(e) for e in result_data[0:40])
    result_data = result_data[40:127]+result_data[0:40]
    print(hex(int(result_str,2)))
    '''
