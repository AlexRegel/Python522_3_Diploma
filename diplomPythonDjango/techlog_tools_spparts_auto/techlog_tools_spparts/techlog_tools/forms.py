from django.forms import ModelForm
from telog_spparts.models import Repairs


class RepairsForm(ModelForm):
    class Meta:
        model = Repairs
        fields = ['title', 'rep_memo', 'priority_rep']
