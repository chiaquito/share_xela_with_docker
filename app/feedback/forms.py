from django import forms
from feedback.models import Feedback


class FeedbackModelForm(forms.ModelForm):

    class Meta:
        model  = Feedback
        fields = ( 'content', 'level',) #'evaluator',
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs["class"] = "form-control" 
        self.fields["content"].widget.attrs["rows"]  = "6"
        self.fields["content"].widget.attrs["size"]  = "6"
        self.fields["level"].widget.attrs["class"] = "form-control" 


