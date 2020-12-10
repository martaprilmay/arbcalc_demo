from django.test import Client, TestCase
from .models import ArbInst, Rate, UserRequest
from .utils.arbitration import ai_chooser


# Create your tests here
class CalcTestCase(TestCase):

    def setUp(self):

        self.client = Client()

        # Create Rates
        Rate.objects.create(name='USD_EUR', rate=1)
        Rate.objects.create(name='EUR_USD', rate=1)
        Rate.objects.create(name='RUB_USD', rate=1)
        Rate.objects.create(name='USD_RUB', rate=1)
        # Rate.objects.create(name='USD_CNY', rate=1)
        # Rate.objects.create(name='CNY_USD', rate=1)
        # Rate.objects.create(name='USD_HKD', rate=1)
        # Rate.objects.create(name='HKD_USD', rate=1)
        # Rate.objects.create(name='SGD_USD', rate=1)
        # Rate.objects.create(name='USD_SGD', rate=1)
        # Rate.objects.create(name='KRW_USD', rate=1)
        # Rate.objects.create(name='USD_KRW', rate=1)

        # Create ArbInsts
        rac = ArbInst.objects.create(arb_inst='RAC (Russia)')
        # ArbInst.objects.create(name='HKIAC (China)')
        # ArbInst.objects.create(name='SIAC (Singapore)')
        # ArbInst.objects.create(name='SCC (Sweden)')
        # ArbInst.objects.create(name='ICC (France)')
        # ArbInst.objects.create(name='RSPP (Russia)')
        # ArbInst.objects.create(name='ICAC (Russia)')
        # ArbInst.objects.create(name='DIS (Germany)')
        # ArbInst.objects.create(name='CIETAC (China)')
        # ArbInst.objects.create(name='VIAC (Austria)')
        # ArbInst.objects.create(name='AIAC (Malaysia)')
        # ArbInst.objects.create(name='KCAB (South Korea)')

        # Create UserRequest
        ur1 = UserRequest.objects.create(
            amount=1000000, arbs=3, parties=2, proc='Standard', ea='No')
        ur1.ai.add(rac)

    def test_home(self):
        rac = (ArbInst.objects.get(pk=1),)
        c = Client()
        response = c.post(
            '', {
                'amount': 1000000,
                'arbs': 3,
                'parties': 2,
                'proc': 'Standard',
                'ea': 'No',
                'ai': rac,
            })

        req = UserRequest.objects.get(pk=1)

        # test redirect
        self.assertEqual(response.status_code, 302)
        # test UserRequest object creation
        self.assertEqual(req.amount, 1000000)
        self.assertEqual(req.arbs, 3)
        self.assertEqual(req.parties, 2)
        self.assertEqual(req.proc, 'Standard')
        self.assertEqual(req.ea, 'No')
        self.assertEqual(req.ai, 'RAC (Russia)')
        # test ai chooser
        self.assertEqual(req.costs.count(), 1)
        self.assertEqual(req.costs.first().arb_fee, 38700.0)
        self.assertEqual(req.costs.first().arbs_fee, 29600.0)
        self.assertEqual(req.costs.first().admin_fee, 9100.0)
        self.assertEqual(req.costs.first().reg_fee, 500.0)

    def test_results(self):
        '''The Results page shows correct results if last_id is in session.'''
        # Create Cost object
        ur1 = UserRequest.objects.get(pk=1)
        rac = (ArbInst.objects.get(pk=1),)
        ai_chooser(ur1, rac, 1000000, 3, "Standard", 2, "No")

        # setup test client and session
        session = self.client.session
        session['last_id'] = 1
        session.save()

        response = self.client.get('/results')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['amount'], 1000000)
        self.assertEqual(len(response.context['result']), 1)
        self.assertEqual(response.context['result'][0].arb_fee, 38700.0)
        self.assertEqual(response.context['result'][0].arbs_fee, 29600.0)
        self.assertEqual(response.context['result'][0].admin_fee, 9100.0)
        self.assertEqual(response.context['result'][0].reg_fee, 500.0)

    def test_results_redirect(self):
        '''The Result page redirects if no last_id in session'''
        c = Client()
        response = c.get('/results')

        self.assertEqual(response.status_code, 302)

    def test_about(self):
        c = Client()
        response = c.get('/about')
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        c = Client()
        response = c.get('')
        self.assertEqual(response.status_code, 200)
