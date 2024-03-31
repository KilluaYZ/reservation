import request from "@/utils/request.js";

export function getVenueList(){
    const data = {

    }
    return request({
        url: 'task/get/venueList',
        method: 'post',
        data: data
    })
}

export function getRoomTypeList(){
    const data = {

    }
    return request({
        url: 'task/get/roomTypeList',
        method: 'post',
        data: data
    })
}

export function getOpenDateList(){
    const data = {

    }
    return request({
        url: 'task/get/openDateList',
        method: 'post',
        data: data
    })
}

export function getRoomList(venueId, roomTypeId, selectDate){
    const data = {
        venueId,
        roomTypeId,
        selectDate
    }
    return request({
        url: 'task/get/roomList',
        method: 'post',
        data: data
    })
}

export function addTask(form){
    const data = {
        time_start: form.time_start,
        time_end: form.time_end,
        onDate: form.onDate,
        length: form.length,
        favored_venue: form.favored_venue,
        room_type: form.room_type,
        interval_ms: form.interval_ms,
    }
    return request({
        url: 'task/add',
        method: 'post',
        data: data
    })
}

export function updateTask(form){
    const data = {
        task_id: form.task_id,
        time_start: form.time_start,
        time_end: form.time_end,
        onDate: form.onDate,
        length: form.length,
        favored_venue: form.favored_venue,
        room_type: form.room_type,
        interval_ms: form.interval_ms,
    }
    return request({
        url: 'task/update',
        method: 'post',
        data: data
    })
}

export function delTask(task_id){
    const data = {
        task_id: task_id
    }
    return request({
        url: 'task/del',
        method: 'post',
        data: data
    })
}

export function listTask(){
    const data = {
    }
    return request({
        url: 'task/list',
        method: 'post',
        data: data
    })
}


