class NetworkException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

class EmailException(Exception):
    def __init__(self, msg):
        self.msg = msg