from django import forms
from django.forms import ModelForm
from .models import UserRequest, UserRequestRu, ArbInst, ArbInstRu


class RequestForm(forms.ModelForm):
    """ A form with all parameters of a dispute.
        Based on UserRequest Model.
        All fields are required
    """
    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        # Change ai field widget from Select to CheckboxSelectMultiple
        self.fields['ai'].widget = forms.CheckboxSelectMultiple(
            choices=self.fields['ai'].choices
        )
        # Change the order of Arbitral institutions
        self.fields['ai'].queryset = ArbInst.objects.order_by('arb_inst')

    class Meta:
        model = UserRequest
        ordering = ['ArbInst__arb_inst']
        labels = {
            "amount": "Ammount in Dispute (USD)",
            "arbs": "Number of Arbitrators",
            "proc": "Type of Procedure",
            "ai": "Arbitral Institution",
            "ea": "Emergency Measures",
            "parties": "Number of Parties",
        }
        fields = ['amount', 'arbs', 'parties', 'proc', 'ea', 'ai']


class RequestFormRu(forms.ModelForm):
    """ A form with all parameters of a dispute.
        Based on UserRequestRu Model.
        All fields are required
    """
    def __init__(self, *args, **kwargs):
        super(RequestFormRu, self).__init__(*args, **kwargs)
        # Change ai field widget from Select to CheckboxSelectMultiple
        self.fields['ai'].widget = forms.CheckboxSelectMultiple(
            choices=self.fields['ai'].choices
        )
        # Change the order of Arbitral institutions
        self.fields['ai'].queryset = ArbInstRu.objects.order_by('arb_inst')

    class Meta:
        model = UserRequestRu
        ordering = ['ArbInst__arb_inst']
        labels = {
            "amount": "Сумма требований",
            "arbs": "Кол-во арбитров",
            "proc": "Вид процедуры",
            "type": "Вид спора",
            "ai": "Арбитражное учреждение",
        }
        fields = ['amount', 'arbs', 'proc', 'type', 'ai']
