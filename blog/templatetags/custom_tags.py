from django import template
from blog.models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
register = template.Library()
@register.simple_tag(name='count')
def total_posts_written():
    return Post.published.count()

@register.inclusion_tag('blog/latest_post.html')
def show_latest_post(count=3):
    latest_post=Post.published.order_by('-publish')[:count]
    return {'latest_post':latest_post}

@register.inclusion_tag('blog/most_comment.html')
def most_commented(count=3):
    most_commented_post=Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    return {'most_commented_post':most_commented_post}

@register.filter(name='markdown')
def markddown_format(text):
    return mark_safe(markdown.markdown(text))