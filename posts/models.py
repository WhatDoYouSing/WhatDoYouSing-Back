from django.db import models

# Create your models here.

class Post(models.Model):
    EMOTION_OPTION_1=models.CharField(max_length=50, null=True) #감정 쾌감
    EMOTION_OPTION_2=models.CharField(max_length=50, null=True) #감정 벅참
    EMOTION_OPTION_3=models.CharField(max_length=50, null=True) #감정 신남
    EMOTION_OPTION_4=models.CharField(max_length=50, null=True) #감정 행복
    EMOTION_OPTION_5=models.CharField(max_length=50, null=True) #감정 희망
    EMOTION_OPTION_6=models.CharField(max_length=50, null=True) #감정 설렘
    EMOTION_OPTION_7=models.CharField(max_length=50, null=True) #감정 평온
    EMOTION_OPTION_8=models.CharField(max_length=50, null=True) #감정 위로
    EMOTION_OPTION_9=models.CharField(max_length=50, null=True) #감정 센치함
    EMOTION_OPTION_10=models.CharField(max_length=50, null=True) #감정 쓸쓸함
    EMOTION_OPTION_11=models.CharField(max_length=50, null=True) #감정 그리움
    EMOTION_OPTION_12=models.CharField(max_length=50, null=True) #감정 슬픔

    SINGS_EMOTION_CHOICES = [
        ('쾌감', '쾌감'),
        ('벅참', '벅참'),
        ('신남', '신남'),
        ('행복', '행복'),
        ('희망', '희망'),
        ('설렘', '설렘'),
        ('평온', '평온'),
        ('위로', '위로'),
        ('센치함', '센치함'),
        ('쓸쓸함', '쓸쓸함'),
        ('그리움', '그리움'),
        ('슬픔', '슬픔'),
    ]

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey("accounts.User", null=True, on_delete=models.CASCADE)  # 게시물 작성자
    lyrics = models.CharField(max_length=60)
    #투표감정 여기에 추가 (others_emotion)
    content = models.TextField(max_length=150)
    title = models.CharField(max_length=200)
    singer = models.CharField(max_length=200)
    link = models.CharField(max_length=200, null=True)

    sings_emotion=models.CharField(choices=SINGS_EMOTION_CHOICES,max_length=50) #게시감정

    #likes = models.ManyToManyField("accounts.User", related_name="liked_posts", blank=True)
    likes_count = models.IntegerField(default=0)  # 좋아요 갯수 필드 추가

    def increase_likes_count(self):
        self.likes_count += 1
        self.save(update_fields=['likes_count'])

    scrap = models.ManyToManyField("accounts.User", related_name="scraped_posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

