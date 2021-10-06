### Django function based view import ###
from typing import Any, Dict
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.urls import reverse

### Django classes based views import ###
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormView

### Import models ###
from .models import Post

### Import formds ###
from .forms import EmailPostForm, CommentForm

class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'blog/post/list.html'

class PostDetailView(FormView, DetailView):	
    model           = Post
    form_class      = CommentForm

    def get_success_url(self):
        object      = self.get_object()
        return reverse('blog:post_detail', kwargs={'slug': object.slug})
    
    def form_valid(self, form: CommentForm) -> HttpResponse:
        post            = self.get_object()
        comment         = form.save(commit=False)
        comment.post_id = post
        comment.save()
        return super().form_valid(form)


class PostShareView(FormView, DetailView):
    template_name   = 'blog/post_share.html'
    form_class      = EmailPostForm
    model           = Post

    def form_valid(self, form, **kwargs):
        post = self.get_object()
        # Form fields passed validation
        cd = form.cleaned_data
        post_url = self.request.build_absolute_uri(post.get_absolute_url())
        subject = f"{cd['name']} recommends you read {post.title}"
        message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
        try:
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
        except Exception as e:
            sent = False
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(form=form, sent=sent))

    def get_success_url(self) -> str:
        object      = self.get_object()
        return reverse('blog:post_share', kwargs={'slug': object.slug})




# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 1) # 3 posts in each page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     return render(request,
#                   'blog/post/list.html',
#                    {'page': page,
#                     'posts': posts})

# def post_share(request, post_id):
#     # Retrieve post by id
#     post = get_object_or_404(Post, id=post_id, status='published')
#     if request.method == 'POST':
#         # Form was submitted
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             # Form fields passed validation
#             cd = form.cleaned_data
#             # ... send email
#     else:
#         form = EmailPostForm()
#     return render(request, 'blog/post/share.html', {'post': post,
#                                                     'form': form})


# def post_detail(request, year, month, day, post):
# 	post = get_object_or_404(Post, slug=post,
# 								   status='published',
# 								   publish__year=year,
# 								   publish__month=month,
# 								   publish__day=day)
# 	return render(request, 'blog/post/detail.html', {'post': post})