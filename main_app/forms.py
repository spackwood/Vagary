from django.forms import ModelForm
from .models import Suitcase

class LuggageForm(ModelForm):
    class Meta:
        model = Suitcase
        fields = ['item_name', 'quantity']