from calc.models import Cost, Rate


usd_to_eur = Rate.objects.get(name='USD_EUR').rate
eur_to_usd = Rate.objects.get(name='EUR_USD').rate
rub_to_usd = Rate.objects.get(name='RUB_USD').rate
usd_to_rub = Rate.objects.get(name='USD_RUB').rate
usd_to_rmb = Rate.objects.get(name='USD_CNY').rate
rmb_to_usd = Rate.objects.get(name='CNY_USD').rate
usd_to_hkd = Rate.objects.get(name='USD_HKD').rate
hkd_to_usd = Rate.objects.get(name='HKD_USD').rate
sgd_to_usd = Rate.objects.get(name='SGD_USD').rate
usd_to_sgd = Rate.objects.get(name='USD_SGD').rate

# usd_to_eur = 1
# eur_to_usd = 1
# rub_to_usd = 1
# usd_to_rub = 1
# usd_to_rmb = 1
# rmb_to_usd = 1
# usd_to_hkd = 1
# hkd_to_usd = 1
# sgd_to_usd = 1
# usd_to_sgd = 1


def rac_at_rima(amount, arbs, proc, measures):

    reg_fee = 500.0
    comment1 = 'The Registration fee is included in the Arbitration fee.'

    admin_fee = 0
    arbs_fee = 0
    comment0 = ''

    if proc == 'Expedited' and amount >= 500000:
        comment0 += (
            'Expedited arbitration only allowed under US$ 500 000 under RIMA R'
            'ules.\nType of arbitration was changed to "Standard".'
        )
        proc = 'Standard'

    if proc == 'Expedited' and arbs == 3:
        comment0 += (
            'A case is settled by a sole arbitrator in an Expedited arbitratio'
            'n under RIMA Rules.\nThe following estimation is for a sole arbit'
            'rator.'
        )
        arbs = 1

    if amount < 10000:
        admin_fee = 1000.00
        arbs_fee = 2000.00
    elif 10000 <= amount < 30000:
        admin_fee = 1000.00 + (amount - 10000) * 0.03
        arbs_fee = 2000.00 + (amount - 10000) * 0.07
    elif 30000 <= amount < 100000:
        admin_fee = 1600.00 + (amount - 30000) * 0.025
        arbs_fee = 3400.00 + (amount - 30000) * 0.06
    elif 100000 <= amount < 200000:
        admin_fee = 3350.00 + (amount - 100000) * 0.02
        arbs_fee = 7600.00 + (amount - 100000) * 0.05
    elif 200000 <= amount < 400000:
        admin_fee = 5350.00 + (amount - 200000) * 0.01
        arbs_fee = 12600.00 + (amount - 200000) * 0.035
    elif 400000 <= amount < 500000:
        admin_fee = 7350.00 + (amount - 400000) * 0.005
        arbs_fee = 19600.00 + (amount - 400000) * 0.025
    elif 500000 <= amount < 1000000:
        admin_fee = 7850.00 + (amount - 500000) * 0.0025
        arbs_fee = 22100.00 + (amount - 500000) * 0.015
    elif 1000000 <= amount < 2000000:
        admin_fee = 9100.00 + (amount - 1000000) * 0.0015
        arbs_fee = 29600.00 + (amount - 1000000) * 0.01
    elif 2000000 <= amount < 10000000:
        admin_fee = 10600.00 + (amount - 2000000) * 0.0005
        arbs_fee = 39600.00 + (amount - 2000000) * 0.0025
    elif 10000000 <= amount:
        admin_fee = 14600.00 + (amount - 10000000) * 0.0001
        arbs_fee = 51600.00 + (amount - 10000000) * 0.0015

    if proc == 'Expedited':
        if amount < 500000:
            admin_fee *= 0.5
            arbs_fee *= 0.75

    if arbs == 1:
        if amount >= 500000:
            arbs_fee *= 0.8

    if arbs == 3:
        if amount < 500000:
            arbs_fee *= 1.2

    arb_fee = admin_fee + arbs_fee

    if measures == 'Yes':
        comment3 = (
            'The RIMA Rules set no additional costs for emergency measures pro'
            'ceedings'
        )

    admin_fee = round(admin_fee, 2)
    arbs_fee = round(arbs_fee, 2)
    arb_fee = round(arb_fee, 2)

    result = {
        'reg_fee': reg_fee,
        'admin_fee': admin_fee,
        'arbs_fee': arbs_fee,
        'arb_fee': arb_fee,
        'comment0': comment0,
        'comment1': comment1,
        'comment3': comment3,
    }

    return result


