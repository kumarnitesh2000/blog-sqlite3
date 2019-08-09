from django.shortcuts import render,get_object_or_404
from .models import PublishedManager,Post,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import EmailPost,CommentForm,SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank,TrigramSimilarity
from .serializers import PostSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
def post_list(request,tag_slug=None):

    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        #object_list = object_list.filter(tags__name__in=[tag])
        object_list = object_list.filter(tags__in=[tag])

    paginater=Paginator(object_list,2)

    page=request.GET.get('page')
    try:
        posts=paginater.page(page)


    except PageNotAnInteger:
        posts=paginater.page(1)


    except EmptyPage:
        posts=paginater.page(paginater.num_pages)

    #postsa = Post.published.filter(tags__name__in=[tag])

    context={'page':page,'tag':tag,'posts':posts}
    template = 'blog/index.html'

    return render(request,template,context)

def post_detail(request,year,month,day,post):
    posts=get_object_or_404(Post,
                    publish__year=year,publish__month=month,publish__day=day,slug=post)
    #list of active comments for this post
    comments = posts.comments.filter(active=True)

    new_comment=None
    if request.method=='POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            #now assign the comment only to the current post
            new_comment.post=posts
            new_comment.save()
    else:
        comment_form=CommentForm()
    post_tags_id=posts.tags.values_list('id',flat=True)
    similar_post=Post.published.filter(tags__in=post_tags_id).exclude(id=posts.id)
    similar_post=similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    #similar_post=.exclude(id=posts.id)
    print(similar_post)
    context = {'similar_post':similar_post,'posts': posts,'comment_form':comment_form,'comments':comments,'new_comment':new_comment}
    template = 'blog/detail.html'
    return render(request, template, context)

def post_share(request,post_id):

    post=get_object_or_404(Post,status='published',id=post_id)
    sent = False
    not_connect=False
    form = EmailPost()
    if request.method == 'POST':
        form=EmailPost(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            print(f'hello register user {name}')
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],cd['email'],post.title)
            message = 'READ "{}" at {}\n\n{}\'s comments : {}'.format(post.title,post_url,cd['name'],cd['comments'])
            #send_mail(subject,message,cd['email'],cd['to'])
            try:
               send_mail(subject,message,'kumarnitesh2000.nk@gmail.com',[cd['to']])
               sent=True
            except:

                not_connect=True



    else:
        form=EmailPost()
    context = {'form':form,'post':post,'sent':sent,'not_connect':not_connect}
    template = 'blog/share.html'
    return render(request,template,context)

def filter(request):
    posts = Post.published.get(id=1)
    object_list=Post.published.all()
    print(posts)
    print(posts.id)
    #posta= Post.published.filter(tags__name__in=['python'])
    #posts=posts.tag.all()
    c=1

    for tag in posts.tags.all():
        print( f'({c}) {tag} with the id {tag.id}')
        c=c+1
    template = 'blog/test.html'
    context = {'posts':posts}

    return render(request,template,context)


def post_search(request):
    query=None
    context=None
    results=None
    trigram_results=None
    result=None
    form=SearchForm()
    if 'query' in request.GET:
        form=SearchForm(request.GET)
        if form.is_valid():
            query=form.cleaned_data['query']
            print(query)
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            result=Post.published.annotate(search=search_vector,rank=SearchRank(search_vector,search_query)).filter(search=search_query).order_by('-rank')
            trigram_results=Post.published.annotate(similarity=TrigramSimilarity('title',query)).filter(similarity__gt=0.3).order_by('-similarity')
    context={'form':form,'results':trigram_results,'result':result,'query':query}
    template='blog/search.html'
    return render(request,template,context)


class Postlist():
    def get(self):
        post=Post.published.all()
        serial=PostSerializer(post,many=True)
        return Response(serial.data)
    def post(self):
        pass



'''
            results=Post.published.annotate(search=SearchVector('title','body')).filter(search=query)
            #now code to search according to certain ranking
            search_vector=SearchVector('title','body')
            search_query=SearchQuery(query)
            result=Post.published.annotate(search=search_vector,rank=SearchRank(search_vector,search_query)).filter(search=search_query).order_by('-rank')
           #trigram_results=Post.published.annotate(similarity=TrigramSimilarity(('title','body
'''