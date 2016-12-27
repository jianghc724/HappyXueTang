from codex.baseerror import *
from codex.baseview import APIView

import requests
import json
from datetime import datetime

from wechat.models import *
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
            # print(return_json['information']['studentnumber'])
            user.user_id = return_json['information']['studentnumber']
            # print(return_json['information']['position'])
            if return_json['information']['position'] == 'teacher':
                user.user_status = User.STATUS_TEACHER
            else:
                # print(1)
                user.user_status = User.STATUS_STUDENT
            # print(return_json['information']['realname'])
            user.name = return_json['information']['realname']
            # print(2333)
            user.save()
        else:
            raise ValidateError("Password and Student ID is not matched")

    def get(self):
        self.check_input('open_id')
        # print(User.get_by_openid(self.input['open_id']).user_status)
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
                # print(self.input['week'])
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
                        'status': 1,
                        'notice': course_json['unreadnotice'],
                        'file': course_json['newfile'],
                        'homework': course_json['unsubmittedoperations']
                    }
                    return result
                else:
                    continue
            result = {
                'name': course_json['coursename'],
                'status': -1,
            }
            return result
        raise GetInfoError('Username Invalid')


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
                       + '/assignments?username=' + userid + '&courseid=' + courseid
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
                                'homework_start_date':assignment['startdate'],
                                'homework_end_date':assignment['duedate'],
                                'current_time':current_time,
                            })
                else:
                    if _return_json['reason'] == 'Invalid username':
                        raise GetInfoError('Username Invalid')
                    elif _return_json['reason'] == 'Invalid courseID':
                        raise GetInfoError('CourseID Invalid')
                    else:
                        raise GetInfoError('Unknown error')
            return result
        raise GetInfoError('Username Invalid')


class GetNotice(APIView):
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
                       + '/notices?username=' + userid + '&courseid=' + courseid
                r = requests.post(addr, data=json.dumps(data), headers=headers)
                _return_json = r.json()
                # print(_return_json)
                if _return_json['message'] == 'Success':
                    notices = _return_json['notices']
                    for notice in notices:
                        noticeid = notice['noticeid']
                        _notices = StudentNotice.objects.filter(notice_id=noticeid).filter(student_id=userid)
                        if not _notices:
                            noc = StudentNotice.objects.create(notice_id=noticeid, student_id=userid, is_read=notice['state'])
                            noc.save()
                        else:
                            noc = StudentNotice.objects.filter(notice_id=noticeid).get(student_id=userid)
                        if notice['state'] == 'unread' and noc.is_read == False:
                            result.append({
                                'course_name':course_json['coursename'],
                                'notice_id':notice['noticeid'],
                                'notice_title':notice['title'],
                                'notice_publisher':notice['publisher'],
                                'notice_publishtime':notice['publishtime'],
                                'notice_content':notice['content'],
                                'current_time':current_time,
                            })
                else:
                    if _return_json['reason'] == 'Invalid username':
                        raise GetInfoError('Username Invalid')
                    elif _return_json['reason'] == 'Invalid courseID':
                        raise GetInfoError('CourseID Invalid')
                    else:
                        raise GetInfoError('Unknown error')
            return result
        raise GetInfoError('Username Invalid')

    def post(self):
        self.check_input('open_id', 'notice_id')
        userid = User.get_by_openid(self.input['open_id']).user_id
        noc = StudentNotice.objects.filter(notice_id=self.input['notice_id']).get(student_id=userid)
        noc.is_read = True
        noc.save()


