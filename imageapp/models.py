from django.db import models
import bcrypt
from django.core.files.storage import FileSystemStorage
from django.conf import  settings

# Create your models here.
file_system = FileSystemStorage(location=settings.FILE_SYSTEM)

class User(models.Model):
    email = models.EmailField(max_length=200, null=False, unique=True, blank=False)
    first_name = models.CharField(max_length=60, null=False, blank=False)
    second_name = models.CharField(max_length=60, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)

    # def __setattr__(self, key, value):
    #     if key == 'password' and value:
    #         print key, value
    #         value = self.hash_password(value)
    #     super(User, self).__setattr__(key, value)


    def hash_password(self, value):
        value = value.encode('ascii','ignore')
        print 'CALLED', value
        return bcrypt.hashpw(value, bcrypt.gensalt())

    def __unicode__(self):
        return "{0} {1}".format(self.first_name, self.second_name)

    @staticmethod
    def return_valid_user(email_address, raw_password):
        raw_password = raw_password.encode('ascii','ignore')
        user = User.objects.filter(email=email_address, password=raw_password)[:1].get()
        return user if user != None else None


class Picture(models.Model):
    user = models.ForeignKey(User, null=False, related_name='pictures')
    photo = models.ImageField(storage=file_system)

    def __unicode__(self):
        return "{0} {1}".format(self.user, self.photo)

