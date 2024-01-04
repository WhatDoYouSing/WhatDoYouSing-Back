from django.db import models
from accounts.models import User
from posts.models import Post

# Create your models here.

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    author = models.ForeignKey("accounts.User", null=True, on_delete=models.CASCADE)  # 댓글 작성자
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    com_content = models.TextField()  # 댓글 내용
    com_likes = models.ManyToManyField('accounts.User',related_name="liked_comments", blank=True )
    created_at = models.DateTimeField(auto_now_add=True)

class Recomment(models.Model):
    recomment_id = models.AutoField(primary_key=True)
    author = models.ForeignKey('accounts.User', null=True, on_delete=models.CASCADE) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", null=True) # 대댓글 작성자
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="recomments", null=True)
    com_content = models.TextField()  
    com_relikes = models.ManyToManyField("accounts.User", related_name="liked_recomments", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)