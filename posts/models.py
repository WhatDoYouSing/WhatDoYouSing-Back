from django.db import models

# Create your models here.

class Post(models.Model):
    
    SINGS_EMOTION_CHOICES = [
        (0, '쾌감'),
        (1, '벅참'),
        (2, '신남'),
        (3, '행복'),
        (4, '희망'),
        (5, '설렘'),
        (6, '평온'),
        (7, '위로'),
        (8, '센치함'),
        (9, '쓸쓸함'),
        (10, '그리움'),
        (11, '슬픔'),
    ]

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey("accounts.User", null=True, on_delete=models.CASCADE)  # 게시물 작성자
    lyrics = models.CharField(max_length=200)
    #투표감정 여기에 추가 (others_emotion)
    content = models.TextField(max_length=300)
    title = models.CharField(max_length=200)
    singer = models.CharField(max_length=200)
    link = models.CharField(max_length=200, null=True)

    sings_emotion=models.IntegerField(choices=SINGS_EMOTION_CHOICES) #게시감정

    #likes = models.ManyToManyField("accounts.User", related_name="liked_posts", blank=True)
    likes_count = models.IntegerField(default=0)  # 좋아요 갯수 필드 추가

    def increase_likes_count(self):
        self.likes_count += 1
        self.save(update_fields=['likes_count'])

    scrap = models.ManyToManyField("accounts.User", related_name="scraped_posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

class Emotion(models.Model):
    user = models.ForeignKey("accounts.User", null=True, on_delete=models.CASCADE)  # 게시물 작성자

    EMOTION_CHOICES = [
        (0, '쾌감'),
        (1, '벅참'),
        (2, '신남'),
        (3, '행복'),
        (4, '희망'),
        (5, '설렘'),
        (6, '평온'),
        (7, '위로'),
        (8, '센치함'),
        (9, '쓸쓸함'),
        (10, '그리움'),
        (11, '슬픔'),
    ]

    emo_id=models.AutoField(primary_key=True)
    content=models.IntegerField(choices=EMOTION_CHOICES)
    emo_post=models.ForeignKey(Post, related_name='emo_post',on_delete=models.CASCADE)
    emo_user=models.ForeignKey("accounts.User", related_name='emo_user',on_delete=models.CASCADE)
