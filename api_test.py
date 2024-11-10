import time
length = 1000000
a = range(length, step=2)
b = range(1, length, step=2)
# print(a[0], a[1])
# print(b[0], b[1])


def time_check(func):
    def print_time():
        aa = time.time()
        func()
        nb = time.time()
        print("time : ", nb-aa)
    return print_time


@time_check
def test():
    for_big_calc_sum = 0
    for ii in range(len(a)):
        for j in range(len(b)):
            for_big_calc_sum += a[ii]*b[j]
    print(for_big_calc_sum)


if __name__ == "__main__":

    test_dict = dict()
    for i in range(int(length/2)):
        test_dict[a[i]] = b[i]
    # print(test_dict)
    # {0: 1, 2: 3, 4: 5, 6: 7, ..... 인 큰 딕셔너리 생성

    test_list = list()
    for i in range(int(length/2)):
        test_list.append(a[i])

        
    print("Dict")
    dict_start_time = time.time()
    counter = 0
    for i in range(int(length/2)):
        if i in test_dict:
            counter += 1

    dict_end_time = time.time()
    print("hit counter : ", counter, " time = ", dict_end_time - dict_start_time)

    print("List")
    list_start_time = time.time()
    counter = 0
    for i in range(int(length / 2)):
        if i in test_list:
            counter += 1

    list_end_time = time.time()
    print("hit counter : ", counter, " time = ", list_end_time - list_start_time)

