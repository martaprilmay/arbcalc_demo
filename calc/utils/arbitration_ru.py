from calc.models import CostRu, Rate


def rima_ru(amount, arbs, proc, type):
    """ Calculates fees for domestic arbitration in the Russian Arbitration
        Center at the Russian Institute of Modern Arbitration
    """
    comment0 = ''

    if type == 'Корпоративный':

        reg_fee = 40000.0
        comment1 = (
            "Сумма регистрационного сбора включена в сумму арбитражного сбора."
        )

        if proc == 'Ускоренная':
            comment0 += (
                'Ускоренная процедура возможна только в арбитраже внутренних с'
                'поров. Результаты для стандартной процедуры.'
            )

        if arbs == 1:
            if comment0:
                comment0 += '\n'
            comment0 += (
                'Корпоративный спор разрешается составом арбитража из трех арб'
                'итров. Результаты для трех арбитров.'
            )
            arbs = 3

        if amount <= 500000:
            admin_fee = 70000.00
            arbs_fee = 100000.00
        elif 500000 < amount <= 1500000:
            admin_fee = 70000.00 + (amount - 500000) * 0.01
            arbs_fee = 100000.00 + (amount - 500000) * 0.035
        elif 1500000 < amount <= 5000000:
            admin_fee = 100000.00 + (amount - 1500000) * 0.003
            arbs_fee = 1700000.00 + (amount - 1500000) * 0.015
        elif 5000000 < amount <= 10000000:
            admin_fee = 187500.00 + (amount - 5000000) * 0.004
            arbs_fee = 380000.00 + (amount - 5000000) * 0.005
        elif 10000000 < amount <= 20000000:
            admin_fee = 287500.00 + (amount - 10000000) * 0.007
            arbs_fee = 630000.00 + (amount - 10000000) * 0.012
        elif 20000000 < amount <= 30000000:
            admin_fee = 387500.00 + (amount - 20000000) * 0.007
            arbs_fee = 980000.00 + (amount - 20000000) * 0.005
        elif 30000000 < amount <= 50000000:
            admin_fee = 437500.00 + (amount - 30000000) * 0.005
            arbs_fee = 1230000.00 + (amount - 30000000) * 0.01
        elif 50000000 < amount <= 100000000:
            admin_fee = 487500.00 + (amount - 50000000) * 0.003
            arbs_fee = 1530000.00 + (amount - 50000000) * 0.01
        elif 100000000 < amount <= 500000000:
            admin_fee = 562500.00 + (amount - 100000000) * 0.0007
            arbs_fee = 2030000.00 + (amount - 100000000) * 0.003
        elif amount >= 500000000:
            admin_fee = 7625000.00 + (amount - 500000000) * 0.0001
            arbs_fee = 3030000.00 + (amount - 500000000) * 0.0015

    if type == 'Внутренний':

        reg_fee = 20000.0
        comment1 = (
            "Сумма регистрационного сбора включена в сумму арбитражного сбора."
        )

        # limitations on Expedited procedure
        if proc == 'Ускоренная' and amount >= 30000000:
            comment0 += (
                'Усколренная процедура применима только к спорам, где сумма тр'
                'ебований не превышает 30 000 000 рублей. Результаты для станд'
                'артной процедуры.'
            )
            proc = 'Стандартная'

        if proc == 'Ускоренная' and arbs == 3:
            if comment0:
                comment0 += '\n'
            comment0 += (
                'В ускоренной процедуре спор разрешается единоличным арбитром.'
                ' Результаты для единоличного арбитра.'
            )
            arbs = 1

        # calculating admin and arbs fee (sole arb before 500 000, then 3 arbs)
        # standard procedure
        if amount <= 500000:
            admin_fee = 17500.00
            arbs_fee = 42500.00
        elif 500000 < amount <= 1500000:
            admin_fee = 17500.00 + (amount - 500000) * 0.01
            arbs_fee = 42500.00 + (amount - 500000) * 0.035
        elif 1500000 < amount <= 5000000:
            admin_fee = 22500.00 + (amount - 1500000) * 0.003
            arbs_fee = 77500.00 + (amount - 1500000) * 0.015
        elif 5000000 < amount <= 10000000:
            admin_fee = 38000.00 + (amount - 5000000) * 0.004
            arbs_fee = 13000.00 + (amount - 5000000) * 0.005
        elif 10000000 < amount <= 20000000:
            admin_fee = 58000.00 + (amount - 10000000) * 0.007
            arbs_fee = 155000.00 + (amount - 10000000) * 0.012
        elif 20000000 < amount <= 29999999:
            admin_fee = 128000.00 + (amount - 20000000) * 0.007
            arbs_fee = 275000.00 + (amount - 20000000) * 0.005
        elif 30000000 <= amount <= 50000000:
            admin_fee = 250000.00 + (amount - 30000000) * 0.005
            arbs_fee = 650000.00 + (amount - 30000000) * 0.01
        elif 50000000 < amount <= 100000000:
            admin_fee = 350000.00 + (amount - 50000000) * 0.003
            arbs_fee = 900000.00 + (amount - 50000000) * 0.01
        elif 100000000 < amount <= 500000000:
            admin_fee = 500000.00 + (amount - 100000000) * 0.0007
            arbs_fee = 1400000.00 + (amount - 100000000) * 0.003
        elif 500000000 < amount <= 1000000000:
            admin_fee = 780000.00 + (amount - 500000000) * 0.0001
            arbs_fee = 2600000.00 + (amount - 500000000) * 0.0015
        elif 1000000000 < amount <= 4999999999:
            admin_fee = 830000.00 + (amount - 1000000000) * 0.0001
            arbs_fee = 3350000.00 + (amount - 1000000000) * 0.0013
        elif amount >= 5000000000:
            admin_fee = 1250000.0
            arbs_fee = 8750000.0

        # adjustments in Expedited proc
        if proc == 'Ускоренная':
            if amount < 500000:
                admin_fee *= 0.5
                arbs_fee *= 0.75

        if arbs == 1:
            if amount >= 30000000:
                arbs_fee *= 0.8

        if arbs == 3:
            if amount < 300000000:
                arbs_fee *= 1.2

    arb_fee = admin_fee + arbs_fee

    # formatting results
    admin_fee = round(admin_fee, 2)
    arbs_fee = round(arbs_fee, 2)
    arb_fee = round(arb_fee, 2)

    # saving results in a dict
    result = {
        'reg_fee': reg_fee,
        'admin_fee': admin_fee,
        'arbs_fee': arbs_fee,
        'arb_fee': arb_fee,
        'comment0': comment0,
        'comment1': comment1,
    }

    return result


