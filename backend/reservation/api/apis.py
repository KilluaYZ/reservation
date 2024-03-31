from reservation.utils.request import *

def get_captcha():
    return get("https://zwlib.ruc.edu.cn/spa/static/public/api/createCaptcha")

def login(username: str, password: str, captchaId: str, captcha: str):
    return post("https://zwlib.ruc.edu.cn/spa/static/public/api/login", {
        "username": username,
        "password": password,
        "captchaId": captchaId,
        "captcha": captcha
    })

def get_venue_list(authorization: str):
    return get_with_auth("https://zwlib.ruc.edu.cn/spa/static/api/book/getVenueList", authorization)

def get_room_type_list(authorization: str):
    return get_with_auth("https://zwlib.ruc.edu.cn/spa/static/api/book/getRoomTypeList", authorization)

def get_open_date_list(authorization: str):
    return get_with_auth("https://zwlib.ruc.edu.cn/spa/static/api/book/getOpenDateList", authorization)


def get_room_list(venueId: str, roomTypeId: str, selectDate: str, authorization: str):
    request_data = {
        "venueId": venueId,
        "roomTypeId": roomTypeId,
        "pageSize": 6,
        "currentPage": 1,
        "selectDate": selectDate
    }
    tmp_resp = post_with_auth("https://zwlib.ruc.edu.cn/spa/static/api/book/getRoomList", authorization, request_data)
    totalCount = tmp_resp['totalCount']
    request_data["pageSize"] = totalCount
    return post_with_auth("https://zwlib.ruc.edu.cn/spa/static/api/book/getRoomList", authorization, request_data)

def get_room_detail(roomId: str, selectDate: str, authorization: str):
    request_data = {
        "roomId": roomId,
        "selectDate": selectDate,
        "seatNo": ""
    }
    return post_with_auth("tps://zwlib.ruc.edu.cn/spa/static/api/book/getRoomDtoByRoomIdAndDate", authorization, request_data)

def save_reservation(begin:int, end: int, onDate: str, phone: str, roomId: str, theme: str, useType: str, authorization: str):
    # request_data = {
    #     "begin": begin,
    #     "end": end,
    #     "onDate": onDate,
    #     "phone": phone,
    #     "roomId": roomId,
    #     "theme": theme,
    #     "useType": useType,
    #     "participants": "",
    #     "filePath": "",
    #     "source": "WEB",
    #     "seatNo": 0
    # }
    #
    # return post_with_auth("https://zwlib.ruc.edu.cn/spa/static/api/book/saveReservation",
    #                       authorization,
    #                       request_data)
    print(f"begin: {begin}, end: {end}, onDate: {onDate}, phone: {phone}, roomId: {roomId}, theme: {theme}, useType: {useType}, authorization: {authorization}")
    return {
        "status": True,
        "code": 200,
        "message": "预约成功",
        "data": ""
    }