def scc(amount, arbs, proc, parties, measures):

    amount *= usd_to_eur

    comment1 = 'The Registration fee is included in the Arbitration fee.'
    comment0 = ''

    if proc == 'Standard':

        reg_fee = eur_to_usd * 3000.00

        if amount <= 25000:
            admin_fee = 3000.00
            min_arbs_fee = 4000.00
            max_arbs_fee = 12000.00
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 25000 < amount <= 50000:
            admin_fee = 3000.00 + (amount - 25000) * 0.048
            min_arbs_fee = 4000.00 + (amount - 25000) * 0.02
            max_arbs_fee = 12000.00 + (amount - 25000) * 0.14
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 50000 < amount <= 100000:
            admin_fee = 4200.00 + (amount - 50000) * 0.026
            min_arbs_fee = 4500.00 + (amount - 50000) * 0.05
            max_arbs_fee = 15500.00 + (amount - 50000) * 0.05
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 100000 < amount <= 500000:
            admin_fee = 5500.00 + (amount - 100000) * 0.021
            min_arbs_fee = 7000.00 + (amount - 100000) * 0.02
            max_arbs_fee = 18000.00 + (amount - 100000) * 0.04
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 500000 < amount <= 1000000:
            admin_fee = 13900.00 + (amount - 500000) * 0.009
            min_arbs_fee = 15000.00 + (amount - 500000) * 0.01
            max_arbs_fee = 34000.00 + (amount - 500000) * 0.03
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 1000000 < amount <= 2000000:
            admin_fee = 18400.00 + (amount - 1000000) * 0.005
            min_arbs_fee = 20000.00 + (amount - 1000000) * 0.008
            max_arbs_fee = 49000.00 + (amount - 1000000) * 0.023
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 2000000 < amount <= 5000000:
            admin_fee = 23400.00 + (amount - 2000000) * 0.0035
            min_arbs_fee = 28000.00 + (amount - 2000000) * 0.004
            max_arbs_fee = 72000.00 + (amount - 2000000) * 0.014
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 5000000 < amount <= 10000000:
            admin_fee = 33900.00 + (amount - 5000000) * 0.0014
            min_arbs_fee = 40000.00 + (amount - 5000000) * 0.002
            max_arbs_fee = 114000.00 + (amount - 5000000) * 0.005
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 10000000 < amount <= 50000000:
            admin_fee = 40900.00 + (amount - 10000000) * 0.0005
            min_arbs_fee = 50000.00 + (amount - 10000000) * 0.0005
            max_arbs_fee = 139000.00 + (amount - 10000000) * 0.002
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 50000000 < amount <= 75000000:
            admin_fee = 60900.00 + (amount - 50000000) * 0.0003
            min_arbs_fee = 70000.00 + (amount - 50000000) * 0.0005
            max_arbs_fee = 219000.00 + (amount - 50000000) * 0.0012
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 75000000 < amount <= 100000000:
            admin_fee = 68400.00 + (amount - 75000000) * 0.0002
            if admin_fee > 70000:
                admin_fee = 70000.0
            min_arbs_fee = 82500.00 + (amount - 75000000) * 0.0003
            max_arbs_fee = 249000.00 + (amount - 75000000) * 0.0005
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif amount > 100000000:
            admin_fee = 70000
            min_arbs_fee = 0
            max_arbs_fee = 0
            med_arbs_fee = 0

        if arbs == 3:
            min_arbs_fee *= 2.2
            max_arbs_fee *= 2.2
            med_arbs_fee *= 2.2

    if proc == 'Expedited':

        reg_fee = eur_to_usd * 2500.00

        if arbs == 3:
            comment0 += (
                'Parties can only appoint one arbitrator in an Expedited arbit'
                'ration under SCC Rules.\nThe following estimation is for a '
                'sole arbitrator.'
            )
            arbs = 1

        if amount <= 25000:
            admin_fee = 2500.00
            min_arbs_fee = 4000.00
            max_arbs_fee = 7000.00
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 25000 < amount <= 50000:
            admin_fee = 2500.00 + (amount - 25000) * 0.026
            min_arbs_fee = 4000.00 + (amount - 25000) * 0.02
            max_arbs_fee = 7000.00 + (amount - 25000) * 0.06
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 50000 < amount <= 100000:
            admin_fee = 3150.00 + (amount - 50000) * 0.017
            min_arbs_fee = 4500.00 + (amount - 50000) * 0.008
            max_arbs_fee = 8500.00 + (amount - 50000) * 0.04
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 100000 < amount <= 500000:
            admin_fee = 4000.00 + (amount - 100000) * 0.008
            min_arbs_fee = 4900.00 + (amount - 100000) * 0.015
            max_arbs_fee = 10500.00 + (amount - 100000) * 0.034
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 500000 < amount <= 1000000:
            admin_fee = 7200.00 + (amount - 500000) * 0.005
            min_arbs_fee = 10900.00 + (amount - 500000) * 0.01
            max_arbs_fee = 24100.00 + (amount - 500000) * 0.024
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 1000000 < amount <= 2000000:
            admin_fee = 9700.00 + (amount - 1000000) * 0.003
            min_arbs_fee = 15900.00 + (amount - 1000000) * 0.008
            max_arbs_fee = 36100.00 + (amount - 1000000) * 0.016
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 2000000 < amount <= 5000000:
            admin_fee = 12700.00 + (amount - 2000000) * 0.0013
            min_arbs_fee = 23900.00 + (amount - 2000000) * 0.004
            max_arbs_fee = 52100.00 + (amount - 2000000) * 0.01
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 5000000 < amount <= 10000000:
            admin_fee = 16600.00 + (amount - 5000000) * 0.0006
            min_arbs_fee = 0
            max_arbs_fee = 0
            med_arbs_fee = 0
        elif amount > 10000000:
            admin_fee = 19600.00 + (amount - 10000000) * 0.001
            if admin_fee > 35000:
                admin_fee = 35000.00
            min_arbs_fee = 0
            max_arbs_fee = 0
            med_arbs_fee = 0

    admin_fee *= eur_to_usd
    min_arbs_fee *= eur_to_usd
    max_arbs_fee *= eur_to_usd
    med_arbs_fee *= eur_to_usd

    reg_fee = round(reg_fee, 2)
    admin_fee = round(admin_fee, 2)
    min_arbs_fee = round(min_arbs_fee, 2)
    max_arbs_fee = round(max_arbs_fee, 2)
    med_arbs_fee = round(med_arbs_fee, 2)

    med_arb_fee = admin_fee + med_arbs_fee
    med_arb_fee = round(med_arb_fee, 2)

    comment2 = ''

    if med_arbs_fee != 0:
        comment2 = (
            f"Arbitrators fee is determined by the SCC Board.\nThe estimation "
            f"above is based upon Median Arbitrators fee.\nMinimum Arbitrators"
            f" fee in this case is USD {min_arbs_fee}.\nMaximum Arbitrators fe"
            f"e in this case is USD {max_arbs_fee}."
        )
    else:
        if comment0:
            comment0 += '\n'
        comment0 += (
            'If the amount in dispute exceeds EUR 5,000,000 the SCC Board de'
            'termines the Arbitrators fee.'
        )

    result = {
        'reg_fee': reg_fee,
        'admin_fee': admin_fee,
        'arbs_fee': med_arbs_fee,
        'arb_fee': med_arb_fee,
        'comment0': comment0,
        'comment1': comment1,
        'comment2': comment2
    }

    return result


