#coding=utf-8

class BaseResponse:

    def __init__(self):
        self.status = False
        self.data = None
        self.summary = None
        self.message = {}

