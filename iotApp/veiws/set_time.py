from django import forms
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError   
from ..models import setting
from django.contrib import messages
from iotApp.middleware import login_required

class SettingForm(forms.ModelForm):
    class Meta:
        model = setting
        fields = ['hour_norm', 'late_time']
    
    widgets = {
        'hour_norm': forms.NumberInput(attrs={'class': 'form-control'}),
        'late_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM'}),
    }

    def clean_hour_norm(self):
        hour_norm = self.cleaned_data.get('hour_norm')
        if hour_norm < 1:
            raise ValidationError("最小小時必需大於1小時")
        return hour_norm
    
    def clean_late_time(self):
        late_time = self.cleaned_data.get('late_time')
        if not late_time:
            raise ValidationError("遲到時間不得為空")
        return late_time

@login_required
def set_time(request):
    try:
        # Attempt to retrieve the existing setting from the database
        existing_setting = setting.objects.first()
    except setting.DoesNotExist:
        existing_setting = None

    if request.method == 'POST':
        form = SettingForm(request.POST, instance=existing_setting)
        if form.is_valid():
            form.save()
            messages.success(request, "設定成功")
        else:
            error_messages = []
            for field, errors in form.errors.items():
                error_messages.extend(errors)
            
            for error_message in error_messages:
                messages.error(request, error_message)
    else:
        # If no existing_setting found, create a new form
        form = SettingForm(instance=existing_setting)
    
    return render(request, 'leader/set_time.html', {'form': form})