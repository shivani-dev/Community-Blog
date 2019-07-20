from django.db import models

# Create your models here.

class NewBlog(models.Model):
	user_id=models.IntegerField(null=True,blank=True)
	blog_name=models.CharField(max_length=100,blank=True,null=True)
	blog_content=models.CharField(max_length=1000,null=True,blank=True)

class create_new_user(models.Model):
	first_name=models.CharField(max_length=100,null=False)
	last_name=models.CharField(max_length=100,null=True,blank=True,default='')
	username=models.CharField(max_length=100,null=False)
	user_password=models.CharField(max_length=100,null=False,blank=False)
