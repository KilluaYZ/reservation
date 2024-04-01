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
from reservation.utils.LogToDB import *

bp = Blueprint('task', __name__, url_prefix='/task')
mongo = Mongo()

AvailableTimeStart = config.AvalibleTimeStart
AvailableTimeEnd = config.AvalibleTimeEnd
TaskThreadsMsgQueue = Queue()
TaskIdThreadMap = {}
AvailableVenueIdNameMap = {}
AvailableRoomTypeIdNameMap = {}

@bp.route('/add', methods=['POST'])
def add_task():
    try:
        user = check_user_before_request(request)

        time_start = request.json.get('time_start')
        time_end = request.json.get('time_end')
        on_date = request.json.get('on_date')
        length = request.json.get('length')
        favored_venue = request.json.get('favored_venue')
        room_type = request.json.get('room_type')
        interval_ms = request.json.get('interval_ms')

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

        task_id = request.json.get('task_id')
        time_start = request.json.get('time_start')
        time_end = request.json.get('time_end')
        on_date = request.json.get('on_date')
        length = request.json.get('length')
        favored_venue = request.json.get('favored_venue')
        interval_ms = request.json.get('interval_ms')
        room_type = request.json.get('room_type')

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
        task_id = request.json.get('task_id')

        checkFrontendArgsIsNotNone(
            [
                {"key": "task_id", "val": task_id},
            ]
        )
        mongo.delete_many('TaskLog', {"task_id": ObjectId(task_id)})
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
        rows = mongo.find('Task', {"user_id": user['_id']}).sort("update_time", -1)
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
    if start_time + res_length >= AvailableTimeEnd:
        res_length = AvailableTimeEnd - start_time
    return res_length

def task_to_string(task: dict, user: dict) -> str:
    return f'''任务参数：
    任务ID(_id):{task['_id']}
    预约日期(on_date):{task["on_date"]}
    最早开始时间(time_start):{task["time_start"]}
    最晚开始时间(time_end){task["time_end"]}
    最短使用时长(length):{task["length"]}
    教学楼优先级(favored_venue):{[(AvailableVenueIdNameMap[x], x) for x in task["favored_venue"]]}
    静音仓类型(room_type):{(AvailableRoomTypeIdNameMap[task['room_type']], task['room_type'])}
    间隔时间(interval_ms):{task["interval_ms"]}

    学号：{user['userInfo']['username']}
    姓名：{user['userInfo']['fullName']}
    学院：{user['userInfo']['department']}
    注册邮箱：{user['email']}
    手机号码：{user['phone']}
    Authorization: {user['authorization']}
'''

def room_to_string(room) -> str:
    return f"""静音仓信息：
    静音仓id(id):{room['id']}
    静音仓名称(name):{room['name']}
    教学楼(venue):{(AvailableVenueIdNameMap[room['venue']], room['venue'])}
    地点(address):{room['address']}
    楼层(floor):{room['floor']}
    已被占用时段:{[(time_num_to_str(x[0]), time_num_to_str(x[1])) for x in room['roomTimeSliceDto']['disableTime']]}
    """

