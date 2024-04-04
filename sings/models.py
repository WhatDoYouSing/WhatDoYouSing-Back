from django.db import models
from accounts.models import User
from comments.models import Comment, Recomment
from posts.models import Post


class Sings(models.Model):
    #comment = models.ForeignKey(Comment, related_name='sings_comment',on_delete=models.CASCADE)
    #recomment = models.ForeignKey(Recomment, related_name='sings_recomment',on_delete=models.CASCADE)
    sings_post=models.ForeignKey(Post, related_name='sings_posts',on_delete=models.CASCADE)
    
class Memory(models.Model):
    non_user_recomlist=models.TextField()

'''    
    def get_comment_count(self):
        return self.sings_comments.count()

    def get_recomment_count(self):
        return self.sings_recomments.count()
'''
'''
    EMOTION_OPTION_1=models.CharField(max_length=50) #감정 쾌감
    EMOTION_OPTION_2=models.CharField(max_length=50) #감정 벅참
    EMOTION_OPTION_3=models.CharField(max_length=50) #감정 신남
    EMOTION_OPTION_4=models.CharField(max_length=50) #감정 행복
    EMOTION_OPTION_5=models.CharField(max_length=50) #감정 희망
    EMOTION_OPTION_6=models.CharField(max_length=50) #감정 설렘
    EMOTION_OPTION_7=models.CharField(max_length=50) #감정 평온
    EMOTION_OPTION_8=models.CharField(max_length=50) #감정 위로
    EMOTION_OPTION_9=models.CharField(max_length=50) #감정 센치함
    EMOTION_OPTION_10=models.CharField(max_length=50) #감정 쓸쓸함
    EMOTION_OPTION_11=models.CharField(max_length=50) #감정 그리움
    EMOTION_OPTION_12=models.CharField(max_length=50) #감정 슬픔

    SINGS_EMOTION_CHOICES = (
       
        (EMOTION_OPTION_1, '쾌감'),
        (EMOTION_OPTION_2, '벅참'),
        (EMOTION_OPTION_3, '신남'),
        (EMOTION_OPTION_4, '행복'),
        (EMOTION_OPTION_5, '희망'),
        (EMOTION_OPTION_6, '설렘'),
        (EMOTION_OPTION_7, '평온'),
        (EMOTION_OPTION_8, '위로'),
        (EMOTION_OPTION_9, '센치함'),
        (EMOTION_OPTION_10, '쓸쓸함'),
        (EMOTION_OPTION_11, '그리움'),
        (EMOTION_OPTION_12, '슬픔')

    )
    EMOTION_CHOICES = (
       
        (EMOTION_OPTION_1, '쾌감'),
        (EMOTION_OPTION_2, '벅참'),
        (EMOTION_OPTION_3, '신남'),
        (EMOTION_OPTION_4, '행복'),
        (EMOTION_OPTION_5, '희망'),
        (EMOTION_OPTION_6, '설렘'),
        (EMOTION_OPTION_7, '평온'),
        (EMOTION_OPTION_8, '위로'),
        (EMOTION_OPTION_9, '센치함'),
        (EMOTION_OPTION_10, '쓸쓸함'),
        (EMOTION_OPTION_11, '그리움'),
        (EMOTION_OPTION_12, '슬픔')

    )
 
    id=models.AutoField(primary_key=True) #포스트 고유번호
    user_id_nickName=models.ForeignKey(User, related_name='user_id_nickName',on_delete=models.SET_NULL,null=True) #작성자
    lyrics=models.CharField(max_length=200) #가사
    content=models.TextField() #해석
    title=models.CharField(max_length=100) #제목
    singer=models.CharField(max_length=50) #가사
    link=models.CharField(max_length=200) #원링크
    likes=models.IntegerField() #무한좋아요
    sings_emotion=models.CharField(choices=SINGS_EMOTION_CHOICES,max_length=100) #게시감정
    others_emotion=models.CharField(choices=EMOTION_CHOICES,max_length=100) #투표감정
    
    #ForeinKey -> 전부 다 foreignkey로 가져와야함.
    

    def __str__(self):
        return self.title
'''