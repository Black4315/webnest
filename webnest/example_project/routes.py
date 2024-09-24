from webnest.urls import route 
from webnest.shortcuts import render

def index(request): 
    return render('index.html',context={'Title':'webnest package'})


urls = [
    route('',index, name='index'), 
]

