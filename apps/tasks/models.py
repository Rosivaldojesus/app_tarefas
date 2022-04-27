from tabnanny import verbose
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nome')
    description = models.TextField(blank=True, null=True, verbose_name='Descrição')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural ='categorias'
        ordering = ['id']

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('B', 'Baixa'),
        ('M', 'Média'),
        ('A', 'Alta'),
    )
    STATUS_CHOICES = (
        ('EX', 'Em execução'),
        ( 'PD', 'Pendente'),
        ('CD', 'Concluída'),
    )
    name = models.CharField('Tarefa',max_length=255, blank=True, null=True)
    description = models.TextField('Descrição', blank=True, null=True)
    end_date = models.DateField('Data final', auto_now=False, auto_now_add=False, blank=True, null=True)
    prioritary = models.CharField('Prioridade', max_length=1, choices=PRIORITY_CHOICES)
    category = models.ManyToManyField(Category)
    status = models.CharField('status', max_length=2, choices=STATUS_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        ordering =['id']


    def __str__(self):
        return self.name
