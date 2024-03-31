from reservation.utils.Tools import *
from reservation.utils.build_response import *
from flask import Blueprint, request
import datetime
from reservation.database.Mongo import Mongo
from reservation.utils.Logger import logger
from bson.objectid import ObjectId
import config
from queue import Queue
import time
from reservation.utils.myExceptions import *
from reservation.email_sender.send_my_email import sendTextEmail
import threading
import inspect
import ctypes
import reservation.api.apis as apis

bp = Blueprint('task', __name__, url_prefix='/task')
mongo = Mongo()

AvalibleTimeStart = config.AvalibleTimeStart
AvalibleTimeEnd = config.AvalibleTimeStart
TaskThreadsMsgQueue = Queue()
TaskIdThreadMap = {}
@bp.route('/add', methods=['POST'])
def add_task():
    try:
        user = check_user_before_request(request)

        time_start = request.json['time_start']
        time_end = request.json['time_end']
        on_date = request.json['onDate']
        length = request.json['length']
        favored_venue = request.json['favored_venue']
        room_type = request.json['room_type']
        interval_ms = request.json['interval_ms']

        checkFrontendArgsIsNotNone(
            [
                {"key": "time_start", "val": time_start},
                {"key": "time_end", "val": time_end},
                {"key": "on_date", "val": on_date},
                {"key": "length", "val": length},
                {"key": "favored_venue", "val": favored_venue},
                {"key": "interval_ms", "val": interval_ms},
                {"key": "room_type", "val": room_type},
            ]
        )

        mongo.insert_one('Task',{
            "user_id": user['_id'],
            "time_start": time_start,
            "time_end":time_end,
            "on_date":on_date,
            "length":length,
            "favored_venue": favored_venue,
            "room_type": room_type,
            "status": 'stop',
            "create_time": datetime.datetime.now(),
            "update_time": datetime.datetime.now(),
            "interval_ms": interval_ms
        })

        return build_success_response()

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        logger.logger.error(e)
        return build_error_response(code=500, msg='服务器内部错误')


@bp.route('/update', methods=['POST'])
def update_task():
    try:
        user = check_user_before_request(request)

        task_id = request.form['task_id']
        time_start = request.json['time_start']
        time_end = request.json['time_end']
        on_date = request.json['onDate']
        length = request.json['length']
        favored_venue = request.json['favored_venue']
        interval_ms = request.json['interval_ms']
        room_type = request.json['room_type']

        checkFrontendArgsIsNotNone(
            [
                {"key": "time_start", "val": time_start},
                {"key": "task_id", "val": task_id},
                {"key": "time_end", "val": time_end},
                {"key": "on_date", "val": on_date},
                {"key": "length", "val": length},
                {"key": "favored_venue", "val": favored_venue},
                {"key": "interval_ms", "val": interval_ms},
                {"key": "room_type", "val": room_type},
            ]
        )

        mongo.update_one('Task',
     {"_id": ObjectId(task_id), "user_id": user['_id']},
     {"$set":{
                "time_start": time_start,
                "time_end": time_end,
                "on_date": on_date,
                "length": length,
                "favored_venue": favored_venue,
                "update_time": datetime.datetime.now(),
                "interval_ms": interval_ms,
                "room_type": room_type
     }})

        return build_success_response()

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        logger.logger.error(e)
        return build_error_response(code=500, msg='服务器内部错误')

@bp.route('/del', methods=['POST'])
def del_task():
    try:
        user = check_user_before_request(request)
        task_id = request.json['task_id']

        checkFrontendArgsIsNotNone(
            [
                {"key": "task_id", "val": task_id},
            ]
        )

        mongo.delete_one('Task', {"_id": ObjectId(task_id), "user_id": user['_id']})

        return build_success_response()

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        logger.logger.error(e)
        return build_error_response(code=500, msg='服务器内部错误')


@bp.route('/list', methods=['POST'])
def list_task():
    try:
        user = check_user_before_request(request)
        rows = mongo.find('Task', {"user_id": user['_id']})
        return build_success_response(list(rows))

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        logger.logger.error(e)
        return build_error_response(code=500, msg='服务器内部错误')


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

