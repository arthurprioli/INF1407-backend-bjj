from django.db import models


class BJJPos(models.Model):
    id = models.AutoField(primary_key=True)
    nome_pt = models.TextField(db_column="nome_pt")
    nome_en = models.TextField(db_column="nome_en")
    categoria = models.TextField(db_column="categoria")
    dificuldade = models.TextField(db_column="dificuldade")
    descricao = models.TextField(db_column="descricao")
    observacoes = models.TextField(db_column="observacoes")

    class Meta:
        managed = True
        db_table = "posicoes"
        ordering = ["id"]

    def __str__(self):
        return self.nome_pt