def rspp_ru(amount, arbs, proc, type):
    """ Calculates fees for domestic arbitration in the Arbitration Centre at
        the Russian Union of Industrialists and Entrepreneurs
    """
    comment0 = ''
    comment2 = ''

    if type == 'Корпоративный':

        reg_fee = 30000.0
        # if parties == 3:
        #     reg_fee += 10000.0
        # if parties == 4:
        #     reg_fee += 20000.0
        comment1 = (
            "Регистрационный сбор является частью административного сбора.")

        if proc == 'Ускоренная':
            comment0 += (
                'Арбитражный регламент АЦ при РСПП не содержит положений об ус'
                'коренной (арбитраже на основании документов) процедуре при ар'
                'битраже корпоративного спора. Результаты для стандартной проц'
                'едуры.'
            )

        # calculate arb_fee (sole arbitrator)
        if amount <= 500000:
            arb_fee = 60000
        elif 500000 < amount <= 750000:
            arb_fee = 70000
        elif 750000 < amount <= 1000000:
            arb_fee = 80000
        elif 1000000 < amount <= 1500000:
            arb_fee = 110000
        elif 1500000 < amount <= 2000000:
            arb_fee = 130000
        elif 2000000 < amount <= 2500000:
            arb_fee = 150000
        elif 2500000 < amount <= 3000000:
            arb_fee = 170000
        elif 3000000 < amount <= 4000000:
            arb_fee = 200000
        elif 4000000 < amount <= 5000000:
            arb_fee = 230000
        elif 5000000 < amount <= 6000000:
            arb_fee = 260000
        elif 6000000 < amount <= 7000000:
            arb_fee = 290000
        elif 7000000 < amount <= 8500000:
            arb_fee = 330000
        elif 8500000 < amount <= 10000000:
            arb_fee = 370000
        elif 10000000 < amount <= 11500000:
            arb_fee = 410000
        elif 11500000 < amount <= 13000000:
            arb_fee = 450000
        elif 13000000 < amount <= 15000000:
            arb_fee = 500000
        elif 15000000 < amount <= 20000000:
            arb_fee = 550000
        elif 20000000 < amount <= 25000000:
            arb_fee = 600000
        elif 25000000 < amount <= 30000000:
            arb_fee = 650000
        elif 30000000 < amount <= 40000000:
            arb_fee = 750000
        elif 40000000 < amount <= 50000000:
            arb_fee = 850000
        elif 50000000 < amount <= 60000000:
            arb_fee = 950000
        elif 60000000 < amount <= 80000000:
            arb_fee = 1100000
        elif 80000000 < amount <= 100000000:
            arb_fee = 1250000
        elif 100000000 < amount <= 125000000:
            arb_fee = 1450000
        elif 125000000 < amount <= 150000000:
            arb_fee = 1650000
        elif 150000000 < amount <= 200000000:
            arb_fee = 1900000
        elif 200000000 < amount <= 300000000:
            arb_fee = 2100000
        elif 300000000 < amount <= 500000000:
            arb_fee = 25000000
        elif 50000000 < amount:
            arb_fee = 25000000 + (amount - 50000000) * 0.0012

    if type == 'Внутренний':

        reg_fee = 20000.0

        comment1 = (
            "Регистрационный сбор является частью административного сбора.")

        # calculate arb_fee (sole arbitrator)
        if amount <= 500000:
            arb_fee = 35000
        elif 500000 < amount <= 750000:
            arb_fee = 40000
        elif 750000 < amount <= 1000000:
            arb_fee = 50000
        elif 1000000 < amount <= 1500000:
            arb_fee = 62500
        elif 1500000 < amount <= 2000000:
            arb_fee = 75000
        elif 2000000 < amount <= 2500000:
            arb_fee = 87500
        elif 2500000 < amount <= 3000000:
            arb_fee = 100000
        elif 3000000 < amount <= 4000000:
            arb_fee = 112500
        elif 4000000 < amount <= 5000000:
            arb_fee = 125000
        elif 5000000 < amount <= 6000000:
            arb_fee = 137500
        elif 6000000 < amount <= 7000000:
            arb_fee = 150000
        elif 7000000 < amount <= 8500000:
            arb_fee = 162500
        elif 8500000 < amount <= 10000000:
            arb_fee = 175000
        elif 10000000 < amount <= 11500000:
            arb_fee = 190000
        elif 11500000 < amount <= 13000000:
            arb_fee = 210000
        elif 13000000 < amount <= 15000000:
            arb_fee = 240000
        elif 15000000 < amount <= 20000000:
            arb_fee = 280000
        elif 20000000 < amount <= 25000000:
            arb_fee = 330000
        elif 25000000 < amount <= 30000000:
            arb_fee = 380000
        elif 30000000 < amount <= 40000000:
            arb_fee = 480000
        elif 40000000 < amount <= 50000000:
            arb_fee = 580000
        elif 50000000 < amount <= 60000000:
            arb_fee = 680000
        elif 60000000 < amount <= 80000000:
            arb_fee = 805000
        elif 80000000 < amount <= 100000000:
            arb_fee = 930000
        elif 100000000 < amount <= 125000000:
            arb_fee = 1080000
        elif 125000000 < amount <= 150000000:
            arb_fee = 1230000
        elif 150000000 < amount <= 200000000:
            arb_fee = 1430000
        elif 200000000 < amount <= 300000000:
            arb_fee = 1680000
        elif 300000000 < amount <= 500000000:
            arb_fee = 1980000
        elif 50000000 < amount:
            arb_fee = 1980000 + (amount - 50000000) * 0.001

        # Expedited proc affects arb_fee and reg_fee
        if proc == 'Ускоренная':
            arb_fee *= 0.7
            reg_fee *= 0.5
            comment2 += (
                'Приведен расчет для арбитража на основании документов без проведе'
                'ния устных слушаний'
            )

    # caclulate arb_fee (if panel of three arbitrators)
    if arbs == 3:
        arb_fee *= 1.3

    # proportion applies for arbs_fee and admin_fee
    arbs_fee = 0.3 * arb_fee
    admin_fee = 0.7 * arb_fee

    # formatting results
    reg_fee = round(reg_fee, 2)
    arbs_fee = round(arbs_fee, 2)
    admin_fee = round(admin_fee, 2)
    arb_fee = round(arb_fee, 2)

    # saving results to dictionary
    result = {
        'reg_fee': reg_fee,
        'arb_fee': arb_fee,
        'arbs_fee': arbs_fee,
        'admin_fee': admin_fee,
        'comment0': comment0,
        'comment1': comment1,
        'comment2': comment2,
    }

    return result


