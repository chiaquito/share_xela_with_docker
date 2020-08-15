from django import forms
from feedback.models import Feedback


class FeedbackModelForm(forms.ModelForm):

    class Meta:
        model  = Feedback
        fields = ( 'content', ) #'evaluator', 'level',
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs["class"] = "form-control mt-1" 
        self.fields["content"].widget.attrs["rows"]  = "6"
        self.fields["content"].widget.attrs["size"]  = "6"
        self.fields["content"].widget.attrs['required'] = 'required'
        #self.fields["level"].widget.attrs["class"] = "form-control" 
        #self.fields["level"].widget.attrs["type"] = "hidden"
        #self.fields["level"].widget.attrs["type"] = "hidden"
        #self.fields["level"].widget.attrs["value"] = 3
        #self.fields['level'].widget = forms.HiddenInput()