def process_single_task_thread(task: dict, user: dict, max_retry_times=3):
    try:
        try_time = 1
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
        logToDB(task['_id'], 'INFO', '任务初始化....')
        logToDB(task['_id'], 'INFO',task_to_string(task, user))
        request_cnt = 0
        # 开始请求
        while(True):
            # 先检查当前时间有没有超过预约时间或者7:00到22:00的限制
            current_time = datetime.datetime.now()
            # print(f"current = {current_time.hour*60+current_time.minute} start = {AvailableTimeStart} end = {AvailableTimeEnd}")
            if current_time.hour*60+current_time.minute < AvailableTimeStart or current_time.hour*60+current_time.minute >= AvailableTimeEnd:
                send_msg = f"您启动的任务超过时间限制(7:00-22:00)，本次预约任务已结束...\n{task_to_string(task, user)}"
                logToDB(task['_id'], 'ERROR', send_msg)
                raise EmailException(send_msg)

            time_end_datetime = datetime.datetime.strptime(f"{on_date} {time_end}", "%Y-%m-%d %H:%M")
            if current_time >= time_end_datetime:
                send_msg = f"无法在您设置的时段({time_start} -- {time_end})内完成预约，本次预约任务已结束...\n{task_to_string(task, user)}"
                logToDB(task['_id'], 'ERROR', send_msg)
                raise EmailException(send_msg)

            request_cnt += 1
            logToDB(task['_id'], 'INFO', f"开始第{request_cnt}次请求...")
            # 按照优先次序，依次查找不同区域的座位情况
            res_room = None
            res_start_time = None
            for (venue_idx, venue) in enumerate(favored_venue):
                resp = apis.get_room_list(venue, room_type, on_date, authorization)['data']
                room_list = resp['pageList']
                for room in room_list:
                    roomTimeSliceDto = room['roomTimeSliceDto']
                    disableTime = roomTimeSliceDto['disableTime']
                    for i in range(time_str_to_num(time_start), time_str_to_num(time_end), 30):
                        if(check_if_avaliable(i, i + length + 1, disableTime)):
                            res_room = room
                            res_start_time = i
                            break
                    if res_room is not None:
                        break

                if res_room is not None:
                    logToDB(task['_id'], 'INFO', f"找到了符合要求的静音仓！\n{room_to_string(res_room)}")

                    # 找到了符合要求的时间段
                    if(venue_idx != 0):
                        # 如果当前的room并不是最理想的room, 则再去看一眼排序在前的room是否有空的
                        logToDB(task['_id'], 'INFO', f"当前静音仓不是条件最优的静音仓，开始寻找条件更优的静音仓是否空闲...")
                        better_venue_res_room = None
                        better_venue_res_start_time = None
                        for better_venue_i in range(venue_idx):
                            better_venue_resp = apis.get_room_list(favored_venue[better_venue_i], room_type, on_date, authorization)['data']
                            better_venue_room_list = better_venue_resp['pageList']
                            for better_venue_room in better_venue_room_list:
                                better_venue_roomTimeSliceDto = better_venue_room['roomTimeSliceDto']
                                better_venue_disableTime = better_venue_roomTimeSliceDto['disableTime']
                                for i in range(time_str_to_num(time_start), time_str_to_num(time_end), 30):
                                    if (check_if_avaliable(i, i + length + 1, better_venue_disableTime)):
                                        better_venue_res_room = better_venue_room
                                        better_venue_res_start_time = i
                                        break
                                if better_venue_res_room is not None:
                                    break
                            if better_venue_res_room is not None:
                                res_room = better_venue_res_room
                                res_start_time = better_venue_res_start_time
                                logToDB(task['_id'], 'INFO', f'找到了条件更优的静音仓！\n{room_to_string(res_room)}')
                                break
                    break

            if res_room is None:
                sleep_time = float(interval_ms) / 2 * (random.random() - 0.5) + float(interval_ms)
                logToDB(task['_id'], 'INFO', f'未找到适合的静音仓，等待{int(sleep_time)}ms后继续查找')
                try_time = 0
                time.sleep(sleep_time/1000)
                continue

            logToDB(task['_id'], 'INFO', f'决定预约的静音仓为\n{room_to_string(res_room)}')
            logToDB(task['_id'], 'INFO', f'开始尝试第{try_time}/{max_retry_times}次预约')
            try_time += 1
            # 找到了最好的符合要求的房间，接下来将要找到最长的可用时间
            max_length = get_max_length(res_start_time, res_room['roomTimeSliceDto']['disableTime'], length)
            begin = res_start_time
            end = res_start_time + max_length
            onDate = on_date
            phone = user['phone']
            roomId = res_room['id']
            theme = '面试'
            useType = room_type
            authorization = user['authorization']
            reservation_resp = apis.save_reservation(begin, end, onDate, phone, roomId, theme, useType, authorization)
            print(f"[DEBUG] begin = {begin} end = {end}")
            if reservation_resp is not None and reservation_resp['code'] == 200:
                # 预约成功，向用户发送邮件提醒
                send_msg = f"您设置的预约任务执行完成！\n预约信息如下：\n\t名称:{res_room['name']}\n\t开始时间:{onDate} {time_num_to_str(begin)} \n\t结束时间:{onDate} {time_num_to_str(end)}\n\t地点:{res_room['address']}\n静音仓信息如下：\n{room_to_string(res_room)}\n任务配置参数如下：\n{task_to_string(task, user)}"
                logToDB(task['_id'], 'INFO', send_msg)
                raise EmailException(send_msg)
            else:
                # 预约失败，重试
                logToDB(task['_id'], 'ERROR', f'第{try_time}/{max_retry_times}次尝试预约失败')
                if try_time <= max_retry_times:
                    logToDB(task['_id'], 'ERROR', f'重新尝试预约')
                    continue
                # 预约失败，向用户发送邮件提醒
                send_msg = f"您设置的预约任务执行失败！ {max_retry_times}次预约尝试均失败，请检查设置或联系管理员\n预约信息如下：\n\t名称:{res_room['name']}\n\t开始时间:{onDate} {time_num_to_str(begin)} \n\t结束时间:{onDate} {time_num_to_str(end)}\n\t地点:{res_room['address']}\n静音仓信息如下：\n{room_to_string(res_room)}\n任务配置参数如下：\n{task_to_string(task, user)}"
                logToDB(task['_id'], 'ERROR', send_msg)
                raise EmailException(send_msg)


    except EmailException as e:
        sendTextEmail(e.msg, user['email'])
    except NetworkException as e:
        raise e
    except Exception as e:
        send_msg = f"您设置的预约任务由于服务端内部错误执行失败！\n{task_to_string(task, user)}\n错误信息:{e}\n详情请登录平台查看任务日志"
        logToDB(task['_id'], 'ERROR', send_msg)
        sendTextEmail(send_msg, user['email'])
        raise e
    finally:
        mongo.update_one('Task', {'_id': task['_id']}, {'$set':{'status': 'stop'}})
        logToDB(task['_id'], 'INFO', '任务结束，正在退出...')

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
        task_id = request.json.get('task_id')
        checkFrontendArgsIsNotNone(
            [
                {"key": "task_id", "val": task_id},
            ]
        )
        user = check_user_before_request(request)
        task = mongo.find_one('Task', {'_id': ObjectId(task_id), "user_id": user['_id']})
        if task is None:
            raise NetworkException(400, f'未找到id为{task_id}的任务')

        logToDB(task['_id'], 'INFO', '正在停止任务')
        if task_id not in TaskIdThreadMap:
            mongo.update_one('Task', {'_id': ObjectId(task_id), 'user_id': user['_id']}, {'$set': {'status': 'stop'}})
            logToDB(task['_id'], 'INFO', '任务停止出错，任务没有在运行\n')
            raise NetworkException(400, f"无法找到任务id为{task_id}的正在运行中的线程")

        task_thread = TaskIdThreadMap[task_id]
        _async_raise(task_thread.ident, SystemExit)
        logToDB(task['_id'], 'INFO', '任务已停止')
        mongo.update_one('Task', {'_id': task['_id']}, {'$set':{'status': 'stop'}})
        return build_success_response()

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        logger.logger.error(e)
        return build_error_response(code=500, msg='服务器内部错误')