def icc(amount, arbs, proc, parties, measures):

    reg_fee = 5000.00
    comment1 = "The Registration fee is included in the Arbitration fee."
    comment0 = ''

    if proc == 'Standard':

        if amount <= 50000:
            admin_fee = 5000.00
            min_arbs_fee = 3000.00
            max_arbs_fee = amount * 0.1802
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 50000 < amount <= 100000:
            admin_fee = 5000.00 + (amount - 50000) * 0.0153
            min_arbs_fee = 3000.00 + (amount - 50000) * 0.0265
            max_arbs_fee = 9100.00 + (amount - 50000) * 0.13568
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 100000 < amount <= 200000:
            admin_fee = 5765.00 + (amount - 100000) * 0.0272
            min_arbs_fee = 4325.00 + (amount - 100000) * 0.01431
            max_arbs_fee = 15794.00 + (amount - 100000) * 0.07685
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 200000 < amount <= 500000:
            admin_fee = 8485.00 + (amount - 200000) * 0.0225
            min_arbs_fee = 5756.00 + (amount - 200000) * 0.01367
            max_arbs_fee = 23479.00 + (amount - 200000) * 0.06837
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 500000 < amount <= 1000000:
            admin_fee = 15235.00 + (amount - 500000) * 0.0162
            min_arbs_fee = 9857.00 + (amount - 500000) * 0.00954
            max_arbs_fee = 43990.00 + (amount - 500000) * 0.04028
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 1000000 < amount <= 2000000:
            admin_fee = 23335.00 + (amount - 1000000) * 0.00788
            min_arbs_fee = 14627.00 + (amount - 1000000) * 0.00689
            max_arbs_fee = 64130.00 + (amount - 1000000) * 0.03604
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 2000000 < amount <= 5000000:
            admin_fee = 31215.00 + (amount - 2000000) * 0.0046
            min_arbs_fee = 21517.00 + (amount - 2000000) * 0.00375
            max_arbs_fee = 100170.00 + (amount - 2000000) * 0.01391
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 5000000 < amount <= 10000000:
            admin_fee = 45015.00 + (amount - 5000000) * 0.0025
            min_arbs_fee = 32767.00 + (amount - 5000000) * 0.00128
            max_arbs_fee = 141900.00 + (amount - 5000000) * 0.0091
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 10000000 < amount <= 30000000:
            admin_fee = 57515.00 + (amount - 10000000) * 0.001
            min_arbs_fee = 39167.00 + (amount - 10000000) * 0.00064
            max_arbs_fee = 187400.00 + (amount - 10000000) * 0.00241
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 30000000 < amount <= 50000000:
            admin_fee = 95515.00 + (amount - 30000000) * 0.0009
            min_arbs_fee = 51967.00 + (amount - 30000000) * 0.00059
            max_arbs_fee = 235600.00 + (amount - 30000000) * 0.00228
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 50000000 < amount <= 80000000:
            admin_fee = 98515.00 + (amount - 50000000) * 0.0001
            min_arbs_fee = 63767.00 + (amount - 50000000) * 0.00033
            max_arbs_fee = 281200.00 + (amount - 50000000) * 0.00157
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 80000000 < amount <= 100000000:
            admin_fee = 100975.00 + (amount - 80000000) * 0.00123
            min_arbs_fee = 73667.00 + (amount - 80000000) * 0.00021
            max_arbs_fee = 328300.00 + (amount - 80000000) * 0.00115
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 100000000 < amount <= 500000000:
            admin_fee = 13900.00 + (amount - 100000000) * 0.00123
            min_arbs_fee = 77867.00 + (amount - 100000000) * 0.00011
            max_arbs_fee = 351300.00 + (amount - 100000000) * 0.00058
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif amount > 500000000:
            admin_fee = 150000.00
            min_arbs_fee = 121867.00 + (amount - 500000000) * 0.0001
            max_arbs_fee = 583300.00 + (amount - 500000000) * 0.0004
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2

    elif proc == 'Expedited':

        if arbs == 3:
            comment0 = (
                'NB! In Expedited Arbitration ICC Court is empowered to appoin'
                't a sole arbitrator to hear the dispute notwithstanding any c'
                'ontrary provision of the arbitration agreement.\nHowever, the'
                ' estimation is calculated for a panel of three arbitrators.'
            )

        if amount <= 50000:
            admin_fee = 5000.00
            min_arbs_fee = 2400.00
            max_arbs_fee = amount * 0.14416
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 50000 < amount <= 100000:
            admin_fee = 5000.00 + (amount - 50000) * 0.0153
            min_arbs_fee = 2400.00 + (amount - 50000) * 0.0212
            max_arbs_fee = 7208.00 + (amount - 50000) * 0.108544
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 100000 < amount <= 200000:
            admin_fee = 5765.00 + (amount - 100000) * 0.0272
            min_arbs_fee = 3460.00 + (amount - 100000) * 0.011448
            max_arbs_fee = 12635.00 + (amount - 100000) * 0.06148
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 200000 < amount <= 500000:
            admin_fee = 8485.00 + (amount - 200000) * 0.0225
            min_arbs_fee = 4605.00 + (amount - 200000) * 0.010936
            max_arbs_fee = 18783.00 + (amount - 200000) * 0.054696
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 500000 < amount <= 1000000:
            admin_fee = 15235.00 + (amount - 500000) * 0.0162
            min_arbs_fee = 7886.00 + (amount - 500000) * 0.007632
            max_arbs_fee = 35192.00 + (amount - 500000) * 0.032224
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 1000000 < amount <= 2000000:
            admin_fee = 23335.00 + (amount - 1000000) * 0.00788
            min_arbs_fee = 11702.00 + (amount - 1000000) * 0.005512
            max_arbs_fee = 51304.00 + (amount - 1000000) * 0.028832
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 2000000 < amount <= 5000000:
            admin_fee = 31215.00 + (amount - 2000000) * 0.0046
            min_arbs_fee = 17214.00 + (amount - 2000000) * 0.003
            max_arbs_fee = 80136.00 + (amount - 2000000) * 0.011128
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 5000000 < amount <= 10000000:
            admin_fee = 45015.00 + (amount - 5000000) * 0.0025
            min_arbs_fee = 26214.00 + (amount - 5000000) * 0.001024
            max_arbs_fee = 113520.00 + (amount - 5000000) * 0.007280
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 10000000 < amount <= 30000000:
            admin_fee = 57515.00 + (amount - 10000000) * 0.001
            min_arbs_fee = 31334.00 + (amount - 10000000) * 0.000512
            max_arbs_fee = 149920.00 + (amount - 10000000) * 0.001928
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 30000000 < amount <= 50000000:
            admin_fee = 95515.00 + (amount - 30000000) * 0.0009
            min_arbs_fee = 41574.00 + (amount - 30000000) * 0.000472
            max_arbs_fee = 188480.00 + (amount - 30000000) * 0.001824
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 50000000 < amount <= 80000000:
            admin_fee = 98515.00 + (amount - 50000000) * 0.0001
            min_arbs_fee = 51014.00 + (amount - 50000000) * 0.000264
            max_arbs_fee = 224960.00 + (amount - 50000000) * 0.001256
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 80000000 < amount <= 100000000:
            admin_fee = 100975.00 + (amount - 80000000) * 0.00123
            min_arbs_fee = 58934.00 + (amount - 80000000) * 0.000168
            max_arbs_fee = 262640.00 + (amount - 80000000) * 0.00092
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif 100000000 < amount <= 500000000:
            admin_fee = 13900.00 + (amount - 100000000) * 0.00123
            min_arbs_fee = 62294.00 + (amount - 100000000) * 0.000088
            max_arbs_fee = 281040.00 + (amount - 100000000) * 0.000464
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
        elif amount > 500000000:
            admin_fee = 150000.00
            min_arbs_fee = 97494.00 + (amount - 500000000) * 0.00008
            max_arbs_fee = 466640.00 + (amount - 500000000) * 0.00032
            med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2

    if amount < 3000000 and proc == 'Standard':
        comment0 = (
            'NB! The Expedited Procedure of the ICC Rules apply automatica'
            'lly to cases with amounts in dispute less then US$ 2 000 000 if'
            ' the arbitration agreement was concluded on or after 1 March '
            '2017 and before 1 January 2021 or to cases with amounts in disput'
            'e less thenless then US$ 3 000 000 if the arbitration agreement w'
            'as concluded on or after 1 January 2021.\nThe Expedited Procedure'
            ' will not apply if the parties opt out in their arbitration agree'
            'ment.'
        )

    if arbs == 3:
        min_arbs_fee *= 3
        max_arbs_fee *= 3
        med_arbs_fee *= 3

    med_arb_fee = admin_fee + med_arbs_fee

    min_arbs_fee = round(min_arbs_fee, 2)
    max_arbs_fee = round(max_arbs_fee, 2)
    med_arbs_fee = round(med_arbs_fee, 2)
    admin_fee = round(admin_fee, 2)
    med_arb_fee = round(med_arb_fee, 2)

    comment2 = (
        f"Arbitrators fee is determined by the ICC Court.\n The estimation abo"
        f"ve is based upon Median Arbitrators fee.\n Minimum Arbitrators fee i"
        f"n this case is {min_arbs_fee}.\n Maximum Arbitrators fee in this cas"
        f"e is {max_arbs_fee}.\n"
    )

    result = {
        'reg_fee': reg_fee,
        'admin_fee': admin_fee,
        'arbs_fee': med_arbs_fee,
        'arb_fee': med_arb_fee,
        'comment0': comment0,
        'comment1': comment1,
        'comment2': comment2
    }

    return result


