from django.db import models
from django.core.validators import MinValueValidator


class ArbInst(models.Model):
    arb_inst = models.CharField(max_length=64)

    def __str__(self):
        return self.arb_inst


class ArbInstRu(models.Model):
    arb_inst = models.CharField(max_length=64)

    def __str__(self):
        return self.arb_inst


class UserRequest(models.Model):

    ARBS = ((1, '1'), (3, '3'),)

    PARTIES = ((2, '2'), (3, '3'), (4, '4'),)

    PROC = (
        ('Standard', 'Standard'),
        ('Expedited', 'Expedited'),
    )

    EMERGENCY = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    amount = models.FloatField(validators=[MinValueValidator(1)])
    arbs = models.IntegerField(choices=ARBS, default=3)
    proc = models.CharField(max_length=16, choices=PROC, default='Standard')
    ai = models.ManyToManyField(ArbInst)
    ea = models.CharField(max_length=8, choices=EMERGENCY, default='No')
    parties = models.IntegerField(choices=PARTIES, default=2)

    def __str__(self):
        return f'Request N{self.id} for {self.amount}'


class UserRequestRu(models.Model):
    ARBS = ((1, '1'), (3, '3'),)
    TYPE_RU = (
        ('Внутренний', 'Внутренний'),
        ('Корпоративный', 'Корпоративный')
    )
    PROC_RU = (
        ('Стандартная', 'Стандартная'),
        ('Ускоренная', 'Ускоренная'),
    )

    amount = models.FloatField(validators=[MinValueValidator(1)])
    arbs = models.IntegerField(choices=ARBS, default=3)
    ai = models.ManyToManyField(ArbInstRu)
    proc = models.CharField(
        max_length=16, choices=PROC_RU, default='Стандартная')
    type = models.CharField(
        max_length=16, choices=TYPE_RU, default='Внутренний')

    def __str__(self):
        return f'Request N{self.id} for {self.amount}'


class Cost(models.Model):

    ai = models.ForeignKey(ArbInst, on_delete=models.CASCADE)
    req = models.ForeignKey(
        UserRequest, on_delete=models.CASCADE, related_name='costs')

    reg_fee = models.FloatField(null=True, blank=True)
    arb_fee = models.FloatField(null=True, blank=True)
    arbs_fee = models.FloatField(null=True, blank=True)
    admin_fee = models.FloatField(null=True, blank=True)
    ea_fee = models.FloatField(null=True, blank=True)

    comment0 = models.TextField(null=True, blank=True)
    comment1 = models.TextField(null=True, blank=True)
    comment2 = models.TextField(null=True, blank=True)


class CostRu(models.Model):
    ai = models.ForeignKey(ArbInstRu, on_delete=models.CASCADE)
    req = models.ForeignKey(
        UserRequestRu, on_delete=models.CASCADE, related_name='costs')

    reg_fee = models.FloatField(null=True, blank=True)
    arb_fee = models.FloatField(null=True, blank=True)
    arbs_fee = models.FloatField(null=True, blank=True)
    admin_fee = models.FloatField(null=True, blank=True)

    comment0 = models.TextField(null=True, blank=True)
    comment1 = models.TextField(null=True, blank=True)
    comment2 = models.TextField(null=True, blank=True)


class Rate(models.Model):

    name = models.CharField(max_length=16)
    rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name
