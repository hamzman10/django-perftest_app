from django.db import models


class Scenario(models.Model):

    id_scenario = models.BigAutoField(primary_key=True)

    name_scenario = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    objectif = models.TextField(blank=True, null=True)

    # Identifiants des tables de référence
    id_project = models.BigIntegerField()
    id_user = models.BigIntegerField()
    id_type_test = models.BigIntegerField()
    id_envir = models.IntegerField()
    id_outilt = models.IntegerField()
    id_protocol = models.IntegerField()

    # Paramètres de charge
    duree_secondes = models.IntegerField()
    nb_threads = models.IntegerField()
    ramp_up = models.IntegerField()
    think_time = models.IntegerField()

    nb_threads_initial = models.IntegerField(
        blank=True, null=True
    )
    nb_threads_max = models.IntegerField(
        blank=True, null=True
    )
    step_threads = models.IntegerField(
        blank=True, null=True
    )
    step_duration_seconds = models.IntegerField(
        blank=True, null=True
    )

    volume_donnees = models.BigIntegerField(
        blank=True, null=True
    )

    seuils_performance = models.JSONField(
        blank=True, null=True
    )

    actif = models.BooleanField()

    date_creation = models.DateTimeField()
    date_modification = models.DateTimeField(
        blank=True, null=True
    )

    # Configuration HTTP historique
    url_endpoint = models.TextField(
        blank=True, null=True
    )
    headers = models.JSONField(
        blank=True, null=True
    )
    params_url = models.JSONField(
        blank=True, null=True
    )
    body = models.JSONField(
        blank=True, null=True
    )

    nb_repetitions = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'scenario'

    def __str__(self):
        return self.name_scenario
