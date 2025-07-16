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


class CostCenter(models.Model):
    class Meta:
        managed = False
        icon = "building-office-2"
        codename_plural = "cost_center"


class Period(models.Model):
    class Meta:
        managed = False
        icon = "calendar-date-range"
        codename_plural = "periods"


class Compensation(models.Model):
    class Meta:
        managed = False
        icon = "banknotes"
        codename_plural = "compensations"
