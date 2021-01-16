from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=11,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name
class Product(models.Model):
    name=models.CharField(max_length=50)
    product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
    price = models.PositiveIntegerField()
    description=models.CharField(max_length=50)
    def __str__(self):
        return self.name
  
class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name