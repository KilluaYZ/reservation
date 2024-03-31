import datetime
# time_str = '9:00'
# tmp_time = datetime.datetime.strptime(time_str, '%H:%M')
# print(tmp_time.hour, tmp_time.minute)
# print(tmp_time.hour * 60 + tmp_time.minute)


# def time_num_to_str(time_num: int) -> str:
#     tmp_time = datetime.datetime(2020, 1, 1, int(time_num/60), int(time_num%60))
#     return tmp_time.strftime('%H:%M')
#
# print(time_num_to_str(540))


def check_if_avaliable(start_time: int, end_time: int, disable_time: list) -> bool:
    tmp_disabled_list = []
    # 如果结束时间早于开始时间，则排除
    for _time in disable_time:
        if _time[1] <= start_time:
            continue
        else:
            tmp_disabled_list.append(_time)
    tmp_distable_list2 = []
    # 如果开始时间晚于结束时间，则排除
    for _time in tmp_disabled_list:
        if _time[0] >= end_time:
            continue
        else:
            tmp_distable_list2.append(_time)

    if len(tmp_distable_list2) == 0:
        # 如果列表为空，说明没有冲突的，则可以分配
        return True
    # 反之则无法分配
    return False

# print(check_if_avaliable(721, 1111, [
#     [510,  720],
#     [870, 1110],
#     [1140, 1320]
# ]))

for i in range(0,10,2):
    print(i)