def hkiac(amount, arbs, proc, parties, measures):

    amount *= usd_to_hkd
    reg_fee = hkd_to_usd * 8000.00
    comment1 = 'The Registration fee is NOT included in the Arbitration fee'
    comment0 = ''

    if proc == 'Expedited' and amount > 25000000:
        comment0 += (
            'Expedited arbitration is only allowed under HKD 25 000 000 under '
            'HKIAC Rules.\nType of arbitration was changed to "Standard".'
        )
        proc == 'Standard'

    if amount <= 400000:
        admin_fee = 19800.00
        arbs_fee = 0.11 * amount
    if 400000 < amount <= 800000:
        admin_fee = 19800.00 + (amount - 400000) * 0.013
        arbs_fee = 44000.00 + (amount - 400000) * 0.1
    if 800000 < amount <= 4000000:
        admin_fee = 25000.00 + (amount - 800000) * 0.01
        arbs_fee = 84000.00 + (amount - 800000) * 0.053
    if 4000000 < amount <= 8000000:
        admin_fee = 57000.00 + (amount - 4000000) * 0.00545
        arbs_fee = 253600.00 + (amount - 4000000) * 0.0378
    if 8000000 < amount <= 16000000:
        admin_fee = 78800.00 + (amount - 8000000) * 0.00265
        arbs_fee = 404800.00 + (amount - 8000000) * 0.0173
    if 16000000 < amount <= 40000000:
        admin_fee = 100000.00 + (amount - 16000000) * 0.002
        arbs_fee = 543200.00 + (amount - 16000000) * 0.0106
    if 40000000 < amount <= 80000000:
        admin_fee = 148000.00 + (amount - 40000000) * 0.0011
        arbs_fee = 797600.00 + (amount - 40000000) * 0.0044
    if 80000000 < amount <= 240000000:
        admin_fee = 192000.00 + (amount - 80000000) * 0.00071
        arbs_fee = 973600.00 + (amount - 80000000) * 0.0025
    if 240000000 < amount <= 400000000:
        admin_fee = 305600.00 + (amount - 240000000) * 0.00059
        arbs_fee = 1373600.00 + (amount - 240000000) * 0.00228
    if 400000000 < amount <= 600000000:
        admin_fee = 400000.00
        arbs_fee = 1738400.00 + (amount - 400000000) * 0.00101
    if 600000000 < amount <= 800000000:
        admin_fee = 400000.00
        arbs_fee = 1940400.00 + (amount - 600000000) * 0.00067
    if 800000000 < amount <= 4000000000:
        admin_fee = 400000.00
        arbs_fee = 2074400.00 + (amount - 800000000) * 0.00044
    if amount > 4000000000:
        admin_fee = 400000.00
        arbs_fee = 3482400.00 + (amount - 4000000000) * 0.00025
        if arbs_fee > 12574000:
            arbs_fee = 12574000.00

    if arbs == 3:
        arbs_fee *= 3

    arbs_fee *= hkd_to_usd
    admin_fee *= hkd_to_usd
    arb_fee = arbs_fee + admin_fee

    arbs_fee = round(arbs_fee, 2)
    admin_fee = round(admin_fee, 2)
    arb_fee = round(arb_fee, 2)
    reg_fee = round(reg_fee, 2)

    result = {
        'reg_fee': reg_fee,
        'arb_fee': arb_fee,
        'arbs_fee': arbs_fee,
        'admin_fee': admin_fee,
        'comment0': comment0,
        'comment1': comment1
    }

    return result


def siac(amount, arbs, proc, parties, measures):

    reg_fee = 2000.00
    comment1 = (
        'The Registration fee is NOT included in the Arbitration fee.\nFor Sin'
        'gapore parties the registration (filling) fee is SGD 2 140.'
    )
    comment0 = ''

    if proc == 'Expedited' and amount > 6000000:
        comment0 = (
            'Expedited arbitration is only allowed under SGD 6 000 000 under '
            'SIAC Rules.\nType of arbitration was changed to "Standard".'
        )
        proc == 'Standard'

    if amount <= 50000:
        admin_fee = 3800.00
        arbs_fee = 6250.00
    if 50000 < amount <= 100000:
        admin_fee = 3800.00 + (amount - 50000) * 0.022
        arbs_fee = 6250.00 + (amount - 50000) * 0.138
    if 100000 < amount <= 500000:
        admin_fee = 4900.00 + (amount - 100000) * 0.012
        arbs_fee = 13150.00 + (amount - 100000) * 0.065
    if 500000 < amount <= 1000000:
        admin_fee = 9700.00 + (amount - 500000) * 0.01
        arbs_fee = 39150.00 + (amount - 500000) * 0.0485
    if 1000000 < amount <= 2000000:
        admin_fee = 14700.00 + (amount - 1000000) * 0.0065
        arbs_fee = 63400.00 + (amount - 1000000) * 0.0275
    if 2000000 < amount <= 5000000:
        admin_fee = 21200.00 + (amount - 2000000) * 0.0032
        arbs_fee = 90900.00 + (amount - 2000000) * 0.0012
    if 5000000 < amount <= 10000000:
        admin_fee = 30800.00 + (amount - 5000000) * 0.0016
        arbs_fee = 126900.00 + (amount - 5000000) * 0.007
    if 10000000 < amount <= 50000000:
        admin_fee = 38800.00 + (amount - 10000000) * 0.00095
        arbs_fee = 161900.00 + (amount - 10000000) * 0.003
    if 50000000 < amount <= 80000000:
        admin_fee = 76800.00 + (amount - 50000000) * 0.0004
        arbs_fee = 281900.00 + (amount - 50000000) * 0.00016
    if 80000000 < amount <= 100000000:
        admin_fee = 88800.00 + (amount - 80000000) * 0.00031
        arbs_fee = 329900.00 + (amount - 80000000) * 0.00075
    if 100000000 < amount <= 500000000:
        admin_fee = 95000.00
        arbs_fee = 344900 + (amount - 100000000) * 0.00065
    if amount > 500000000:
        admin_fee = 95000.00
        arbs_fee = 605000.00 + (amount - 500000000) * 0.0004
        if arbs_fee > 2000000:
            arbs_fee = 2000000.00

    if arbs == 3:
        arbs_fee *= 3

    arb_fee = arbs_fee + admin_fee

    arbs_fee = round(arbs_fee, 2)
    admin_fee = round(admin_fee, 2)
    arb_fee = round(arb_fee, 2)

    result = {
        'reg_fee': reg_fee,
        'arb_fee': arb_fee,
        'arbs_fee': arbs_fee,
        'admin_fee': admin_fee,
        'comment1': comment1,
        'comment0': comment0
    }

    return result


