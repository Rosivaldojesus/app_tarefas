from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

# Create your models here.

class UserProfile(models.Model):
    photo = models.ImageField('Foto', upload_to='photos')
    cell_phone = models.CharField('Celular', max_length=16)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')

    class Meta:
        verbose_name = 'Perfil do usuário'
        verbose_name_plural = 'Perfis dos usuários'

    def __str__(self) -> str:
        return self.user.username

    def clean(self):
        model = self.__class__
        if model.objects.count() > 0 and self.id != model.get().id:
            raise ValidationError("Você já tem um perfil cadastrado.")
