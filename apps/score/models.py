from datetime import datetime
from django.db import models


class Students(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="学号", help_text="学生唯一识别号")
    name = models.CharField(max_length=20, verbose_name="学生姓名", help_text="学生姓名")
    score = models.FloatField(default=0, verbose_name="科目得分")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        app_label = "score"
        verbose_name = "学生"
        verbose_name_plural = "学生"

    def __str__(self):
        return self.name


class Answers(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="id")
    answer = models.CharField(max_length=300, verbose_name="答案内容", help_text="答案内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        app_label = "score"
        verbose_name = "答案"
        verbose_name_plural = "答案"

    def __str__(self):
        return self.answer


class Questions(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="id")
    question_num = models.IntegerField(verbose_name="问题num", help_text="问题唯一识别号")
    question = models.CharField(max_length=300, verbose_name="问题内容", help_text="问题内容")
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE)
    score = models.FloatField(default=0, verbose_name="分数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        app_label = "score"
        verbose_name = "题目"
        verbose_name_plural = "题目"

    def __str__(self):
        return self.question


class Papers(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="试卷id", help_text="试卷唯一识别号")
    title = models.CharField(max_length=300, verbose_name="试卷标题", help_text="试卷标题")
    score = models.FloatField(default=0, verbose_name="试卷总分")
    question = models.ManyToManyField(Questions)
    student = models.ManyToManyField(Students)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        app_label = "score"
        verbose_name = "试卷"
        verbose_name_plural = "试卷"

    def __str__(self):
        return self.title