def viac(amount, arbs, proc, parties, measures):

    amount *= usd_to_eur
    comment1 = 'Registration fee is NOT included in the Arbitration fee.'

    if amount <= 25000:
        reg_fee = 500.00
        admin_fee = 500.00
        arbs_fee = 3000.00
    if 25000 < amount <= 75000:
        reg_fee = 1000.00
        admin_fee = 500.00
        arbs_fee = amount * 0.06
        if arbs_fee < 3000:
            arbs_fee = 3000.00
    if 75000 < amount <= 100000:
        reg_fee = 1500.00
        admin_fee = 1000.00
        arbs_fee = amount * 0.06
        if arbs_fee < 3000:
            arbs_fee = 3000.00
    if 100000 < amount <= 200000:
        reg_fee = 1500.00
        admin_fee = 3000.00 + (amount - 100000) * 0.01875
        arbs_fee = 6000.00 + (amount - 100000) * 0.03
    if 200000 < amount <= 500000:
        reg_fee = 1500.00
        admin_fee = 4875.00 + (amount - 200000) * 0.0125
        arbs_fee = 9000.00 + (amount - 200000) * 0.025
    if 500000 < amount <= 1000000:
        reg_fee = 1500.00
        admin_fee = 8625.00 + (amount - 500000) * 0.00875
        arbs_fee = 16500.00 + (amount - 500000) * 0.02
    if 1000000 < amount <= 2000000:
        reg_fee = 1500.00
        admin_fee = 13000.00 + (amount - 1000000) * 0.005
        arbs_fee = 26500.00 + (amount - 1000000) * 0.01
    if 2000000 < amount <= 5000000:
        reg_fee = 1500.00
        admin_fee = 18000.00 + (amount - 2000000) * 0.00125
        if admin_fee > 75000:
            admin_fee = 75000.00
        arbs_fee = 36500.00 + (amount - 2000000) * 0.006
    if 5000000 < amount <= 10000000:
        reg_fee = 1500.00
        admin_fee = 18000.00 + (amount - 5000000) * 0.00063
        if admin_fee > 75000:
            admin_fee = 75000.00
        arbs_fee = 54500.00 + (amount - 5000000) * 0.004
    if 10000000 < amount <= 20000000:
        reg_fee = 1500.00
        admin_fee = 18000.00 + (amount - 5000000) * 0.01875
        if admin_fee > 75000:
            admin_fee = 75000.00
        arbs_fee = 74500.00 + (amount - 10000000) * 0.002
    if 20000000 < amount <= 100000000:
        reg_fee = 1500.00
        admin_fee = 18000.00 + (amount - 5000000) * 0.01875
        if admin_fee > 75000:
            admin_fee = 75000.00
        arbs_fee = 94500.00 + (amount - 20000000) * 0.001
    if amount > 100000000:
        reg_fee = 1500.00
        admin_fee = 18000.00 + (amount - 5000000) * 0.01875
        if admin_fee > 75000:
            admin_fee = 75000.00
        arbs_fee = 174500.00 + (amount - 100000000) * 0.0001

    if arbs == 3:
        arbs_fee *= 2.5

    arb_fee = arbs_fee + admin_fee

    max_arbs_fee = 1.4 * arbs_fee

    arbs_fee *= eur_to_usd
    admin_fee *= eur_to_usd
    arb_fee *= eur_to_usd
    max_arbs_fee *= eur_to_usd

    arbs_fee = round(arbs_fee, 2)
    admin_fee = round(admin_fee, 2)
    arb_fee = round(arb_fee, 2)
    max_arbs_fee = round(max_arbs_fee, 2)

    comment2 = (
        f'The Secretary General of VIAC may increase the arbitrators’ fee by a'
        f' maximum total of 40 percent. In this case Arbitrators fee may reach'
        f' USD {max_arbs_fee}.'
    )

    result = {
        'reg_fee': reg_fee,
        'arb_fee': arb_fee,
        'arbs_fee': arbs_fee,
        'admin_fee': admin_fee,
        'comment1': comment1,
        'comment2': comment2
    }

    return result


