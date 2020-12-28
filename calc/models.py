from django.db import models
from django.core.validators import MinValueValidator


class ArbInst(models.Model):
    """ International Arbitral Institutions """
    arb_inst = models.CharField(max_length=64)

    def __str__(self):
        return self.arb_inst


class ArbInstRu(models.Model):
    """ Russian Arbitral Institutions """
    arb_inst = models.CharField(max_length=64)

    def __str__(self):
        return self.arb_inst


class UserRequest(models.Model):
    """ International arbitration - parameters of a dispute """

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
    """ Russian domestic arbitration - parameters of a dispute """

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
    """ Results (all fees and comments) calculated based upon dispute parameters
        from a corresponding a UserRequest object. One Cost object per Arbitral
        institution in UserRequest object. A queryset of Cost objects for a
        UserRequest object can be accessed via related name 'costs'
    """

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

    def __str__(self):
        return f'Request N {self.req.id} ({self.req.amount}) - {self.ai.arb_inst}'


class CostRu(models.Model):
    """ Results (all fees and comments) calculated based upon dispute parameters
        from a corresponding a UserRequestRu object. One CostRu object per Arbitral
        institution in UserRequestRu object. A queryset of CostRu objects for a
        UserRequestRu object can be accessed via related name 'costs'
    """
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

    def __str__(self):
        return f'Request N {self.req.id} ({self.req.amount}) - {self.ai.arb_inst}'


class Rate(models.Model):
    """ Exchange rates """
    name = models.CharField(max_length=16)
    rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name
