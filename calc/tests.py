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

        # Create ArbInsts object
        rac = ArbInst.objects.create(arb_inst='RAC (Russia)')

        # Create UserRequest object
        ur1 = UserRequest.objects.create(
            amount=1000000, arbs=3, parties=2, proc='Standard', ea='No')
        ur1.ai.add(rac)

    def test_home(self):
        """ Checks that Home page redirects to Results page if valid data was submitted """
        c = Client()
        response = c.post(
            '', {
                'amount': 1000000,
                'arbs': 3,
                'parties': 2,
                'proc': 'Standard',
                'ea': 'No',
                'ai': [1],
            })

        # test redirect to results page
        self.assertEqual(response.status_code, 302)

    def test_home_invalid(self):
        """ Checks that Home page reloads with error msgs if invalid data was submitted """
        c = Client()
        response = c.post(
            '', {
                'amount': -1,
                'arbs': -1,
                'parties': -9,
                'proc': -1,
                'ea': -1,
                'ai': -1,
            })

        # No redirect to results page
        self.assertEqual(response.status_code, 200)
        # New UserRequest object was not created
        self.assertEqual(UserRequest.objects.all().count(), 1)
        # Error messages are displayed
        self.assertTrue(
            'Ensure this value is greater than or equal to 1' in
            str(response.content))
        self.assertTrue('Select a valid choice' in str(response.content))

    def test_home_userrequest_object(self):
        """ Checks that UserRequest object is created with post data """
        c = Client()
        c.post(
            '', {
                'amount': 1000000,
                'arbs': 3,
                'parties': 2,
                'proc': 'Standard',
                'ea': 'No',
                'ai': [1],
            })

        req = UserRequest.objects.get(pk=2)
        rac = ArbInst.objects.get(pk=1)

        # test UserRequest object creation
        self.assertEqual(UserRequest.objects.all().count(), 2)
        self.assertEqual(req.amount, 1000000)
        self.assertEqual(req.arbs, 3)
        self.assertEqual(req.parties, 2)
        self.assertEqual(req.proc, 'Standard')
        self.assertEqual(req.ea, 'No')
        self.assertEqual(req.ai.first(), rac)

    def test_home_userrequest_costs(self):
        """ Checks that Cost object is created with correct data """
        c = Client()
        c.post(
            '', {
                'amount': 1000000,
                'arbs': 3,
                'parties': 2,
                'proc': 'Standard',
                'ea': 'No',
                'ai': [1],
            })

        req = UserRequest.objects.get(pk=2)

        # test ai chooser and Cost object
        self.assertEqual(req.costs.count(), 1)
        self.assertEqual(req.costs.first().arb_fee, 38700.0)
        self.assertEqual(req.costs.first().arbs_fee, 29600.0)
        self.assertEqual(req.costs.first().admin_fee, 9100.0)
        self.assertEqual(req.costs.first().reg_fee, 500.0)

    def test_results(self):
        """ The Results page shows correct results if last_id is in session """
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
        """ Checks that Result page redirects to Home page if no last_id in session """
        c = Client()
        response = c.get('/results')

        self.assertEqual(response.status_code, 302)
