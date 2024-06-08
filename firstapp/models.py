from django.db import models
from django.contrib.auth.models import User 
import datetime
import os

def getFileName(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H;%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)


class catagory(models.Model):
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    created_at=models.DateField(auto_now_add=True)
    def __str__ (self):
        return self.name


class product(models.Model):
    catagory=models.ForeignKey(catagory,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=False,blank=False)
    brand=models.CharField(max_length=150,null=False,blank=False,default="Null")
    model=models.CharField(max_length=150,null=False,blank=False,default="Null")
    ram=models.CharField(max_length=3,null=False, blank=True)
    product_image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    quantity=models.IntegerField(null=False,blank=False)
    originl_price=models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    trending=models.BooleanField(default=False,help_text="0-defauft,1-Trending")
    created_at=models.DateField(auto_now_add=True)
    alert_sent = models.BooleanField(default=False)

    def Ram(self,*args,**kwargs):
        if self.catagory != "Mobiles":
            self.ram=None
        super(product,self).save(*args,**kwargs)

    def __str__ (self):
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return self.product_qty*self.product.selling_price

