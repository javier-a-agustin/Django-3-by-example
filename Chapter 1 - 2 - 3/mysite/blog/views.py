from django.core.mail import send_mail
from django.db.models import Count
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm
from .models import Post


class PostListView(ListView):
    """Class to display the list of all published posts"""

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"

    def get_queryset(self):
        """
        Return the queryset that will be displayed
        If there are tags, the queryset will be filtered by tags.
        If there are not tags, it will return all published posts.
        """
        tag_slug = self.kwargs.get("tag_slug", None)
        self.tag = None
        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            self.queryset = self.queryset.filter(tags__in=[self.tag])
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context


class PostDetailView(FormView, DetailView):
    model = Post
    form_class = CommentForm

    def get_success_url(self):
        object = self.get_object()
        return reverse(
            "blog:post_detail",
            kwargs={"slug": object.slug},
        )

    def form_valid(self, form: CommentForm) -> HttpResponse:
        post = self.get_object()
        comment = form.save(commit=False)
        comment.post_id = post
        comment.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # List of similar posts
        post = self.get_object()
        post_tags_ids = post.tags.values_list("id", flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(
            id=post.id
        )
        similar_posts = similar_posts.annotate(
            same_tags=Count("tags")
        ).order_by("-same_tags", "-publish")[:4]
        context = super().get_context_data(**kwargs)
        context["similar_posts"] = similar_posts
        return context


class PostShareView(FormView, DetailView):
    template_name = "blog/post_share.html"
    form_class = EmailPostForm
    model = Post

    def form_valid(self, form, **kwargs):
        post = self.get_object()
        # Form fields passed validation
        cd = form.cleaned_data
        post_url = self.request.build_absolute_uri(post.get_absolute_url())
        subject = f"{cd['name']} recommends you read {post.title}"
        message = f"Read {post.title} at {post_url}\n\n {cd['name']}'s \
            comments: {cd['comments']}"
        try:
            send_mail(
                subject,
                message,
                "admin@myblog.com",
                [cd["to"]],
            )
            sent = True
        except Exception:
            sent = False
        self.object = self.get_object()
        return self.render_to_response(
            self.get_context_data(form=form, sent=sent)
        )

    def get_success_url(self) -> str:
        object = self.get_object()
        return reverse(
            "blog:post_share",
            kwargs={"slug": object.slug},
        )


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
