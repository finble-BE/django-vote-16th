from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, id, team, email, part, name, password, **extra_fields):
        if not id:
            raise ValueError('Users must have an id')
        if not team:
            raise ValueError('Users require a team')
        if not email:
            raise ValueError('Users require an email')
        if not part:
            raise ValueError('Users require a part')
        if not name:
            raise ValueError('Users require a name')
        email = self.normalize_email(email)
        user = self.model(self, id=id, team=team, email=email, part=part, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, id, team, email, part, name, password=None, **extra_fields):
        return self._create_user(self, id, team, email, part, name, password, **extra_fields)

    # def create_superuser(self, id, team, email, part, name, password):
    #     user = self.create_user(
    #         id=id,
    #         team=team,
    #         email=email,
    #         part=part,
    #         name=name,
    #         password=password
    #     )
    #     user.is_admin = True
    #     user.save(using=self._db)
    #     return user


class Team(models.Model):
    name = models.CharField(max_length=20)
    vote_num = models.IntegerField(default=0)


class User(AbstractBaseUser):
    PART_CHOICES = {
        ('front', 'Front-end'),
        ('back', 'Back-end'),
    }
    id = models.CharField(max_length=10, primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    email = models.EmailField(max_length=30, unique=True)
    part = models.CharField(max_length=10, choices=PART_CHOICES)
    name = models.CharField(max_length=10)
    part_voted = models.BooleanField(default=False)
    demo_voted = models.BooleanField(default=False)
    vote_num = models.IntegerField(default=0)

    objects = UserManager()
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['team', 'email', 'part', 'name', ]