class CommentOverview(APIView):
    def get(self):
        self.check_input('course_id', 'course_number')
        try:
            cou = Course.objects.filter(key=self.input['course_id']).get(number=self.input['course_number'])
        except:
            raise CourseError('No such course')
        result = {
            'ratings': [],
            'comments': [],
            'course_info':{
                'course_id': cou.key,
                'course_number': cou.number,
                'course_name': cou.name,
            },
        }
        result['ratings'].append(cou.rating_one, cou.rating_two, cou.rating_three)
        result['comments'] = self.get_comment_list(cou)
        return result

    def get_comment_list(self, cou):
        all_comments = Comment.objects.filter(course_key=cou.key).filter(course_number=cou.number)
        comments = []
        for comment in all_comments:
            if len(comments) == 10 and comment.rating_time < comments[9]['rating_time']:
                continue
            student = User.objects.get(user_id=comment.student_id)
            com = {
                'student': student.name,
                'time':comment.rating_time,
                'comment':comment.rating_comment,
            }
            if len(comments) == 10:
                comments[9] = com
            else:
                comments[len(comments)] = com
            comments = self.sort_comment_list(comments)
        return comments

    def sort_comment_list(self, comment_list):
        i = len(comment_list) - 1
        while True:
            if i == 0:
                break
            if comment_list[i]['time'] < comment_list[i - 1]['time']:
                break
            temp_com = comment_list[i]
            comment_list[i] = comment_list[i - 1]
            comment_list[i - 1] = temp_com
            i = i - 1
        return comment_list


class MakeComment(APIView):
    def get(self):
        self.check_input('course_id', 'course_number')
        try:
            cou = Course.objects.filter(key=self.input['course_id']).get(number=self.input['course_number'])
        except:
            raise CourseError('No such course')
        result = {
            'ratings': [],
            'course_info': {
                'course_id': cou.key,
                'course_number': cou.number,
                'course_name': cou.name,
            },
        }
        result['ratings'].append(cou.rating_one, cou.rating_two, cou.rating_three)
        return result

    def post(self):
        self.check_input('open_id', 'course_id', 'course_number', 'rating_one', 'rating_two', 'rating_three', 'comment')
        try:
            cou = Course.objects.filter(key=self.input['course_id']).get(number=self.input['course_number'])
        except:
            raise CourseError('No such course')
        user = User.get_by_openid(self.input['open_id'])
        current_time = datetime.now().timestamp()
        com = Comment.objects.create(student_id=user.user_id, course_key=self.input['course_id'], course_number=self.input['course_number'],
                                     rating_one=self.input['rating_one'], rating_two=self.input['rating_two'], rating_three=self.input['rating_three'],
                                     rating_time=current_time, rating_comment = self.input['comment'])
        com.save()
        total_people = cou.rating_people
        total_rating_one = cou.rating_one * total_people
        cou.rating_one = (total_rating_one + self.input['rating_one']) / (total_people + 1)
        total_rating_two = cou.rating_two * total_people
        cou.rating_two = (total_rating_two + self.input['rating_two']) / (total_people + 1)
        total_rating_three = cou.rating_three * total_people
        cou.rating_three = (total_rating_three + self.input['rating_three']) / (total_people + 1)
        cou.rating_people = total_people + 1
        cou.save()


