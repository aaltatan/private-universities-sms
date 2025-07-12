from django.db import models


class Ledger(models.Model):
    class Meta:
        managed = False
        codename_plural = "ledger"


class TrialBalance(models.Model):
    class Meta:
        managed = False
        icon = "scale"
        codename_plural = "trial_balance"
