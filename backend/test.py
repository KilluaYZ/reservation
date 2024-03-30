# from pondmemory.database.Mongo import Mongo
# print(Mongo().insert_one("User", {"username": "killuayz", "password": "<PASSWORD>"}))
# Mongo().delete_many("User",{"username": "killuayz"})
# res = Mongo().find_one("User", {"username": "xinxin"})
# print(res)
# print(res["username"])
#

from pondmemory.utils.file import uploadFile
from bson import ObjectId
# fileId = ''
with open("C:\\Users\\killuayz\\Desktop\\微信图片_20240211233055.png", 'rb') as f:
    fileId = uploadFile(f.read(), "微信图片_20240211233055.png", ObjectId("65c9b8f4ffd0ded94ed6987a"),  False)

# import mimetypes
# print(mimetypes.guess_type('C:\\Users\\killuayz\\Desktop\\微信图片_20240211233055.png'))

# with open("./test1.png", "wb") as f:
#     res = getFileFromDB({"_id": ObjectId('65c9bb1b05195b1912e1c14b')})
#     if(res is not None):
#         f.write(res)

# from minio import Minio
# client = Minio(
#     "killuayz.top:9000",
#     access_key="eEn6r2cs1eyGFADxeJZE",
#     secret_key="T1WQGCEI9P1c0NC4KizNZF5PGWzVB2sq6vG6hiOa",
#     secure=False
# )
# import os
# print(client.list_buckets())
# file_stat = os.stat("C:\\Users\\killuayz\\Pictures\\Screenshots\\屏幕截图 2024-01-18 171646.png")
# with open("C:\\Users\\killuayz\\Pictures\\Screenshots\\屏幕截图 2024-01-18 171646.png", 'rb') as f:
#     client.put_object("pond-memory-bucket", 'pic1', f, file_stat.st_size)
#
# print(client.list_objects("pond-memory-bucket",recursive=True))