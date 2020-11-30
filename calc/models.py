from django.db import models
from django.core.validators import MinValueValidator


class ArbInst(models.Model):
    arb_inst = models.CharField(max_length=64)

    def __str__(self):
        return self.arb_inst


class UserRequest(models.Model):

    ARBS = ((1, '1'), (3, '3'),)

    PARTIES = ((1, '1'), (2, '2'), (3, '3'), (4, '4'),)

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


class Cost(models.Model):

    ai = models.ForeignKey(ArbInst, on_delete=models.CASCADE)
    req = models.ForeignKey(
        UserRequest, on_delete=models.CASCADE, related_name='costs')

    reg_fee = models.FloatField(null=True, blank=True)
    arb_fee = models.FloatField(null=True, blank=True)
    arbs_fee = models.FloatField(null=True, blank=True)
    admin_fee = models.FloatField(null=True, blank=True)
    em_fee = models.FloatField(null=True, blank=True)

    min_arbs_fee = models.FloatField(null=True, blank=True)
    med_arbs_fee = models.FloatField(null=True, blank=True)
    max_arbs_fee = models.FloatField(null=True, blank=True)

    comment0 = models.TextField(null=True, blank=True)
    comment1 = models.TextField(null=True, blank=True)
    comment2 = models.TextField(null=True, blank=True)
    comment3 = models.TextField(null=True, blank=True)


class Rate(models.Model):

    name = models.CharField(max_length=16)
    rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


    # def calculate(self, req):
    #     ais = req.ai.all()
    #     amount = req.amount
    #     arbs = req.arbs
    #     proc = req.proc
    #
    #     def ai_chooser(req, ais, amount, arbs, proc):
    #         for ai in ais:
    #             if ai.id == 1:
    #                 res = rac_at_rima(amount, arbs, proc)
    #                 obj = Cost(ai=ai, req=req)
    #                 print('new object')
    #                 obj.reg_fee = res['reg_fee']
    #                 obj.arb_fee = res['arb_fee']
    #                 obj.arbs_fee = res['arbs_fee']
    #                 obj.admin_fee = res['admin_fee']
    #                 obj.comment1 = res['comment1']
    #                 if res['comment0']:
    #                     obj.comment0 = res['comment0']
    #                 obj.save()
    #             elif ai.id == 2:
    #                 obj = Cost(ai=ai, req=req)
    #                 obj.reg_fee = 0
    #                 obj.arb_fee = 0
    #                 obj.arbs_fee = 0
    #                 obj.admin_fee = 0
    #             elif ai.id == 3:
    #                 obj = Cost(ai=ai, req=req)
    #                 obj.reg_fee = 0
    #                 obj.arb_fee = 0
    #                 obj.arbs_fee = 0
    #                 obj.admin_fee = 0
    #             elif ai.id == 4:
    #                 obj = Cost(ai=ai, req=req)
    #                 obj.reg_fee = 0
    #                 obj.arb_fee = 0
    #                 obj.arbs_fee = 0
    #                 obj.admin_fee = 0
    #             elif ai.id == 5:
    #                 obj = Cost(ai=ai, req=req)
    #                 obj.reg_fee = 0
    #                 obj.arb_fee = 0
    #                 obj.arbs_fee = 0
    #                 obj.admin_fee = 0
    #             elif ai.id == 6:
    #                 obj = Cost(ai=ai, req=req)
    #                 obj.reg_fee = 0
    #                 obj.arb_fee = 0
    #                 obj.arbs_fee = 0
    #                 obj.admin_fee = 0
    #             elif ai.id == 7:
    #                 obj = Cost(ai=ai, req=req)
    #                 obj.reg_fee = 0
    #                 obj.arb_fee = 0
    #                 obj.arbs_fee = 0
    #                 obj.admin_fee = 0
    #             elif ai.id == 8:
    #                 obj = Cost(ai=ai, req=req)
    #                 obj.reg_fee = 0
    #                 obj.arb_fee = 0
    #                 obj.arbs_fee = 0
    #                 obj.admin_fee = 0
    #             elif ai.id == 9:
    #                 obj = Cost(ai=ai, req=req)
    #                 obj.reg_fee = 0
    #                 obj.arb_fee = 0
    #                 obj.arbs_fee = 0
    #                 obj.admin_fee = 0
    #             elif ai.id == 10:
    #                 obj = Cost(ai=ai, req=req)
    #                 obj.reg_fee = 0
    #                 obj.arb_fee = 0
    #                 obj.arbs_fee = 0
    #                 obj.admin_fee = 0
    #             elif ai.id == 11:
    #                 obj = Cost(ai=ai, req=req)
    #                 obj.reg_fee = 0
    #                 obj.arb_fee = 0
    #                 obj.arbs_fee = 0
    #                 obj.admin_fee = 0
    #             elif ai.id == 12:
    #                 obj = Cost(ai=ai, req=req)
    #                 obj.reg_fee = 0
    #                 obj.arb_fee = 0
    #                 obj.arbs_fee = 0
    #                 obj.admin_fee = 0
    #     return ai_chooser(req, ais, amount, arbs, proc)



# class AbitrationCost(models.Model):
#     request = models.OneToOneField(
#         UserRequest, null=True, on_delete=models.CASCADE
#     )
#     cost = models.ForeignKey(
#         Cost, null=True, on_delete=models.CASCADE
#     )
#
#     def calculate(self):
#         pass


# class Arbitration(models.Model):
    # num_of_arbs = models.IntegerField()
    # type_of_proc = models.CharField(max_length=200)
    # arb_inst = models.CharField(max_length=200)
