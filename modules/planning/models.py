from django.db import models
from ..app.models import TablasConfiguracion


class Perfil(models.Model):
    idperfil = models.SmallAutoField(primary_key=True)
    deescripcion = models.TextField()
    desc_corta = models.TextField()
    fk_rama = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, default=None, null=True)


class CompetenciasReq(models.Model):
    idcompetenciasreq = models.AutoField(primary_key=True)
    desc_competencia = models.TextField()
    fk_perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, default=None, null=True)
    fk_tipo_competencia = models.ForeignKey(TablasConfiguracion, on_delete=models.CASCADE, default=None, null=True)
    fk_nivel = models.ForeignKey(TablasConfiguracion, related_name='competencias_nivel', on_delete=models.CASCADE, default=None, null=True)