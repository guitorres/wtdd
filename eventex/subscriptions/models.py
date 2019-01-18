from django.db import models

def _create_hash():
    from uuid import uuid4
    return uuid4().hex


class Subscription(models.Model):
    name = models.CharField('nome', max_length=100)
    cpf = models.CharField('cpf', max_length=11)
    email = models.EmailField('e-mail')
    phone = models.CharField('telefone', max_length=20)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    _hash = models.CharField('_hash', max_length=32, default=_create_hash, unique=True)
    paid = models.BooleanField('pago', default=False)

    class Meta:
        verbose_name_plural = 'inscrições'
        verbose_name = 'inscrição'
        ordering = ['-created_at']

    def __str__(self):
        return self.name