def get_max_length(start_time: int, disable_time: list, min_length=30, max_length=240) -> int:
    res_length = min_length
    for l in range(min_length, max_length+1, 30):
        if check_if_avaliable(start_time, start_time+l, disable_time):
            res_length = l
        else:
            break
    return res_length

def process_single_task_thread(task: dict, user: dict, max_retry_times=3):
    try:
        try_time = 0
        # 任务初始化，写入到日志
        mongo.update_one('Task', {"_id": task['_id']}, {"$set": {"status": "running"}})
        interval_ms = task["interval_ms"]
        on_date = task["on_date"]
        time_start = task["time_start"]
        time_end = task["time_end"]
        authorization = user['authorization']
        length = task["length"]
        favored_venue = task["favored_venue"]
        room_type = task['room_type']
        # 开始请求
        while(True):
            # 先检查当前时间有没有超过预约时间或者7:00到22:00的限制
            current_time = datetime.datetime.now()
            if current_time.hour*60+current_time.minute < AvalibleTimeStart or current_time.hour*60+current_time.minute >= AvalibleTimeEnd:
                raise EmailException("超过时间限制(7:00-22:00)，本次预约任务已结束...")

            time_end_datetime = datetime.datetime.strptime(f"{current_time.year}-{on_date} {time_num_to_str(time_start)}", "%Y-%m-%d %H:%M")
            if current_time >= time_end_datetime:
                raise EmailException(f"无法在您设置的时段({time_num_to_str(time_start)} -- {time_num_to_str(time_end)})内完成预约，本次预约任务已结束...")

            # 按照优先次序，依次查找不同区域的座位情况
            res_room = None
            res_start_time = None
            for (venue_idx, venue) in enumerate(favored_venue):
                resp = apis.get_room_list(venue, room_type, on_date, authorization)
                room_list = resp['pageList']
                for room in room_list:
                    roomTimeSliceDto = room['roomTimeSliceDte']
                    disableTime = roomTimeSliceDto['disableTime']
                    for i in range(time_start, time_end, 30):
                        if(check_if_avaliable(i, i + length + 1, disableTime)):
                            res_room = room
                            res_start_time = i
                            break
                    if res_room is not None:
                        break

                # 找到了符合要求的时间段
                if(venue_idx != 0):
                    # 如果当前的room并不是最理想的room, 则再去看一眼排序在前的room是否有空的
                    better_venue_res_room = None
                    better_venue_res_start_time = None
                    for better_venue_i in range(venue_idx):
                        better_venue_resp = apis.get_room_list(favored_venue[better_venue_i], room_type, on_date, authorization)
                        better_venue_room_list = better_venue_resp['pageList']
                        for better_venue_room in better_venue_room_list:
                            better_venue_roomTimeSliceDto = better_venue_room['roomTimeSliceDte']
                            better_venue_disableTime = better_venue_roomTimeSliceDto['disableTime']
                            for i in range(time_start, time_end, 30):
                                if (check_if_avaliable(i, i + length + 1, better_venue_disableTime)):
                                    better_venue_res_room = better_venue_room
                                    better_venue_res_start_time = i
                                    break
                            if better_venue_res_room is not None:
                                break
                        if better_venue_res_room is not None:
                            res_room = better_venue_res_room
                            res_start_time = better_venue_res_start_time
                            break

                if res_room is not None:
                    break

            if res_room is None:
                time.sleep(float(interval_ms)/1000)
                continue

            try_time += 1
            # 找到了最好的符合要求的房间，接下来将要找到最长的可用时间
            max_length = get_max_length(res_start_time, res_room['roomTimeSliceDte']['disableTime'], length)
            begin = res_start_time
            end = res_start_time + max_length
            onDate = on_date
            phone = user['phone']
            roomId = res_room['id']
            theme = '面试'
            useType = room_type
            authorization = user['authorization']
            reservation_resp = apis.save_reservation(begin, end, onDate, phone, roomId, theme, useType, authorization)
            if reservation_resp is not None and reservation_resp['status']:
                # 预约成功，向用户发送邮件提醒
                raise EmailException(f"您设置的预约任务执行完成！\n静音仓信息如下：\n\t名称:{res_room['name']}\n\t开始时间:{onDate} {time_num_to_str(begin)} \n\t结束时间:{onDate} {time_num_to_str(end)}\n\t地点:{res_room['address']}")
            else:
                # 预约失败，重试
                if try_time <= max_retry_times:
                    continue
                # 预约失败，向用户发送邮件提醒
                raise EmailException(f"您设置的预约任务执行失败！ {max_retry_times}次预约尝试均失败，请检查设置或联系管理员")

    except EmailException as e:
        sendTextEmail(e.msg, user['email'])
    except NetworkException as e:
        raise e
    except Exception as e:
        raise e

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


