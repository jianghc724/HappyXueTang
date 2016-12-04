from codex.baseerror import *
from codex.baseview import APIView

import requests
import json

from wechat.models import User
from HappyXueTang.settings import API_KEY, API_SECRET


class UserBind(APIView):
    def validate_user(self):
        data = {
            "apikey": API_KEY,
            "apisecret": API_SECRET,
            "username": self.input['student_id'],
            "password": self.input['password']
        }
        headers = {'content-type': 'application/json'}
        r = requests.post('http://se.zhuangty.com/students/register', data=data, headers=headers)
        return_json = r.json()
        if return_json['message'] == 'Success':
            user = User.get_by_openid(self.input['openid'])
            user.user_id = return_json['information']['studentnumber']
            if return_json['information']['position'] == 'teacher':
                user.user_status = User.STATUS_TEACHER
            else:
                user.user_status = User.STATUS_STUDENT
            user.name = return_json['information']['realname']
            user.save()
        else:
            raise ValidateError("Password and Student ID is not matched")

    def get(self):
        self.check_input('openid')
        return User.get_by_openid(self.input['openid']).student_id

    def post(self):
        self.check_input('openid', 'student_id', 'password')
        self.validate_user()


class UserUnBind(APIView):
    def get(self):
        pass

    def post(self):
        pass