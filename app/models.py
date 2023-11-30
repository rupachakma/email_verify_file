from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils.crypto import get_random_string
from django.core.mail import send_mail


class Customusermanager(BaseUserManager):
    def create_user(self,phone_num,password=None,**extra_fields):
        if not phone_num:
            raise ValueError("Phone number required")
        
        user = self.model(phone_num=phone_num,**extra_fields)
        user.set_password(password)
        user.generate_token()
        user.email_verification()
        user.save(using=self._db)
        return user
    
    def create_superuser(self,phone_num,password,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault('is_active',True)
        return self.create_user(phone_num,password,**extra_fields)
        

# Create your models here.
class Customuser(AbstractBaseUser,PermissionsMixin):
    phone_num = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_img = models.ImageField(upload_to="profile_pic",blank=True,null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    verification_token = models.CharField(max_length=100,blank=True,null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    class Meta:
        db_table = "custom_user"


    def __str__(self):
        return self.phone_num


    objects = Customusermanager()
    USERNAME_FIELD = "phone_num"
    REQUIRED_FIELDS = ['email','first_name']


    def generate_token(self):
        self.verification_token = get_random_string(50)


    def email_verification(self):
        subjects = "Verify your email"
        message = f"Hi, {self.first_name}! \n\n Click the following link to verify your email\n\n http://127.0.0.1:8000/verify/?token={self.verification_token}"
        send_mail(subjects,message,"joy572064@gmail.com",[self.email])
