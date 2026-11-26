

from django.db import models


# =====================================================
# TABLE : scenario_request
# Configuration de la requête HTTP d'un scénario
# =====================================================

class ScenarioRequest(models.Model):

    id_request = models.BigAutoField(primary_key=True)

    id_scenario = models.BigIntegerField()

    url_cible = models.TextField()

    methode_http = models.CharField(max_length=50)

    content_type = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    headers = models.JSONField(
        blank=True,
        null=True
    )

    parametres = models.JSONField(
        blank=True,
        null=True
    )

    body = models.TextField(
        blank=True,
        null=True
    )

    auth_type = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    auth_config = models.JSONField(
        blank=True,
        null=True
    )

    date_creation = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'scenario_request'

    def __str__(self):
        return f"Requête du scénario {self.id_scenario}"


# =====================================================
# TABLE : scenario_execute
# Historique des exécutions des scénarios
# =====================================================

class ScenarioExecute(models.Model):

    id_execution = models.BigAutoField(primary_key=True)

    id_scenario = models.BigIntegerField()

    date_execution = models.DateTimeField(
        blank=True,
        null=True
    )

    statut_execution = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    moteur_execution = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    url_cible = models.TextField(
        blank=True,
        null=True
    )

    methode_http = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    headers_request = models.JSONField(
        blank=True,
        null=True
    )

    body_request = models.TextField(
        blank=True,
        null=True
    )

    params_request = models.JSONField(
        blank=True,
        null=True
    )

    status_http = models.IntegerField(
        blank=True,
        null=True
    )

    temps_reponse_ms = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        blank=True,
        null=True
    )

    headers_response = models.JSONField(
        blank=True,
        null=True
    )

    body_response = models.TextField(
        blank=True,
        null=True
    )

    config_charge = models.JSONField(
        blank=True,
        null=True
    )

    resultat_k6 = models.JSONField(
        blank=True,
        null=True
    )

    erreur = models.TextField(
        blank=True,
        null=True
    )

    date_fin = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'scenario_execute'

    def __str__(self):
        return f"Exécution {self.id_execution} - Scénario {self.id_scenario}"
