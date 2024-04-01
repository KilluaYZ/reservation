from reservation.database.Mongo import Mongo
import datetime
from bson import ObjectId

mongo = Mongo()

def logToDB(task_id:ObjectId, type: str, msg: str):
    mongo.insert_one('TaskLog', {"task_id": task_id, "type": type, "msg": msg, "create_time": datetime.datetime.now()})

def getLogByTaskId(task_id:ObjectId) -> list:
    return list(mongo.find("TaskLog", {"task_id": task_id}).sort("create_time"))
