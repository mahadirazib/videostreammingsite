from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.db.models import Count
from django.db.models import Q

from . import models
from userAuth.models import userInfo
from . import forms


# Create your views here.
def feedMain(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('userAuth:loginFunction'))


    dict = {}

    currentUser = request.user
    dict.update({'myinfo' : currentUser})
    currentUserMoreInfo = userInfo.objects.get(user__pk = currentUser.id)
    dict.update({'myMoreInfo': currentUserMoreInfo})


    latestVideos = models.videoInfo.objects.all().order_by('-created_at')[:5]
    dict.update({'latestVideos': latestVideos})

    popularVideos = models.comments.objects.values('video').annotate(dcount=Count('comment')).order_by('-dcount')[:5]

    popularVideosArr = []

    for i in popularVideos:
        popvid = models.videoInfo.objects.get(id=i['video'])
        popularVideosArr.append(popvid)

    dict.update({'popularVideos': popularVideosArr})

    userVideo = models.videoInfo.objects.filter(user=currentUser)[:5]
    dict.update({'userVideo': userVideo})
    if len(userVideo)>0:
        dict.update({'usedHasVideo': True})
        


    return render(request, 'feed/feedmain.html', context=dict)











def seeVideo(request, id):

    user = request.user
    
    vid = models.videoInfo.objects.get(pk=id)

    comments = models.comments.objects.filter(video=vid).select_related('user')
    category = models.videoAndCategory.objects.filter(video=vid).select_related('catagory')

    videos = models.videoInfo.objects.all().order_by('-created_at').exclude(id=id)[:6]

    dict = {'vid': vid, 'comments': comments, 'category': category, 'videos': videos }

    if vid.user == user:
        dict.update({'author': True})

    if request.method == "POST":

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('userAuth:loginFunction'))

        usr = request.user
        cmnt = request.POST.get('comment').strip()

        if cmnt != "" and cmnt != None:
            obj = models.comments(video=vid, user = usr, comment=cmnt)
            obj.save()


    return render(request, 'feed/videopage.html', context=dict)










@login_required
def uploadVideo(request):
    user = request.user

    vidinfo = forms.videoInfoForm()
    vidCategory = forms.videoCategoryForm()

    diction = {'videoInfo': vidinfo, 'videoCategory': vidCategory}


    if request.method == 'POST':

        info = forms.videoInfoForm(data=request.POST)
        category = forms.videoCategoryForm(data=request.POST)

        categories = request.POST.getlist('catagory')

        if info.is_valid() and len(categories)>0:

            user = request.user
            video = request.POST.get('video')
            title = request.POST.get('title')
            desc = request.POST.get('description')

            obj = models.videoInfo(user=user, video=video, title=title, description=desc)
            obj.save()

            vid = models.videoInfo.objects.get(user=user, video=video, title=title, description=desc)
            for i in categories:
                cat = models.catagory.objects.get(id=i)
                obj = models.videoAndCategory(video=vid, catagory=cat)
                obj.save()
            
            return HttpResponseRedirect(reverse('feed:feedMain'))


    return render(request, 'feed/uploadVideo.html', context=diction)









@login_required
def editVideo(request, id):
    user = request.user

    vid = models.videoInfo.objects.get(id=id)
    if vid.user != user:
        return HttpResponseRedirect(reverse('feed:seeVideo', kwargs={ 'id': id }))


    info = forms.videoInfoForm(instance=vid)
    vidCategory = forms.videoCategoryForm()
    diction = {'videoInfo': info, 'videoCategory': vidCategory, 'edit': True}

    if request.method == 'POST':

        info = forms.videoInfoForm(data=request.POST)
        category = forms.videoCategoryForm(data=request.POST)

        categories = request.POST.getlist('catagory')

        if info.is_valid() and len(categories)>0:

            user = request.user
            video = request.POST.get('video')
            title = request.POST.get('title')
            desc = request.POST.get('description')

            obj = models.videoInfo.objects.get(id=id)
            obj.video = video
            obj.title = title
            obj.description = desc
            obj.save()

            models.videoAndCategory.objects.filter(video=vid).delete()

            for i in categories:
                cat = models.catagory.objects.get(id=i)
                obj = models.videoAndCategory(video=vid, catagory=cat)
                obj.save()

            return HttpResponseRedirect(reverse('feed:seeVideo', kwargs={ 'id': id }))

    return render(request, 'feed/uploadVideo.html', context=diction)









@login_required
def deletVideo(request, id):
    user = request.user

    vid = models.videoInfo.objects.get(id=id)
    if vid.user != user:
        return HttpResponseRedirect(reverse('feed:seeVideo', kwargs={ 'id': id }))
    

    vid.delete()

    return HttpResponseRedirect(reverse('feed:feedMain'))










def videosOnSearch(request):

    dict = {}

    find = request.GET.get('find')
    cat = request.GET.get('category')
    popular = request.GET.get('popular')
    uservideo = request.GET.get('uservideo')


    videos = models.videoInfo.objects.all()[:20]
    dict.update({'videos': videos})

    categories = models.catagory.objects.all()
    dict.update({'category': categories})


    if find != '' and find !=None:

        find = find.strip()

        categoryid = 0
        findInCategory = False

        for i in categories:
            if(find.lower() == i.title.lower()):
                categoryid = i.id
                findInCategory = True


        videos = models.videoInfo.objects.filter(Q(title__icontains=find) | Q(description__icontains=find))
        videosFromCategoryAndVideo = ''
        if findInCategory:
            objForCategory = models.catagory.objects.get(id=categoryid)
            videosFromCategoryAndVideo = models.videoAndCategory.objects.filter(catagory=objForCategory).select_related('video')

            videoids = []
            videos = list(videos)

            for i in videos:
                videoids.append(i.id)
            
            for i in videosFromCategoryAndVideo:
                if i.video.id not in videoids:
                    videos.append(i.video)


        dict.update({'videos': videos})
        dict.update({'search': find})


    else:

        if cat:
            category = models.catagory.objects.get(id=cat)
            videos = models.videoAndCategory.objects.filter(catagory=category).select_related('video')
            mainVideoArr = []
            dict.update({'search': category.title})

            for i in videos:
                mainVideoArr.append(i.video)

            dict.update({'videos': mainVideoArr, 'active': category.title})

        elif popular:
            popularVideos = models.comments.objects.values('video').annotate(dcount=Count('comment')).order_by('-dcount')
            popularVideosArr = []
            for i in popularVideos:
                popvid = models.videoInfo.objects.get(id=i['video'])
                popularVideosArr.append(popvid)
            dict.update({'videos': popularVideosArr})
            dict.update({'search': 'Popular', 'popular': True})

        elif uservideo:
            user = request.user
            userVideos = models.videoInfo.objects.filter(user=user)

            dict.update({'videos': userVideos})
            dict.update({'search': 'Your Videos', 'uservideo': True})


        else:
            latestVideos = models.videoInfo.objects.all().order_by('-created_at')
            dict.update({'videos': latestVideos})



    return render(request, 'categoryAndSearch/singleCategoryPage.html', context=dict)












