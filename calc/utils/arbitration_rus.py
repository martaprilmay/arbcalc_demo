def rima_ru(amount, arbs, proc, type):
    pass


def rspp_ru(amount, arbs, proc, type):
    pass


def icac_ru(amount, arbs, proc, type):
    pass


def ai_chooser(req, ais, amount, arbs, proc, parties, measures):

    result = []

    for ai in ais:
        if ai.id == 1:
            res = rima_ru(amount, arbs, proc, measures)
            obj = Cost(ai=ai, req=req)
            obj.reg_fee = res['reg_fee']
            obj.arb_fee = res['arb_fee']
            obj.arbs_fee = res['arbs_fee']
            obj.admin_fee = res['admin_fee']
            obj.comment1 = res['comment1']
            if 'comment0' in res:
                obj.comment0 = res['comment0']
            obj.save()
            result.append(obj)
        if ai.id == 2:
            res = hkiac(amount, arbs, proc, parties, measures)
            obj = Cost(ai=ai, req=req)
            obj.reg_fee = res['reg_fee']
            obj.arb_fee = res['arb_fee']
            obj.arbs_fee = res['arbs_fee']
            obj.admin_fee = res['admin_fee']
            obj.comment1 = res['comment1']
            if 'comment0' in res:
                obj.comment0 = res['comment0']
            obj.save()
            result.append(obj)
        if ai.id == 3:
            res = siac(amount, arbs, proc, parties, measures)
            obj = Cost(ai=ai, req=req)
            obj.reg_fee = res['reg_fee']
            obj.arb_fee = res['arb_fee']
            obj.arbs_fee = res['arbs_fee']
            obj.admin_fee = res['admin_fee']
            obj.comment1 = res['comment1']
            if 'comment0' in res:
                obj.comment0 = res['comment0']
            obj.save()
            result.append(obj)
