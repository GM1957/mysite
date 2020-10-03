from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Product(models.Model):
    productUniquename = models.CharField(max_length=200)
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200,unique = True)
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null = True,blank=True,default=now)
    image = models.ImageField(upload_to="home/images")
    #slug = models.CharField(max_length=200)

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    contactsno = models.AutoField(primary_key = True)
    name = models.CharField(max_length=300)
    phonenumber = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name

class userdata(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    profile_pic = models.ImageField(upload_to="home/images/userprofileimages",default='home/images/userprofileimages/defaultuser.png')
    def __str__(self):
        return str(self.user)  

# class userinfo(models.Model):
#     user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
#     profile_pic = models.ImageField(upload_to="home/images/userprofileimages",blank=True,default='home/images/userprofileimages/defaultuser.png')
#     def __str__(self):
#         return str(self.user)