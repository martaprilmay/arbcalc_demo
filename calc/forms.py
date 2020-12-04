from django import forms
from django.forms import ModelForm
from .models import UserRequest, UserRequestRu, ArbInst, ArbInstRu


class RequestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['ai'].widget = forms.CheckboxSelectMultiple(
            choices=self.fields['ai'].choices
        )
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

    def __init__(self, *args, **kwargs):
        super(RequestFormRu, self).__init__(*args, **kwargs)
        self.fields['ai'].widget = forms.CheckboxSelectMultiple(
            choices=self.fields['ai'].choices
        )
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


# PROCEDURE = ["Standard", "Expedited"]
# NUMBER = ["1", "3", "5", "7"]
# INSTITUTIONS = ["RAC at RIMA", "ICC", "SCC"]


# class CalcForm(forms.Form):
#     dispute_ammount = forms.FloatField(
#         required=True,
#         min_value=1.0,
#         label="Ammount in Dispute"
#     )
#     number_of_arbitrators = forms.ChoiceField(
#         # required=True,
#         choices=NUMBER,
#         widget=forms.Select,
#         label='Number of Arbotrators'
#     )
#     type_of_procedure = forms.ChoiceField(
#         # required=True,
#         choices=PROCEDURE,
#         widget=forms.RadioSelect,
#         label="Type of Procedure"
#     )
#     arbitral_institution = forms.MultipleChoiceField(
#         # required=True,
#         widget=forms.CheckboxSelectMultiple,
#         choices=INSTITUTIONS,
#         label="Type of Procedure"
#     )
