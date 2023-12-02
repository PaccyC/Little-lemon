from django.shortcuts import render
from .models import UserComments
from .forms import CommentForm
from django.http import JsonResponse

# Create your views here.

def form_view(request):
    form = CommentForm()
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            # clean_data is a method that helps in data normalization
            cd = form.cleaned_data
            
            uc = UserComments(
                first_name=cd["first_name"],
                last_name=cd["last_name"],
                comment=cd["comment"],
            )
            
            uc.save()
            return JsonResponse({
                'message':'success'
                    })
            
    return render(request,'blog.html',{'form':form})        

      
        