def icac_ru(amount, arbs, proc, type):
    """ Calculates fees for domestic arbitration in the International
        Commercial Arbitration Court at the Chamber of Commerce and Industry
        of the Russian Federation
    """
    comment0 = ''

    if type == 'Корпоративный':

        # get rates from database
        rub_to_usd = Rate.objects.get(name='RUB_USD').rate
        usd_to_rub = Rate.objects.get(name='USD_RUB').rate

        # conbert amount to usd
        amount *= rub_to_usd

        reg_fee = 1000.0 * usd_to_rub
        comment1 = (
            "Сумма регистрационного сбора НЕ включена в сумму арбитражного сбо"
            "ра."
        )
        if proc == 'Ускоренная':
            comment0 += (
                'Правила арбитража корпоративных споров МКАС не содержат полож'
                'ений об ускоренной процедуре. Результаты для стандартной проц'
                'едуры.'
            )

        # calculating arb_fee (panel of 3)
        if amount < 10000:
            arb_fee = 3000
        elif 10000 <= amount < 50000:
            arb_fee = 3000 + (amount - 10000) * 0.125
        elif 50000 <= amount < 100000:
            arb_fee = 8000 + (amount - 50000) * 0.11
        elif 100000 <= amount < 200000:
            arb_fee = 13500 + (amount - 100000) * 0.06
        elif 200000 <= amount < 500000:
            arb_fee = 19500 + (amount - 200000) * 0.03
        elif 500000 <= amount < 1000000:
            arb_fee = 28500 + (amount - 500000) * 0.018
        elif 1000000 <= amount < 2000000:
            arb_fee = 37500 + (amount - 1000000) * 0.01
        elif 2000000 <= amount < 5000000:
            arb_fee = 47500 + (amount - 2000000) * 0.006
        elif 5000000 <= amount <= 10000000:
            arb_fee = 65500 + (amount - 5000000) * 0.005
        elif amount > 10000000:
            arb_fee = 90500 + (amount - 10000000) * 0.0014

        # back to RUB
        arb_fee *= usd_to_rub

    if type == "Внутренний":

        reg_fee = 10000.0
        comment1 = (
            "Сумма регистрационного сбора НЕ включена в сумму арбитражного сбо"
            "ра."
        )

        if proc == 'Ускоренная':
            comment0 += (
                'Правила арбитража внутренних споров МКАС не содержат положени'
                'й об ускоренной процедуре. Результаты для стандартной процеду'
                'ры.'
            )

        if amount <= 100000:
            arb_fee = 10000.0
        if 100000 < amount <= 200000:
            arb_fee = 10000.0 + (amount - 100000) * 0.02
        if 200000 < amount <= 1000000:
            arb_fee = 12000.0 + (amount - 200000) * 0.018
        if 1000000 < amount <= 2000000:
            arb_fee = 26400.0 + (amount - 1000000) * 0.008
        if 2000000 < amount <= 10000000:
            arb_fee = 34400.0 + (amount - 2000000) * 0.005
        if 10000000 < amount <= 30000000:
            arb_fee = 74400.0 + (amount - 10000000) * 0.004
        if 30000000 < amount <= 50000000:
            arb_fee = 154400.0 + (amount - 30000000) * 0.003
        if 50000000 < amount <= 70000000:
            arb_fee = 214400.0 + (amount - 50000000) * 0.002
        if amount > 70000000:
            arb_fee = 254400.0 + (amount - 70000000) * 0.0015

    # calculate arb, arbs and admin fee (solo)
    if arbs == 1:
        arb_fee *= 0.8
        arbs_fee = 0.4 * arb_fee * 0.72
        admin_fee = arb_fee - arbs_fee

    # calculate arb, arbs and admin fee (panel of three)
    if arbs == 3:
        arbs_fee = 0.4 * arb_fee * 0.78
        admin_fee = arb_fee - arbs_fee

    # formatting the results
    admin_fee = round(admin_fee, 2)
    arbs_fee = round(arbs_fee, 2)
    arb_fee = round(arb_fee, 2)
    reg_fee = round(arb_fee, 2)

    # adding results to dict
    result = {
        'reg_fee': reg_fee,
        'admin_fee': admin_fee,
        'arbs_fee': arbs_fee,
        'arb_fee': arb_fee,
        'comment0': comment0,
        'comment1': comment1,
    }

    return result


def ai_chooser_ru(req, ais, amount, arbs, proc, type):
    """ Calls ai function for each Arbitral institution in UserRequestRu and
        collects results in a list of CostRu objects
    """
    result = []
    for ai in ais:
        if ai.id == 1:
            res = rima_ru(amount, arbs, proc, type)
        elif ai.id == 2:
            res = rspp_ru(amount, arbs, proc, type)
        elif ai.id == 3:
            res = icac_ru(amount, arbs, proc, type)
        obj = CostRu(ai=ai, req=req)
        obj.reg_fee = res['reg_fee']
        obj.arb_fee = res['arb_fee']
        obj.arbs_fee = res['arbs_fee']
        obj.admin_fee = res['admin_fee']
        if 'comment0' in res:
            obj.comment0 = res['comment0']
        obj.comment1 = res['comment1']
        obj.save()
        result.append(obj)

    return result
