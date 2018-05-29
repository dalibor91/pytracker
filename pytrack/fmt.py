

print_outlinte = True


def __pad_arr(arr, padding):
    data = []
    for r in arr:
        data.append(len(str(r))+padding)
    return data


def __find_pad(arr, padding):
    data = []
    for row in arr:
        if len(data) == 0:
            data = __pad_arr(row, padding)
        else:
            tmp_data = __pad_arr(row, padding)
            for tmp_k, tmp_v in enumerate(tmp_data):
                if data[tmp_k] < tmp_v:
                    data[tmp_k] = tmp_v

    return data


def print_formated(arr, header=None, padding=0):
    if header is not None:
        new_arr = [ header ]
        for row in arr:
            new_arr.append(row)
        arr = new_arr

    pading = __find_pad(arr, padding)

    for key, val in enumerate(arr):
        if not print_outlinte and key == 0 and header is not None:
            continue
        str = ""
        for key1, val1 in enumerate(val):
            pad = pading[key1]
            str += ("%s" % val1).ljust(pad) + (" | " if print_outlinte else " ")

        if (key == 0) and (header is not None) and print_outlinte:
            summed = 0
            for r in pading:
                summed += r+4
            summed-=1
            print(summed*'-')
            print(str)
            print(summed*'-')
        else:
            print(str)
