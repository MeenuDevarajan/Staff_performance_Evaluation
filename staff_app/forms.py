from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()
    data_type = forms.ChoiceField(choices=[
        ('time', 'Time Tracking Data'),
        ('activity', 'Activity Level Data')
    ])

class PerformanceForm(forms.Form):
    total_hours = forms.FloatField(label='Total Hours Worked')
    activity_percentage = forms.FloatField(label='Activity Percentage')