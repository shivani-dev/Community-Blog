from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from community_blog.models import NewBlog,create_new_user
from django.views.generic import *
from django.conf import settings

# Create your views here.
class index(View):
	def get(self,request):
		try:
			user_val=request.session['user_id']
			if user_val != "":
				user_details=create_new_user.objects.get(id=user_val)
				show_username=user_details.first_name
				show_create_blog=1
		except KeyError:
			show_username=""
			show_create_blog=0
		blogs={}
		all_posts=NewBlog.objects.all().values('id','user_id','blog_name')
		i=0
		for each_posts in all_posts:
			i+=1
			blog_name=each_posts['blog_name']
			blog_id=each_posts['id']
			user_id=each_posts['user_id']
			blogs[i]={}
			blogs[i][user_id]={}
			blogs[i][user_id][blog_id]={}
			blogs[i][user_id][blog_id]=blog_name
		print(blogs)
		return render(self.request,'index_blog.html',{"blogs":blogs,"show_username":show_username,"show_create_blog":show_create_blog})


class add_new_blog(View):
	def get(self,request):
		try:
			if request.session['user_id'] != "":
				return render(self.request,'add_new_blog.html',{"show_username":"","show_create_blog":1})
		except KeyError:
			return render(self.request,'add_new_blog.html',{"show_username":"","show_create_blog":0})

	def post(self,request):
		try:
			if request.method == "POST" and request.session['user_id'] != "":
				blog_name_val=request.POST['blog_name']
				blog_content_val=request.POST['blog_content']
				if blog_name_val != "" and blog_content_val != "":
					user_id_val=request.session['user_id']
					blog_data=NewBlog.objects.create(user_id=user_id_val,blog_name=blog_name_val,blog_content=blog_content_val)
				return HttpResponseRedirect("new_or_existing_user")
		except KeyError:
			return HttpResponseRedirect("index_blog")

class blog_details(View):
	def get(self,request,user_id,blog_key):
		blog_id_content=NewBlog.objects.get(id=blog_key)
		blog_owner=create_new_user.objects.get(id=user_id)
		first_name=blog_owner.first_name
		last_name=blog_owner.last_name
		if first_name != "":
			blog_owner=first_name
			if last_name != "":
				blog_owner=blog_owner+" "+last_name
			else:
				pass
		else:
			blog_owner="Anonymous"
		blog_name=blog_id_content.blog_name
		blog_content=blog_id_content.blog_content
		try:
			if request.session['user_id'] != "":
				show_create_blog=1
				session_user=create_new_user.objects.get(id=request.session['user_id']).first_name
		except KeyError:
			show_create_blog=0
			session_user=""
		return render(self.request,'blog_details.html',{"show_username":session_user,"blog_name":blog_name,"blog_content":blog_content,"blog_owner":blog_owner,"show_create_blog":show_create_blog})

class new_or_existing_user(View):
	def get(self,request):
		try:
			if request.session['user_id'] != "":
				user_details=create_new_user.objects.get(id=request.session['user_id'])
				blogs={}
				user_first_name=user_details.first_name
				user_blogs=NewBlog.objects.filter(user_id=user_details.id)
				show_create_blog=1
				for each_post_user in user_blogs:
					blog_name=each_post_user.blog_name
					blog_id=each_post_user.id
					blogs[blog_id]={}
					blogs[blog_id][blog_name]=each_post_user.blog_content
				return render(self.request,'login_user_account.html',{"show_username":user_first_name,"blogs":blogs,"user_id":user_details.id,"show_create_blog":show_create_blog})

		except KeyError:
			wrong_credentials=0
			show_username=""
			show_create_blog=0
			return render(self.request,'new_or_existing_user.html',{"wrong_user":wrong_credentials,"show_username":"","show_create_blog":show_create_blog})

	def post(self,request):
		if request.method == "POST":
			login_or_register=int(request.POST['login_form'])
			if login_or_register == 1:
				user_name=request.POST['user_name']
				user_passwrd=request.POST['user_passwrd']
				if user_name != "" and user_passwrd != "":
					check_user_exist=create_new_user.objects.get(username=user_name,user_password=user_passwrd)
					if not check_user_exist:
						wrong_credentials=1
						show_create_blog=0
						return render(self.request,'new_or_existing_user.html',{"wrong_user":wrong_credentials,"show_create_blog":show_create_blog})
					else:
						blogs={}
						user_details=create_new_user.objects.get(username=user_name,user_password=user_passwrd)
						user_first_name=user_details.first_name
						user_blogs=NewBlog.objects.filter(user_id=user_details.id)
						request.session['user_id']=user_details.id
						show_create_blog=1
						for each_post_user in user_blogs:
							blog_name=each_post_user.blog_name
							blog_id=each_post_user.id
							blogs[blog_id]={}
							blogs[blog_id][blog_name]=each_post_user.blog_content
						return render(self.request,'login_user_account.html',{"show_username":user_first_name,"blogs":blogs,"user_id":user_details.id,"show_create_blog":show_create_blog})
			else:
				first_name=request.POST['first_name']
				last_name=request.POST['last_name']
				user_name=request.POST['user_name']
				user_passwrd=request.POST['user_password']
				confirm_passwrd=request.POST['user_confirm_password']
				if user_passwrd == confirm_passwrd:
					create_user_db=create_new_user.objects.get_or_create(first_name=first_name,last_name=last_name,username=user_name,user_password=user_passwrd)
					return HttpResponseRedirect('index_blog')

def logout_current_session(request):
	try:
		del request.session['user_id']
	except KeyError:
		pass
	return HttpResponseRedirect('index_blog')

def delete_blog(request,user_id,blog_id):
	if request.session['user_id'] != "" and request.method == "POST":
		# blog_id=request.POST['delete_each_blog']
		if blog_id != "":
			blog_deleted=NewBlog.objects.get(id=blog_id).delete()
			return HttpResponseRedirect('/py/community_blog/new_or_existing_user')

def edit_blog_items(request,user_id,blog_id):
	try:
		if request.session['user_id'] != "":
			blog_name=request.POST['blog_name']
			blog_content=request.POST['blog_content']
			update_data=NewBlog.objects.update_or_create(id=blog_id,user_id=user_id,defaults={"blog_name":blog_name,"blog_content":blog_content})
			return HttpResponseRedirect('/py/community_blog/new_or_existing_user')
	except KeyError:
		return HttpResponseRedirect('index_blog')

