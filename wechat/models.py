from django.db import models

from codex.baseerror import LogicError


class User(models.Model):
    open_id = models.CharField(max_length=64, unique=True, db_index=True)
    user_id = models.CharField(max_length=16, db_index=True)
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
    course_id = models.CharField(max_length=32)
    teacher = models.CharField(max_length=32)
    semester = models.IntegerField(default=3)
    week = models.IntegerField()
    location = models.CharField(max_length=128)
    course_time = models.IntegerField()
    exam_start_time = models.DateTimeField(null=True, blank=True)
    exam_end_time = models.DateTimeField(null=True, blank=True)
    exam_location = models.CharField(max_length=128, null=True, blank=True)
    rating_people = models.IntegerField(default=0)
    rating_one = models.FloatField(default=-1,blank=True,null=True)
    rating_two = models.FloatField(default=-1,blank=True,null=True)
    rating_three = models.FloatField(default=-1,blank=True,null=True)


    COURSE_CANCELLED = -1
    COURSE_AUTUMN_ONLY = 1
    COURSE_SPRING_ONLY = 2
    COURSE_BOTH_SEMESTER = 3
    COURSE_SUMMER_ONLY = 4


class Discussion(models.Model):
    student_id = models.CharField(max_length=16)
    course_key = models.CharField(max_length=16, db_index=True)
    course_number = models.IntegerField()
    release_time = models.DateTimeField()
    content = models.TextField()
    status = models.BooleanField()


class Comment(models.Model):
    student_id = models.CharField(max_length=16)
    course_key = models.CharField(max_length=16, db_index=True)
    course_number = models.IntegerField()
    semester = models.CharField(max_length=16, blank=True)
    rating_time = models.DateTimeField()
    rating_one = models.IntegerField()
    rating_two = models.IntegerField()
    rating_three = models.IntegerField()
    rating_comment = models.TextField()


class StudentCourse(models.Model):
    student_id = models.CharField(max_length=16, db_index=True)
    course_key = models.CharField(max_length=16, db_index=True)
    course_number = models.IntegerField()
    course_id = models.CharField(max_length=32)
    semester = models.CharField(max_length=16)
    status = models.IntegerField(default=0, null=True, blank=True)
    grading_policy = models.IntegerField(null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)

    COURSE_WITHDRAWN = -1
    COURSE_IN_PROGRESS = 0
    COURSE_FINISHED = 1

    COURSE_PF = 0
    COURSE_RATING = 1
