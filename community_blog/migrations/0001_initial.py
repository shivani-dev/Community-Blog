# Generated by Django 2.2 on 2019-07-14 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewBlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('blog_name', models.CharField(blank=True, max_length=100, null=True)),
                ('blog_content', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
    ]
