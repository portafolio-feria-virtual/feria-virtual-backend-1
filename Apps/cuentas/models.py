from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

# Create your models here.

class UserAccountManager(BaseUserManager):
    def create_user(self , email , password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
          
        user = self.model(
            email = self.normalize_email(email) , 
        )
        
        user.set_password(password)
        user.save(using = self._db)
        return user
      
    def create_superuser(self , email , password):
        user = self.create_user(
            email = self.normalize_email(email) , 
            password = password
        )
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.es_clienteInterno = True
        user.save(using = self._db)
        return user
      
class UserAccount(AbstractBaseUser, PermissionsMixin):
    class Types(models.TextChoices):
        LOCAL_TRADER = "LOCAL TRADER" , "local trader"
        INTERNATIONAL_TRADER = "INTERNATIONAL TRADER" , "INTERNATIONAL TRADER"
        CONSULTANT = "CONSULTANR","consultant"
        PRODUCER = "PRODUCER", "producer"
        CARRIER = "CARRIER","carrier"
        ADMINISTRATOR = "ADMINISTRATOR", "administrator"


        
          
    type = models.CharField(max_length = 30 , choices = Types.choices , 
                            # Default is user is teacher
                            default = Types.LOCAL_TRADER)
    email = models.EmailField(max_length = 200 , unique = True)

    """
    Las siguientes variables pertenecen a django, por eso utilizan snake_case 
    
    """
    is_active = models.BooleanField(default = False)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    last_login = models.DateTimeField(null= True, blank = True)
    date_joined = models.DateTimeField(auto_now_add=True)

     
    #####
    ##### Las siguientes variables no se utilizaron nunca, así que las comenté -dotMamu
    #####

    # esClienteInterno = models.BooleanField(default = False)

    # esComercianteExtranjero = models.BooleanField(default = False)
    # esComercianteLocal = models.BooleanField(default = False)
    # esConsultor = models.BooleanField(default = False)
    # esProductor = models.BooleanField(default = False)
    # esTransportista = models.BooleanField(default = False)

    firstName = models.CharField(max_length= 100)
    lastName = models.CharField(max_length= 100)
    address = models.CharField(max_length= 100)
    phone = models.CharField(max_length= 100)
       
    USERNAME_FIELD = "email"
      
    # defining the manager for the UserAccount model
    objects = UserAccountManager()
      
    def __str__(self):
        return str(self.email)
      
    def has_perm(self , perm, obj = None):
        return self.is_admin
      
    def has_module_perms(self , app_label):
        return True
      
    def save(self , *args , **kwargs):
        if not self.type or self.type == None : 
            self.type = UserAccount.Types.EXTERNO
        return super().save(*args , **kwargs)

class InternationalTrader(UserAccount):
    
    businessName = models.CharField( max_length=50, unique=True)
    country = models.CharField(max_length=255)


    def save(self , *args , **kwargs):
        
        self.type = UserAccount.Types.INTERNATIONAL_TRADER
        self.is_staff = False
        return super().save(*args , **kwargs)
    

    def __str__(self):
        return f"{self.businessName} represented by {self.firstName} {self.lastName}"

class LocalTrader(UserAccount):

    documentNumber = models.CharField(max_length=255, blank=True)
    businessName = models.CharField( max_length=50, unique=True)
    rut = models.CharField(max_length=255, blank=True)
    

    def __str__(self):
        return str(self.firstName)

    def save(self , *args , **kwargs):

        self.type = UserAccount.Types.LOCAL_TRADER
        self.is_staff = False
        return super().save(*args , **kwargs)


class Producer(UserAccount):
    
    documentNumber = models.CharField(max_length=255, blank=True)
    businessName = models.CharField( max_length=50, unique=True)
    rut = models.CharField(max_length=255, blank=True)
    productType = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.firstName)

    def save(self , *args , **kwargs):

        self.type = UserAccount.Types.PRODUCER
        self.is_staff = False 
        return super().save(*args , **kwargs)



class Carrier(UserAccount):
    businessName = models.CharField( max_length=50, unique=True)
    documentNumber = models.CharField(max_length=255, blank=True)
    rut = models.CharField(max_length=255, blank=True)
    



    def __str__(self):
        return str(self.firstName)

    def save(self , *args , **kwargs):

        self.type = UserAccount.Types.CARRIER
        self.is_staff = False
        return super().save(*args , **kwargs)


class Consultant(UserAccount):

    
    

    def __str__(self):
        return str(self.firstName)

    def save(self , *args , **kwargs):

        self.type = UserAccount.Types.CONSULTANT
        self.is_active= True
        self.is_staff = True
        self.has_perm('cuentas.view_consultor')
        return super().save(*args , **kwargs)

class Administrator(UserAccount):

    

    def __str__(self):
        return str(self.firstName)

    def save(self , *args , **kwargs):

        self.type = UserAccount.Types.ADMINISTRADOR
        self.is_staff = True
        self.is_active = True
        self.is_admin = True
        return super().save(*args , **kwargs)


@receiver(post_save)
def afterCreateMail(sender, instance=None, created= False, **kwargs):
    if sender.__name__ in ("InternationalTrader","LocalTrader","Producer","Carrier"):
        if created:
            print(instance.email)

            subject = f"Welcome {instance.firstName} {instance.lastName} to Maipo Grande"
            message = f"Dear Mr/Ms {instance.firstName} {instance.lastName}:\nAt Maipo Grande, we are very pleased to have you on board.\nIn the next few hours one of our executives will contact you."
            lista = []
            lista.append(instance.email)
            send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=lista)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "feriaMaipoGrande@gmail.com",
        # to:
        [reset_password_token.user.email]
    )