def dis(amount, arbs, proc, parties, measures):

    amount *= usd_to_eur
    reg_fee = 0.0
    comment1 = (
        'No registration fee is set by DIS Rules. Within a time limit set by '
        'the DIS, the claimant shall pay to the DIS the administrative fee.'
    )

    if amount <= 5000:
        admin_fee = amount * 0.2
        if admin_fee < 750:
            admin_fee = 750.00
        arb1 = 1000
        arb2 = arb3 = 770
    if 5000 < amount <= 20000:
        admin_fee = amount * 0.2
        if admin_fee < 750:
            admin_fee = 750.00
        arb1 = 1500
        arb2 = arb3 = 1150
    if 20000 < amount <= 50000:
        admin_fee = amount * 0.2
        if admin_fee < 750:
            admin_fee = 750.00
        arb1 = 3000
        arb2 = arb3 = 2300
    if 50000 < amount <= 70000:
        admin_fee = 1000 + (amount - 50000) * 0.1
        arb1 = 4000
        arb2 = arb3 = 3000
    if 70000 < amount <= 100000:
        admin_fee = 1000 + (amount - 50000) * 0.1
        arb1 = 5000
        arb2 = arb3 = 3800
    if 100000 < amount <= 500000:
        admin_fee = 1000 + (amount - 50000) * 0.1
        arb2 = arb3 = 4450 + (amount - 100000) * 0.2
        arb1 = 1.3 * arb2
    if 500000 < amount <= 1000000:
        admin_fee = 1000 + (amount - 50000) * 0.1
        arb2 = arb3 = 12450 + (amount - 100000) * 0.14
        arb1 = 1.3 * arb2
    if 1000000 < amount <= 2000000:
        admin_fee = 10500 + (amount - 1000000) * 0.1
        arb2 = arb3 = 19450 + (amount - 1000000) * 0.1
        arb1 = 1.3 * arb2
    if 2000000 < amount <= 5000000:
        admin_fee = 10500 + (amount - 1000000) * 0.1
        arb2 = arb3 = 29450 + (amount - 2000000) * 0.005
        arb1 = 1.3 * arb2
    if 5000000 < amount <= 10000000:
        admin_fee = 10500 + (amount - 1000000) * 0.1
        if admin_fee > 40000:
            admin_fee = 40000.00
        arb2 = arb3 = 44450 + (amount - 5000000) * 0.003
        arb1 = 1.3 * arb2
    if 10000000 < amount <= 50000000:
        admin_fee = 40000.00
        arb2 = arb3 = 59450.00 + (amount - 10000000) * 0.001
        arb1 = 1.3 * arb2
    if 50000000 < amount <= 100000000:
        admin_fee = 40000.00
        arb2 = arb3 = 99450.00 + (amount - 50000000) * 0.0006
        arb1 = 1.3 * arb2
    if 100000000 < amount <= 750000000:
        admin_fee = 40000.00
        arb2 = arb3 = 129450.00 + (amount - 100000000) * 0.0005
        arb1 = 1.3 * arb2
    if amount > 750000000:
        admin_fee = 40000.00
        arb2 = arb3 = 454450.00
        arb1 = 1.3 * arb2

    if arbs == 1:
        arbs_fee = arb1

    if arbs == 3:
        arbs_fee = arb1 + arb2 + arb3

    arb_fee = admin_fee + arbs_fee

    arbs_fee *= eur_to_usd
    admin_fee *= eur_to_usd
    arb_fee *= eur_to_usd

    admin_fee = round(admin_fee, 2)
    arbs_fee = round(arbs_fee, 2)
    arb_fee = round(arb_fee, 2)

    result = {
        'reg_fee': reg_fee,
        'admin_fee': admin_fee,
        'arbs_fee': arbs_fee,
        'arb_fee': arb_fee,
        'comment1': comment1
    }

    return result


def aiac(amount, arbs, proc, parties, measures):
    reg_fee = 2000.00
    comment1 = 'The Registration fee is NOT included in the Arbitration fee.'

    if proc == 'Expedited':
        if amount <= 50000:
            arbs_fee = 3500.00
        if 50000 < amount <= 100000:
            arbs_fee = 3500.00 + (amount - 50000) * 0.0054
        if 100000 < amount <= 500000:
            arbs_fee = 6200.00 + (amount - 100000) * 0.02475
        if 500000 < amount <= 1000000:
            arbs_fee = 16100.00 + (amount - 500000) * 0.018
        if 1000000 < amount <= 2000000:
            arbs_fee = 25100.00 + (amount - 1000000) * 0.009
        if 2000000 < amount <= 5000000:
            arbs_fee = 34000.00 + (amount - 2000000) * 0.0045
        if 5000000 < amount <= 10000000:
            arbs_fee = 47600.00 + (amount - 5000000) * 0.00225
        if 10000000 < amount <= 50000000:
            arbs_fee = 58850.00 + (amount - 10000000) * 0.001125
        if 50000000 < amount <= 80000000:
            arbs_fee = 103850.00 + (amount - 50000000) * 0.00045
        if 80000000 < amount <= 100000000:
            arbs_fee = 117350.00 + (amount - 80000000) * 0.0003375
        if amount > 100000000:
            arbs_fee = 124100.00

        if arbs == 3:
            arbs_fee *= 3

        admin_fee = 0.2 * arbs_fee

    if proc == 'Standard':
        if amount <= 50000:
            admin_fee = 2050.00
            arbs_fee = 3500.00
        if 50000 < amount <= 100000:
            admin_fee = 2050.00 + (amount - 50000) * 0.0126
            arbs_fee = 3500.00 + (amount - 50000) * 0.082
        if 100000 < amount <= 500000:
            admin_fee = 2680.00 + (amount - 100000) * 0.00705
            arbs_fee = 7600.00 + (amount - 100000) * 0.036
        if 500000 < amount <= 1000000:
            admin_fee = 5500.00 + (amount - 500000) * 0.005
            arbs_fee = 22000.00 + (amount - 500000) * 0.0302
        if 1000000 < amount <= 2000000:
            admin_fee = 8000.00 + (amount - 1000000) * 0.0035
            arbs_fee = 37100.00 + (amount - 1000000) * 0.0139
        if 2000000 < amount <= 5000000:
            admin_fee = 11500.00 + (amount - 2000000) * 0.0013
            arbs_fee = 51000.00 + (amount - 2000000) * 0.006125
        if 5000000 < amount <= 10000000:
            admin_fee = 16700.00 + (amount - 5000000) * 0.00088
            arbs_fee = 75500.00 + (amount - 5000000) * 0.0035
        if 10000000 < amount <= 50000000:
            admin_fee = 21100.00 + (amount - 10000000) * 0.00052
            arbs_fee = 93000.00 + (amount - 10000000) * 0.00181
        if 50000000 < amount <= 80000000:
            admin_fee = 41900.00
            arbs_fee = 165300.00 + (amount - 50000000) * 0.000713
        if 80000000 < amount <= 100000000:
            admin_fee = 41900.00
            arbs_fee = 186700.00 + (amount - 80000000) * 0.000535
        if 100000000 < amount <= 500000000:
            admin_fee = 41900.00
            arbs_fee = 197400 + (amount - 100000000) * 0.000386
        if amount > 500000000:
            admin_fee = 41900.00
            arbs_fee = 351800.00 + (amount - 500000000) * 0.0003
            if arbs_fee > 2000000:
                arbs_fee = 2000000.00

        if arbs == 3:
            arbs_fee *= 3

    arb_fee = arbs_fee + admin_fee

    arbs_fee = round(arbs_fee, 2)
    admin_fee = round(admin_fee, 2)
    arb_fee = round(arb_fee, 2)

    result = {
        'reg_fee': reg_fee,
        'arb_fee': arb_fee,
        'arbs_fee': arbs_fee,
        'admin_fee': admin_fee,
        'comment1': comment1
    }

    return result


def kcab(amount, arbs, proc, parties, measures):
    pass


