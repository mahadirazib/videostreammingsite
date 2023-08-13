from django import forms
from django.contrib.auth.models import User
from . import models




class videoInfoForm(forms.ModelForm):
    
    class Meta():
        model = models.videoInfo
        fields = ('video', 'title', 'description')

    def __init__(self, *args, **kwargs): 
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        self.fields['video'].widget.attrs = ({'class': 'form-control', 'placeholder': "Video Url"})
        self.fields['title'].widget.attrs = ({'class': 'form-control', 'placeholder': "Video Title"})
        self.fields['description'].widget.attrs = ({'class': 'form-control', 'placeholder': "Description"})




class videoCategoryForm(forms.ModelForm):

    objs = models.catagory.objects.all().order_by('title')
    arr = []

    for i in objs:
        arr.append([i.id, i.title])

    catagory = forms.MultipleChoiceField(choices=arr)
    
    class Meta():
        model = models.videoAndCategory
        fields = ('catagory',)

    def __init__(self, *args, **kwargs): 
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        self.fields['catagory'].widget.attrs = ({'class': 'form-control'})