class UserNotify(APIView):
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
        result = {
            "total": {}, #字典，显示用户全部的未读公告数、未下载文件数和未交作业数
            "new_detail": {
                "new_notices": [],
                "new_files": [],
                "new_operations": [],
            }, #字典，存储所有未读公告、未下载文件和未交作业
        }
        if return_json['message'] == "Success":
            courses = return_json['courses']
            total_unreadnotice = 0
            total_newfile = 0
            total_unsubmittedoperations = 0
            for course in courses:
                total_unreadnotice += course['unreadnotice']
                total_newfile += course['newfile']
                total_unsubmittedoperations += course['unsubmittedoperations']
                courseid = course['courseid']
                notice_addr = 'http://se.zhuangty.com:8000/learnhelper/' + userid + '/courses/' + courseid + '/notices?username=' + userid + '&courseid=' + courseid
                file_addr = 'http://se.zhuangty.com:8000/learnhelper/' + userid + '/courses/' + courseid + '/documents?username=' + userid + '&courseid=' + courseid
                operation_addr = 'http://se.zhuangty.com:8000/learnhelper/' + userid + '/courses/' + courseid + '/assignments?username=' + userid + '&courseid=' + courseid
                notice_json = requests.post(notice_addr, data=json.dumps(data), headers=headers).json()
                file_json = requests.post(file_addr, data=json.dumps(data), headers=headers).json()
                operation_json = requests.post(operation_addr, data=json.dumps(data), headers=headers).json()
                if notice_json['message'] == "Failure":
                    raise GetInfoError(notice_json['reason'] + "for notice")
                if file_json['message'] == "Failure":
                    raise GetInfoError(file_json['reason'] + "for file")
                if operation_json['message'] == "Failure":
                    raise GetInfoError[operation_json['reason'] + "for operation"]
                notices = notice_json['notices']
                for notice in notices:
                    noticeid = notice['noticeid']
                    if not Notice.objects.filter(notice_key=noticeid).exists():
                        pass
                    if notice.state == "unread":
                        result['new_notices'].append({
                            'title': notice['title'],
                            'publishtime': notice['publishtime'],
                            'content': notice['content'],
                        })
                files = file_json['documents']
                for file in files:
                    if file.state == "new":
                        result['new_files'].append({
                            'title': file['title'],
                            'explanation': file['explanation'],
                            'updatingtime': file['updatingtime'],
                            'size': file['size'],
                            'url': file['url'],
                        })
                operations = operation_json['assignments']
                for operation in operations:
                    if operation.state == "尚未提交":
                        result['new_operations'].append({
                                'title': operation['title'],
                                'startdate': operation['startdate'],
                                'duedate': operation['duedate'],
                                'detail': operation['detail'],
                                'fileurl': operation['fileurl'],
                            })
            result['total']['total_unreadnotice'] = total_unreadnotice
            result['total']['total_newfile'] = total_newfile
            result['total']['total_unsubmittedoperations'] = total_unsubmittedoperations
            return result
        else:
            raise GetInfoError('Username Invalid')


class BulletScreen(APIView):
    def get(self):
        self.check_input('course_id', 'course_number')
        discussions = Discussion.objects.filter(course_key=self.input['course_id']).\
            filter(course_number=self.input['course_number']).filter(status=False)
        result = []
        for discuss in discussions:
            result.append({
                'content':discuss.content,
                'release_time':discuss.release_time,
            })
            discuss.status = True
            discuss.save()
        return result


class LibraryStatus(APIView):
    def get(self):
        self.check_input('open_id', 'course_id')
        data = {
            "apikey": API_KEY,
            "apisecret": API_SECRET,
        }
        headers = {'content-type': 'application/json'}
        userid = User.get_by_openid(self.input['open_id']).user_id
        addr = 'http://se.zhuangty.com:8000/library/hs'
        r = requests.post(addr, data=json.dumps(data), headers=headers)
        return_json = r.json()
        if return_json['message'] == 'Success':
            areas = return_json['areas']
            result = areas
            return result
        raise LogicError('Library Info Unavailable')


class InfoSearch(APIView):
    def get(self):
        self.check_input('open_id', 'course_id', 'search')
        search = self.input['search']
        courseid = self.input['course_id']
        userid = User.get_by_openid(self.input['open_id']).user_id
        result = {
            'courses':[],
            'notices': [],
            'operations': [],
        }
        studentnotices = StudentNotice.objects.filter(student_id=userid)
        for studentnotice in studentnotices:
            notice = studentnotice.notice
            if (search in notice.title) or (search in notice.content):
                result['notices'].append({
                    'title': notice.title,
                    'content': notice.content,
                })
        studentoperations = StudentHomework.objects.filter(student_id=userid)
        for studentoperation in studentoperations:
            operation = studentoperation.homework
            if (search in operation.title) or (search in operation.content):
                result['operations'].append({
                    'title': operation.title,
                    'content': operation.instructions,
                })
        courses = Course.objects.all()
        for cou in courses:
            if search in cou.name:
                result['courses'].append({
                    'course_id': cou.key,
                    'course_number': cou.number,
                    'course_name': cou.name,
                    'course_teacher': cou.teacher,
                })
        return result

