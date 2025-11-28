from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[('estudante', 'Estudante'), ('admin', 'Admin')], default='estudante')

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class PosicaoAprendida(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="aprendidas")
    posicao_id = models.IntegerField()
    data_aprendizado = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'posicao_id')
        verbose_name = "Posição Aprendida"
        verbose_name_plural = "Posições Aprendidas"

    def __str__(self):
        return f"{self.user.username} aprendeu posição {self.posicao_id}"
    
    