def cietac(amount, arbs, proc, parties, measures):

    amount_c = amount * usd_to_rmb

    reg_fee_c = rmb_to_usd * 10000

    if amount_c <= 1000000:
        arb_fee_c = amount_c * 0.04
        if arb_fee_c < 10000:
            arb_fee_c = 10000.0
    elif 1000000 < amount_c <= 2000000:
        arb_fee_c = 40000.00 + (amount - 1000000) * 0.035
    elif 2000000 < amount_c <= 5000000:
        arb_fee_c = 75000.00 + (amount - 2000000) * 0.025
    elif 5000000 < amount_c <= 10000000:
        arb_fee_c = 150000.00 + (amount - 5000000) * 0.015
    elif 10000000 < amount_c <= 50000000:
        arb_fee_c = 225000.00 + (amount - 10000000) * 0.01
    elif 50000000 < amount_c <= 100000000:
        arb_fee_c = 625000.00 + (amount - 50000000) * 0.005
    elif 100000000 < amount_c <= 500000000:
        arb_fee_c = 875000.00 + (amount - 100000000) * 0.0048
    elif 500000000 < amount_c <= 1000000000:
        arb_fee_c = 2795000.00 + (amount - 500000000) * 0.0047
    elif 1000000000 < amount_c <= 2000000000:
        arb_fee_c = 5145000.00 + (amount - 1000000000) * 0.0046
    elif amount_c > 2000000000:
        arb_fee_c = 9745000.00 + (amount - 1000000) * 0.0045

    reg_fee = hkd_to_usd * 8000.00
    comment1 = 'The Registration fee is NOT included in the Arbitration fee'
    amount *= usd_to_hkd

    if amount <= 500000:
        admin_fee = 16000.00
        min_arbs_fee = 15000.00
        max_arbs_fee = 60000.00
        med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
    elif 500000 < amount <= 1000000:
        admin_fee = 16000.00 + (amount - 500000) * 0.0078
        min_arbs_fee = 15000.00 + (amount - 500000) * 0.023
        max_arbs_fee = 60000.00 + (amount - 500000) * 0.085
        med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
    elif 1000000 < amount <= 5000000:
        admin_fee = 19900.00 + (amount - 1000000) * 0.0065
        min_arbs_fee = 26500.00 + (amount - 1000000) * 0.008
        max_arbs_fee = 102500.00 + (amount - 1000000) * 0.043
        med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
    elif 5000000 < amount <= 10000000:
        admin_fee = 45900.00 + (amount - 5000000) * 0.0038
        min_arbs_fee = 58500.00 + (amount - 5000000) * 0.006
        max_arbs_fee = 274500.00 + (amount - 5000000) * 0.023
        med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
    elif 10000000 < amount <= 20000000:
        admin_fee = 64900.00 + (amount - 10000000) * 0.0022
        min_arbs_fee = 88500.00 + (amount - 5000000) * 0.0035
        max_arbs_fee = 389500.00 + (amount - 5000000) * 0.01
        med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
    elif 20000000 < amount <= 40000000:
        admin_fee = 86900.00 + (amount - 20000000) * 0.0015
        min_arbs_fee = 123500.00 + (amount - 5000000) * 0.002
        max_arbs_fee = 489500.00 + (amount - 5000000) * 0.0065
        med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
    elif 40000000 < amount <= 80000000:
        admin_fee = 116900.00 + (amount - 40000000) * 0.0008
        min_arbs_fee = 163500.00 + (amount - 5000000) * 0.0007
        max_arbs_fee = 619500.00 + (amount - 5000000) * 0.0035
        med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
    elif 80000000 < amount <= 200000000:
        admin_fee = 148900.00 + (amount - 80000000) * 0.00052
        min_arbs_fee = 191500.00 + (amount - 5000000) * 0.0005
        max_arbs_fee = 759500.00 + (amount - 5000000) * 0.0025
        med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
    elif 200000000 < amount <= 400000000:
        admin_fee = 211900.00 + (amount - 200000000) * 0.0004
        min_arbs_fee = 251500.00 + (amount - 5000000) * 0.0003
        max_arbs_fee = 1059500.00 + (amount - 5000000) * 0.0015
        med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
    elif 400000000 < amount <= 600000000:
        admin_fee = 291300.00
        min_arbs_fee = 311500.00 + (amount - 5000000) * 0.0002
        max_arbs_fee = 1359500.00 + (amount - 5000000) * 0.012
        med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
    elif 600000000 < amount <= 750000000:
        admin_fee = 291300.00
        min_arbs_fee = 351500.00 + (amount - 5000000) * 0.0001
        max_arbs_fee = 1559500.00 + (amount - 5000000) * 0.001
        med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2
    elif amount > 750000000:
        admin_fee = 291300.00
        min_arbs_fee = 366500.00 + (amount - 5000000) * 0.00008
        max_arbs_fee = 1749500.00 + (amount - 5000000) * 0.0006
        med_arbs_fee = (min_arbs_fee + max_arbs_fee) / 2

    if arbs == 3:
        min_arbs_fee *= 3
        max_arbs_fee *= 3
        med_arbs_fee *= 3

    arb_fee = admin_fee + med_arbs_fee

    arb_fee_c *= rmb_to_usd
    arb_fee *= hkd_to_usd
    admin_fee *= hkd_to_usd
    min_arbs_fee *= hkd_to_usd
    med_arbs_fee *= hkd_to_usd
    max_arbs_fee *= hkd_to_usd

    reg_fee_c = round(reg_fee_c, 2)
    arb_fee_c = round(arb_fee_c, 2)
    arb_fee = round(arb_fee, 2)
    admin_fee = round(admin_fee, 2)
    min_arbs_fee = round(min_arbs_fee, 2)
    max_arbs_fee = round(max_arbs_fee, 2)
    med_arbs_fee = round(med_arbs_fee, 2)

    comment2 = (
        f'If the case is administered by the CIETAC Hong Kong Arbitration Cent'
        f'er the following estimation applies:\nRegitration fee: {reg_fee} USD,'
        f'\nArbitration fee: {arb_fee} USD,\nAdministrative fee: {admin_fee} USD'
        f',\nMinimum Arbitrators fee: {min_arbs_fee} USD,\nMaximun Arbitrators f'
        f'ee: {max_arbs_fee} USD,\nMediam Arbitrators fee: {med_arbs_fee} USD.'
    )

    result = {
        'reg_fee': reg_fee_c,
        'arb_fee': arb_fee_c,
        'arbs_fee': 0.0,
        'admin_fee': 0.0,
        'comment1': comment1,
        'comment2': comment2
    }

    return result


