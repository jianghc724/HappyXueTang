from codex.baseerror import *
from codex.baseview import APIView

import requests
import json
from datetime import datetime

from wechat.models import User, Course, StudentCourse
from HappyXueTang.settings import API_KEY, API_SECRET


class UserBind(APIView):
    def validate_user(self):
        data = {
            "apikey": API_KEY,
            "apisecret": API_SECRET,
            "username": self.input['user_id'],
            "password": self.input['password']
        }
        headers = {'content-type': 'application/json'}
        r = requests.post('http://se.zhuangty.com:8000/users/register', data=json.dumps(data), headers=headers)
        return_json = r.json()
        if return_json['message'] == 'Success':
            user = User.get_by_openid(self.input['open_id'])
            #print(return_json['information']['studentnumber'])
            user.user_id = return_json['information']['studentnumber']
            #print(return_json['information']['position'])
            if return_json['information']['position'] == 'teacher':
                user.user_status = User.STATUS_TEACHER
            else:
                #print(1)
                user.user_status = User.STATUS_STUDENT
            #print(return_json['information']['realname'])
            user.name = return_json['information']['realname']
            #print(2333)
            user.save()
        else:
            raise ValidateError("Password and Student ID is not matched")

    def get(self):
        self.check_input('open_id')
        #print(User.get_by_openid(self.input['open_id']).user_status)
        return User.get_by_openid(self.input['open_id']).user_status

    def post(self):
        self.check_input('open_id', 'user_id', 'password')
        self.validate_user()


class CourseList(APIView):
    def get(self):
        self.check_input('open_id', 'week')
        data = {
            "apikey": API_KEY,
            "apisecret": API_SECRET,
        }
        headers = {'content-type': 'application/json'}
        userid = User.get_by_openid(self.input['open_id']).user_id
        addr = 'http://se.zhuangty.com:8000/curriculum/' + userid + '?username=' + userid
        r = requests.post(addr, data=json.dumps(data), headers=headers)
        return_json = r.json()
        if return_json['message'] == 'Success':
            result = []
            for course_json in return_json['classes']:
                course_num_list = course_json['courseid'].split('-')
                courseid = course_num_list[3]
                coursenum = int(course_num_list[4])
                weeks = 0
                for week in course_json['week']:
                    weeks = weeks * 2 + int(week)
                times = course_json['time']
                time = times[0] * 10 + times[1]
                courses = Course.objects.filter(key=courseid).filter(number=coursenum).filter(week=weeks).filter(course_time=time)
                if not courses:
                    cou = Course.objects.create(name=course_json['coursename'], key=courseid, teacher=course_json['teacher'],
                                                week=weeks, location=course_json['classroom'], course_time=time, number=coursenum)
                    cou.save()
                else:
                    # judge semester
                    pass

                stucou = StudentCourse.objects.filter(student_id=userid).filter(course_key=courseid).filter(course_number=coursenum)
                if not stucou:
                    stu_cou = StudentCourse.objects.create(student_id=userid, course_key=courseid, course_number=coursenum)
                    stu_cou.save()
                #print(self.input['week'])
                if int(course_json['week'][int(self.input['week']) - 1]) == 1:
                    result.append({
                        'name':course_json['coursename'],
                        'time':times
                    })
            return result
        else:
            raise GetInfoError('Get Course List Failed')


class CourseDetail(APIView):
    def get(self):
        self.check_input('open_id', 'course_id')
        data = {
            "apikey": API_KEY,
            "apisecret": API_SECRET,
        }
        headers = {'content-type': 'application/json'}
        userid = User.get_by_openid(self.input['open_id']).user_id
        addr = 'http://se.zhuangty.com:8000/learnhelper/' + userid + '/courses?username=' + userid
        r = requests.post(addr, data=json.dumps(data), headers=headers)
        return_json = r.json()
        if return_json['message'] == 'Success':
            for course_json in return_json['classes']:
                course_num_list = course_json['courseid'].split('-')
                courseid = course_num_list[3]
                if courseid == self.input['course_id']:
                    result = {
                        'name': course_json['coursename'],
                        'notice': course_json['unreadnotice'],
                        'file': course_json['newfile'],
                        'homework': course_json['unsubmittedoperations']
                    }
                else:
                    continue
            raise LogicError('No such course')
        raise LogicError('Username Invalid')


class GetDeadline(APIView):
    def get(self):
        self.check_input('open_id')
        data = {
            "apikey": API_KEY,
            "apisecret": API_SECRET,
        }
        headers = {'content-type': 'application/json'}
        userid = User.get_by_openid(self.input['open_id']).user_id
        addr = 'http://se.zhuangty.com:8000/learnhelper/' + userid + '/courses?username=' + userid
        r = requests.post(addr, data=json.dumps(data), headers=headers)
        return_json = r.json()
        current_time = datetime.now().timestamp()
        if return_json['message'] == 'Success':
            result = []
            for course_json in return_json['classes']:
                course_num_list = course_json['courseid'].split('-')
                courseid = course_num_list[3]
                addr = 'http://se.zhuangty.com:8000/learnhelper/' + userid + '/courses/' + courseid \
                       + '/assignments?username=' + userid
                r = requests.post(addr, data=json.dumps(data), headers=headers)
                _return_json = r.json()
                # print(_return_json)
                if _return_json['message'] == 'Success':
                    assignments = _return_json['assignments']
                    for assignment in assignments:
                        if current_time > assignment['duedate'] and assignment['state'] == '尚未提交':
                            result.append({
                                'course_name':course_json['coursename'],
                                'homework_title':assignment['title'],
                                'homework_start_date':assignment['startdate'], #时间戳
                                'homework_end_date':assignment['duedate'], #时间戳
                                'current_time':current_time,
                            })
                else:
                    if _return_json['reason'] == 'Invalid username':
                        raise LogicError('Username Invalid')
                    elif _return_json['reason'] == 'Invalid courseID':
                        raise LogicError('CourseID Invalid')
                    else:
                        raise LogicError('Unknown error')
            return result
        raise LogicError('Username Invalid')


class CommentOverview(APIView):
    def get(self):
        pass


class MakeComment(APIView):
    def get(self):
        pass

    def post(self):
        pass
    