@bp.route('/start', methods=['POST'])
def start_task():
    try:
        task_id = request.json.get('task_id')
        checkFrontendArgsIsNotNone(
            [
                {"key": "task_id", "val": task_id},
            ]
        )
        user = check_user_before_request(request)
        task = mongo.find_one('Task', {'_id': ObjectId(task_id), "user_id": user['_id']})
        if task is None:
            raise NetworkException(400, f'未找到id为{task_id}的任务')
        venues = apis.get_venue_list(user['authorization'])['data']
        for venue in venues:
            AvailableVenueIdNameMap[venue['id']] = venue['name']
        room_types = apis.get_room_type_list(user['authorization'])['data']
        for room_type in room_types:
            AvailableRoomTypeIdNameMap[room_type['id']] = room_type['name']
        logToDB(task['_id'], 'INFO', '正在启动任务')
        task_thread = threading.Thread(target=process_single_task_thread, args=(task, user, 3))
        task_thread.start()
        TaskIdThreadMap[task_id] = task_thread
        logToDB(task['_id'], 'INFO', '任务已启动')
        mongo.update_one('Task', {'_id': task['_id']}, {'$set':{'status': 'running'}})
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
        venueId = request.json.get('venueId')
        roomTypeId = request.json.get('roomTypeId')
        selectDate = request.json.get('selectDate')

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

@bp.route('/log/json', methods=['POST'])
def get_task_json_log():
    try:
        task_id = request.json.get('task_id')
        checkFrontendArgsIsNotNone(
            [
                {"key": "task_id", "val": task_id},
            ]
        )

        user = check_user_before_request(request)
        task = mongo.find_one('Task', {'_id': ObjectId(task_id), "user_id": user['_id']})
        if task is None:
            raise NetworkException(400, f'该用户没有id为{task_id}的任务')
        logs = getLogByTaskId(ObjectId(task_id))
        return build_success_response(logs)

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        logger.logger.error(e)
        return build_error_response(code=500, msg='服务器内部错误')

@bp.route('/log/text', methods=['POST'])
def get_task_text_log():
    try:
        task_id = request.json.get('task_id')
        checkFrontendArgsIsNotNone(
            [
                {"key": "task_id", "val": task_id},
            ]
        )

        user = check_user_before_request(request)
        task = mongo.find_one('Task', {'_id': ObjectId(task_id), "user_id": user['_id']})
        if task is None:
            raise NetworkException(400, f'该用户没有id为{task_id}的任务')
        logs = getLogByTaskId(ObjectId(task_id))
        res = []
        for item in logs:
            res.append(f"[{item['type']}] {item['create_time']} - {item['msg']}")
        return build_success_response(res)

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        logger.logger.error(e)
        return build_error_response(code=500, msg='服务器内部错误')

