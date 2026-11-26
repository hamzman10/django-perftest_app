from django.db import models
from django.db import models


class RefTypeTest(models.Model):
    id_type_test = models.BigAutoField(primary_key=True)
    code_type = models.CharField(max_length=30, unique=True)
    libelle = models.CharField(max_length=100)
    description = models.TextField()
    objectif = models.TextField()
    duree_secondes = models.IntegerField()
    nb_threads = models.IntegerField()
    ramp_up = models.IntegerField()
    think_time = models.IntegerField(blank=True, null=True)
    volume_donnees = models.IntegerField(blank=True, null=True)
    actif = models.BooleanField(blank=True, null=True)
    nb_threads_max = models.IntegerField(blank=True, null=True)
    nb_threads_initial = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ref_type_test'

    def __str__(self):
        return self.libelle


class RefEnvironnement(models.Model):
    id_envir = models.AutoField(primary_key=True)
    desingnation_env = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'ref_environnement'

    def __str__(self):
        return self.desingnation_env


class RefOutilTest(models.Model):
    id_outilt = models.AutoField(primary_key=True)
    desingnation_outilt = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'ref_outil_test'

    def __str__(self):
        return self.desingnation_outilt


class RefProtocole(models.Model):
    id_protocol = models.AutoField(primary_key=True)
    desingnation_protocol = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'ref_protocole'

    def __str__(self):
        return self.desingnation_protocol


class RefStatutTest(models.Model):
    id_statust = models.AutoField(primary_key=True)
    desingnation_statust = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'ref_statut_test'

    def __str__(self):
        return self.desingnation_statust