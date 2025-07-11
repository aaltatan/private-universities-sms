from django.db import models


class ReportPermission(models.Model):
    class Meta:
        managed = False
        permissions = (
            ("view_ledger", "Can view ledger report"),
            ("view_trialbalance", "Can view trial balance report"),
        )
