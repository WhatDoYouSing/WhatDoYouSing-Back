# Generated by Django 3.2.8 on 2024-04-04 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sings', '0002_alter_sings_sings_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Memory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('non_user_recomlist', models.TextField()),
            ],
        ),
    ]