from django.db import models


class Projects(models.Model):
    id_project = models.BigAutoField(primary_key=True)
    name_pr = models.CharField(max_length=100)
    description_pr = models.CharField(
        unique=True,
        max_length=255
    )
    base_url = models.CharField(max_length=100)
    created_at_p = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'projects'

    def __str__(self):
        return self.name_pr