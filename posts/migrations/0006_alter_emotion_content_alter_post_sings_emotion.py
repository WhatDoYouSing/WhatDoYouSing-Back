# Generated by Django 5.0.1 on 2024-01-07 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_emotion_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emotion',
            name='content',
            field=models.IntegerField(choices=[(0, '쾌감'), (1, '벅참'), (2, '신남'), (3, '행복'), (4, '희망'), (5, '설렘'), (6, '평온'), (7, '위로'), (8, '센치함'), (9, '쓸쓸함'), (10, '그리움'), (11, '슬픔')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='sings_emotion',
            field=models.IntegerField(choices=[(0, '쾌감'), (1, '벅참'), (2, '신남'), (3, '행복'), (4, '희망'), (5, '설렘'), (6, '평온'), (7, '위로'), (8, '센치함'), (9, '쓸쓸함'), (10, '그리움'), (11, '슬픔')]),
        ),
    ]
