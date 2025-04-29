from django.db import models

# Create your models here.
class Basemodel(models.Model):
    created = models.DateTimeField(auto_now_add=True) # 객체 생성 시각 저장

    class Meta:
        abstract = True # 추상 클래스


class GuestbookStructure(Basemodel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30) # 제목 : 글자수 30자 제한
    author = models.CharField(max_length=30) # 방명록 작성자의 글자 수도 30자 제한
    body = models.TextField()
    password = models.CharField(max_length=16) # 비밀번호 글자수 16자자 제한   