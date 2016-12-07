from codex.baseerror import *
from codex.baseview import APIView

import requests
import json

from wechat.models import User, Course, StudentCourse
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
        return User.get_by_openid(self.input['openid']).user_status

    def post(self):
        self.check_input('openid', 'student_id', 'password')
        self.validate_user()


class CourseList(APIView):
    def get(self):
        self.check_input('openid')
        data = {
            "apikey": API_KEY,
            "apisecret": API_SECRET,
        }
        headers = {'content-type': 'application/json'}
        userid = User.get_by_openid(self.input['openid']).user_id
        addr = 'http://se.zhuangty.com/curriculum/' + userid + '?username=' + userid
        r = requests.post(addr, data=data, headers=headers)
        return_json = r.json()
        if return_json['message'] == 'Success':
            result = []
            for course_json in return_json['classes']:
                courseid = course_json['coursid']
                coursenum = course_json['coursesequence']
                weeks = 0
                for week in course_json['week']:
                    weeks = weeks * 2 + week
                times = course_json['time']
                time = times[0] * 10 + times[1]
                courses = Course.objects.filter(course_id=courseid).filter(course_number=coursenum).filter(week=weeks).filter(course_time=time)
                if not courses:
                    cou = Course.objects.create(name=course_json['coursename'], key=course_json['coursid'], teacher=course_json['teacher'],
                                                week=weeks, location=course_json['classroom'], course_time=time, number=coursenum)
                    cou.save()

                stucou = StudentCourse.objects.filter(student_id=userid).filter(course_key=courseid).filter(course_number=coursenum)
                if not stucou:
                    stu_cou = StudentCourse.objects.create(student_id=userid, course_key=courseid, course_number=coursenum)
                    stu_cou.save()
                result.append({
                    'name':course_json['coursename'],
                    'week':weeks,
                    'time':times
                })
            return result
        else:
            raise GetInfoError('Get Course List Failed')


class CourseDetail(APIView):
    def get(self):
        pass