@bp.route('/stop', methods=['POST'])
def stop_task():
    try:
        user = check_user_before_request(request)
        task_id = request.json['task_id']
        task = mongo.find_one('Task', {'_id': ObjectId(task_id), "user_id": user['_id']})
        if task is None:
            raise NetworkException(400, f'未找到id为{task_id}的任务')

        task_thread = TaskIdThreadMap[task_id]
        if task_thread is None:
            mongo.update_one('Task', {'_id': ObjectId(task_id), 'user_id': user['_id']}, {'$set': {'status': 'stop'}})
            raise NetworkException(400, f"无法找到任务id为{task_id}的正在运行中的线程")

        _async_raise(task_thread.ident, SystemExit)
        return build_success_response()

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        logger.logger.error(e)
        return build_error_response(code=500, msg='服务器内部错误')


@bp.route('/start', methods=['POST'])
def start_task():
    try:
        user = check_user_before_request(request)
        task_id = request.json['task_id']
        task = mongo.find_one('Task', {'_id': ObjectId(task_id), "user_id": user['_id']})
        if task is None:
            raise NetworkException(400, f'未找到id为{task_id}的任务')
        task_thread = threading.Thread(target=process_single_task_thread, args=(task, user, 3))
        task_thread.start()
        TaskIdThreadMap[task_id] = task_thread
        return build_success_response()

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        logger.logger.error(e)
        return build_error_response(code=500, msg='服务器内部错误')

@bp.route('/get/venueList', methods=['POST'])
def get_venue_list_api():
    try:
        user = check_user_before_request(request)
        authorization = user['authorization']
        resp = apis.get_venue_list(authorization)
        if resp['code'] != 200:
            raise NetworkException(400, f"获取教学楼列表出错，{resp['message']}")

        return build_success_response(resp['data'])

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        logger.logger.error(e)
        return build_error_response(code=500, msg='服务器内部错误')


@bp.route('/get/roomTypeList', methods=['POST'])
def get_room_type_list_api():
    try:
        user = check_user_before_request(request)
        authorization = user['authorization']
        resp = apis.get_room_type_list(authorization)
        if resp['code'] != 200:
            raise NetworkException(400, f"获取静音仓类型列表出错，{resp['message']}")

        return build_success_response(resp['data'])

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        logger.logger.error(e)
        return build_error_response(code=500, msg='服务器内部错误')

@bp.route('/get/openDateList', methods=['POST'])
def get_open_date_list_api():
    try:
        user = check_user_before_request(request)
        authorization = user['authorization']
        resp = apis.get_open_date_list(authorization)
        if resp['code'] != 200:
            raise NetworkException(400, f"获取开放预约时间列表出错，{resp['message']}")

        return build_success_response(resp['data'])

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        logger.logger.error(e)
        return build_error_response(code=500, msg='服务器内部错误')


@bp.route('/get/roomList', methods=['POST'])
def get_room_list_api():
    try:
        venueId = request.json['venueId']
        roomTypeId = request.json['roomTypeId']
        selectDate = request.json['selectDate']

        checkFrontendArgsIsNotNone(
            [
                {"key": "venueId", "val": venueId},
                {"key": "roomTypeId", "val": roomTypeId},
                {"key": "selectDate", "val": selectDate},
            ]
        )

        user = check_user_before_request(request)
        authorization = user['authorization']

        resp = apis.get_room_list(venueId,roomTypeId,selectDate,authorization)
        if resp['code'] != 200:
            raise NetworkException(400, f"获取开放预约时间列表出错，{resp['message']}")

        return build_success_response(resp['data'])

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        logger.logger.error(e)
        return build_error_response(code=500, msg='服务器内部错误')