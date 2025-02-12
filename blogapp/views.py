from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from blogapp.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST




# def post_list(request):
#     post_list = Post.objects.all()
#     paginator = Paginator(post_list, 2)
#     page_number = request.GET.get('page', 1)

#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blogapp\post\list.html', {'posts': posts})

class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    paginate_by = 2
    template_name = 'blogapp\post\list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post, 
                             publish__year=year, 
                             publish__month=month, 
                             publish__day=day, 
                        )
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    return render(request, 'blogapp/post/detail.html', {'post': post, 'comments': comments, 'form': form})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        #Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} \n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'haneen.hamchou@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blogapp/post/share.html', {'post': post, 'form': form, 'sent': sent})
    
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the DB
        comment = form.save(commit=False)
        # Assign the post to the Comment
        comment.post = post
        # Save the Comment to the DB
        comment.save()
    return render(request, 'blogapp/post/comment.html', {'post':post, 'form':form, 'comment':comment})