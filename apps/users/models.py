from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import Permission,Group
from django.contrib.contenttypes.models import ContentType   

class Rol(models.Model):
    """Model definition for Rol."""

    # TODO: Define fields here
    id = models.AutoField(primary_key = True)
    rol = models.CharField('Rol', max_length=50,unique = True)

    class Meta:
        """Meta definition for Rol."""

        verbose_name = 'Rol'
        verbose_name_plural = 'Rols'

    def __str__(self):
        """Unicode representation of Rol."""
        return self.rol
    
    def save(self,*args,**kwargs):
        permisos_defecto = ['add','change','delete','view']
        if not self.id:
            nuevo_grupo,creado = Group.objects.get_or_create(name = f'{self.rol}')
            for permiso_temp in permisos_defecto:
                permiso,created = Permission.objects.update_or_create(
                    name = f'Can {permiso_temp} {self.rol}',
                    content_type = ContentType.objects.get_for_model(Rol),
                    codename = f'{permiso_temp}_{self.rol}'
                )
                if creado:
                    nuevo_grupo.permissions.add(permiso.id)
            super().save(*args,**kwargs)
        else:
            rol_antiguo = Rol.objects.filter(id = self.id).values('rol').first()
            if rol_antiguo['rol'] == self.rol:
                super().save(*args,**kwargs)
            else:
                Group.objects.filter(name = rol_antiguo['rol']).update(name = f'{self.rol}')
                for permiso_temp in permisos_defecto:
                    Permission.objects.filter(codename = f"{permiso_temp}_{rol_antiguo['rol']}").update(
                        codename = f'{permiso_temp}_{self.rol}',
                        name = f'Can {permiso_temp} {self.rol}'
                    )
                super().save(*args,**kwargs)



#create user in cli
class UserManager(auth_models.BaseUserManager):
    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str = None,
        is_staff=False,
        is_superuser=False,
    ) -> "User":
        if not email:
            raise ValueError("User must have an email")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        return user

    def create_superuser(
        self, first_name: str, last_name: str, email: str, password: str, is_staff: bool, is_superuser: bool
    ) -> "User":
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )
        user.save()

        return user


class User(auth_models.AbstractUser):
    first_name = models.CharField(verbose_name="First Name", max_length=255)
    last_name = models.CharField(verbose_name="Last Name", max_length=255)
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    password = models.CharField(max_length=255)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE,blank = True,null = True)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    username = None

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name","rol"]

    class Meta:
        permissions = [('permiso_desde_codigo','Este es un permiso creado desde código'),
                        ('segundo_permiso_codigo','Segundo permiso creado desde codigo')]

    def __str__(self):
        return f'{self.first_name},{self.last_name}'


    def save(self,*args,**kwargs):
        if not self.id:
            super().save(*args,**kwargs)
            if self.rol is not None:
                grupo = Group.objects.filter(name = self.rol.rol).first()
                if grupo:
                    self.groups.add(grupo)
                super().save(*args,**kwargs)
        else:
            if self.rol is not None:
                grupo_antiguo = User.objects.filter(id = self.id).values('rol__rol').first()
                if grupo_antiguo['rol__rol'] == self.rol.rol:
                    print("Entro en igualdad de roles")
                    super().save(*args,**kwargs)
                else:
                    grupo_anterior = Group.objects.filter(name = grupo_antiguo['rol__rol']).first()                    
                    if grupo_anterior:
                        print(grupo_anterior)
                        self.groups.remove(grupo_anterior)
                    nuevo_grupo = Group.objects.filter(name = self.rol.rol).first()
                    if nuevo_grupo:
                        self.groups.add(nuevo_grupo)
                    super().save(*args,**kwargs)