from django.db import models

from codex.baseerror import LogicError


class User(models.Model):
    open_id = models.CharField(max_length=64, unique=True, db_index=True)
    user_id = models.CharField(max_length=16, unique=True, db_index=True)
    user_status = models.IntegerField(default=-1)
    name = models.CharField(max_length=32)

    STATUS_UNBIND = -1
    STATUS_STUDENT = 0
    STATUS_TEACHER = 1

    @classmethod
    def get_by_openid(cls, openid):
        try:
            return cls.objects.get(open_id=openid)
        except cls.DoesNotExist:
            raise LogicError('User not found')


class Course(models.Model):
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=16, db_index=True)
    number = models.IntegerField()
    teacher = models.CharField(max_length=32)
    semester = models.IntegerField()
    week = models.IntegerField()
    location = models.CharField(max_length=128)
    course_time = models.CharField(max_length=128)
    exam_start_time = models.DateTimeField()
    exam_end_time = models.DateTimeField()
    exam_location = models.CharField(max_length=128)
    rating = models.FloatField()

    COURSE_CANCELLED = -1
    COURSE_AUTUMN_ONLY = 1
    COURSE_SPRING_ONLY = 2
    COURSE_BOTH_SEMESTER = 3
    COURSE_SUMMER_ONLY = 4


class Notice(models.Model):
    course_key = models.CharField(max_length=16,db_index=True)
    course_number = models.IntegerField()
    title = models.CharField(max_length=32)
    content = models.TextField()
    release_person = models.CharField(max_length=32)
    release_time = models.DateTimeField()


class Homework(models.Model):
    course_key = models.CharField(max_length=16,db_index=True)
    course_number = models.IntegerField()
    title = models.CharField(max_length=32)
    instructions = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(db_index=True)
    has_attachment = models.BooleanField()


class Discussion(models.Model):
    student_id = models.CharField(max_length=16)
    course_key = models.CharField(max_length=16,db_index=True)
    course_number = models.IntegerField()
    release_time = models.DateTimeField()
    content = models.TextField()


class Comment(models.Model):
    student_id = models.CharField(max_length=16)
    course_key = models.CharField(max_length=16,db_index=True)
    course_number = models.IntegerField()
    semester = models.CharField(max_length=8)
    rating_time = models.DateTimeField()
    rating = models.IntegerField()
    rating_comment = models.TextField()


class StudentCourse(models.Model):
    student_id = models.CharField(max_length=16, db_index=True)
    course_key = models.CharField(max_length=16, db_index=True)
    course_number = models.IntegerField()
    semester = models.CharField(max_length=8)
    status = models.IntegerField()
    grading_policy = models.IntegerField()
    grade = models.IntegerField()

    COURSE_WITHDRAWN = -1
    COURSE_IN_PROGRESS = 0
    COURSE_FINISHED = 1

    COURSE_PF = 0
    COURSE_RATING = 1


class StudentNotice(models.Model):
    student_id = models.CharField(max_length=16, db_index=True)
    notice = models.ForeignKey(Notice)
    is_read = models.BooleanField()


class StudentHomework(models.Model):
    student_id = models.CharField(max_length=16, db_index=True)
    homework = models.ForeignKey(Homework)
    status = models.BooleanField()
    content = models.TextField()