def icac(amount, arbs, proc, parties, measures):

    reg_fee = 1000.0
    comment1 = "The Registration fee is NOT included in the Arbitration fee."
    comment0 = ''
    comment2 = ''

    if proc == "Expedited" and amount > 50000:
        comment0 += (
            'Expedited arbitration only allowed under US$ 500 000 under ICAC R'
            'ules.\nType of arbitration was changed to "Standard".'
        )
        proc = 'Standard'

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

    if arbs == 1:
        arb_fee *= 0.8
        arbs_fee = 0.72 * arb_fee
        admin_fee = arb_fee - arbs_fee

    if arbs == 3:
        arbs_fee = 0.78 * arb_fee
        admin_fee = arb_fee - arbs_fee
        if proc == 'Expedited':
            comment2 += (
                'Typically in Expedited arbitration under ICAC Rules a case is'
                ' settled by a sole arbitrator.\nHowever, the estimation is ca'
                'lculated for a panel of three arbitrators.'
            )

    admin_fee = round(admin_fee, 2)
    arbs_fee = round(arbs_fee, 2)
    arb_fee = round(arb_fee, 2)

    result = {
        'reg_fee': reg_fee,
        'admin_fee': admin_fee,
        'arbs_fee': arbs_fee,
        'arb_fee': arb_fee,
        'comment0': comment0,
        'comment1': comment1,
        'comment2': comment2
    }

    return result


def rspp(amount, arbs, proc, parties, measures):

    amount *= usd_to_rub

    reg_fee = rub_to_usd * 30000.0
    comment1 = "The Registration fee is NOT included in the Arbitration fee."

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

    if proc == 'Expedited':
        arb_fee *= 0.7

    if arbs == 3:
        arb_fee *= 1.3

    arbs_fee = 0.3 * arb_fee
    admin_fee = 0.7 * arb_fee

    arbs_fee *= rub_to_usd
    admin_fee *= rub_to_usd
    arb_fee *= rub_to_usd

    arbs_fee15 = arbs_fee * 1.5
    admin_fee15 = admin_fee * 1.5
    arb_fee15 = arb_fee * 1.5

    reg_fee = round(reg_fee, 2)
    arbs_fee = round(arbs_fee, 2)
    arbs_fee15 = round(arbs_fee15, 2)
    admin_fee = round(admin_fee, 2)
    admin_fee15 = round(admin_fee15, 2)
    arb_fee = round(arb_fee, 2)
    arb_fee15 = round(arb_fee15, 2)

    comment2 = (
        f'If the applicable law and the language of arbitration are Russian la'
        f'w and Russian language, arbitartion fee will be {arb_fee} USD.'
    )

    result = {
        'reg_fee': reg_fee,
        'arb_fee': arb_fee15,
        'arbs_fee': arbs_fee15,
        'admin_fee': admin_fee15,
        'comment1': comment1,
        'comment2': comment2
    }

    return result


def ai_chooser2(req, ais, amount, arbs, proc, parties, measures):
    result = []
    for ai in ais:
        if ai.id == 1:
            res = rac_at_rima(amount, arbs, proc, parties, measures)
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
        elif ai.id == 4:
            res = scc(amount, arbs, proc, parties, measures)
            obj = Cost(ai=ai, req=req)
            obj.reg_fee = res['reg_fee']
            obj.arb_fee = res['arb_fee']
            obj.arbs_fee = res['arbs_fee']
            obj.admin_fee = res['admin_fee']
            obj.comment1 = res['comment1']
            obj.comment2 = res['comment2']
            if 'comment0' in res:
                obj.comment0 = res['comment0']
            obj.save()
            result.append(obj)
        elif ai.id == 5:
            res = icc(amount, arbs, proc, parties, measures)
            obj = Cost(ai=ai, req=req)
            obj.reg_fee = res['reg_fee']
            obj.arb_fee = res['arb_fee']
            obj.arbs_fee = res['arbs_fee']
            obj.admin_fee = res['admin_fee']
            obj.comment1 = res['comment1']
            obj.comment2 = res['comment2']
            if 'comment0' in res:
                obj.comment0 = res['comment0']
            obj.save()
            result.append(obj)
        elif ai.id == 6:
            res = rspp(amount, arbs, proc, parties, measures)
            obj = Cost(ai=ai, req=req)
            obj.reg_fee = res['reg_fee']
            obj.arb_fee = res['arb_fee']
            obj.arbs_fee = res['arbs_fee']
            obj.admin_fee = res['admin_fee']
            obj.comment1 = res['comment1']
            obj.comment2 = res['comment2']
            if 'comment0' in res:
                obj.comment0 = res['comment0']
            obj.save()
            result.append(obj)
        elif ai.id == 7:
            res = icac(amount, arbs, proc, parties, measures)
            obj = Cost(ai=ai, req=req)
            obj.reg_fee = res['reg_fee']
            obj.arb_fee = res['arb_fee']
            obj.arbs_fee = res['arbs_fee']
            obj.admin_fee = res['admin_fee']
            obj.comment1 = res['comment1']
            obj.comment2 = res['comment2']
            if 'comment0' in res:
                obj.comment0 = res['comment0']
            obj.save()
            result.append(obj)
        elif ai.id == 8:
            res = dis(amount, arbs, proc, parties, measures)
            obj = Cost(ai=ai, req=req)
            obj.reg_fee = res['reg_fee']
            obj.arb_fee = res['arb_fee']
            obj.arbs_fee = res['arbs_fee']
            obj.admin_fee = res['admin_fee']
            obj.comment1 = res['comment1']
            obj.save()
            result.append(obj)
        elif ai.id == 9:
            res = cietac(amount, arbs, proc, parties, measures)
            obj = Cost(ai=ai, req=req)
            obj.reg_fee = res['reg_fee']
            obj.arb_fee = res['arb_fee']
            obj.arbs_fee = res['arbs_fee']
            obj.admin_fee = res['admin_fee']
            obj.comment1 = res['comment1']
            obj.comment2 = res['comment2']
            obj.save()
            result.append(obj)
        elif ai.id == 10:
            res = viac(amount, arbs, proc, parties, measures)
            obj = Cost(ai=ai, req=req)
            obj.reg_fee = res['reg_fee']
            obj.arb_fee = res['arb_fee']
            obj.arbs_fee = res['arbs_fee']
            obj.admin_fee = res['admin_fee']
            obj.comment1 = res['comment1']
            obj.comment2 = res['comment2']
            obj.save()
            result.append(obj)
        elif ai.id == 11:
            res = aiac(amount, arbs, proc, parties, measures)
            obj = Cost(ai=ai, req=req)
            obj.reg_fee = res['reg_fee']
            obj.arb_fee = res['arb_fee']
            obj.arbs_fee = res['arbs_fee']
            obj.admin_fee = res['admin_fee']
            obj.comment1 = res['comment1']
            obj.save()
            result.append(obj)
    return result


def calculate_cost(request_object):
    ais = request_object.ai.all()
    amount = request_object.amount
    arbs = request_object.arbs
    proc = request_object.proc

    return ai_chooser2(request_object, ais, amount, arbs, proc)
