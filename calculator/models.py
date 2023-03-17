from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name = '', last_name= '', password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name = '', last_name = '', password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, first_name, last_name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=100)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Operation(models.Model):
    TYPE_CHOICES = (
        ('addition', 'Addition'),
        ('subtraction', 'Subtraction'),
        ('multiplication', 'Multiplication'),
        ('division', 'Division'),
        ('square_root', 'Square Root'),
        ('random_string', 'Random String'),
    )

    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.type == 'addition' or self.type == 'subtraction' or self.type == 'multiplication' or self.type == 'division':
            self.cost = 10
        elif self.type == 'square_root':
            self.cost = 20
        elif self.type == 'random_string':
            self.cost = 25

        super(Operation, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']

class Record(models.Model):
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user_balance = models.DecimalField(max_digits=10, decimal_places=2)
    operation_response = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.deleted = True
        self.save()

    def undelete(self):
        self.deleted = False
        self.save()

    def save(self, *args, **kwargs):
        if self.pk is None:  # Only update amount, user_balance and user credit if the record is being created, not updated
            self.amount = self.operation.cost
            self.user.credit -= self.amount
            self.user.save()
            self.user_balance = self.user.credit
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['date']
