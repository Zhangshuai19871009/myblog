import datetime
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache

from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from blog.models import Blog

# 过去7天内热门博客
def get_seven_days_hot_blogs():
    today = timezone.now().date()
    seven_days = today - datetime.timedelta(days=7)
    blogs = Blog.objects\
            .filter(read_details__date__lt=today, read_details__date__gte=seven_days)\
            .values('id', 'title')\
            .annotate(read_num_sum=Sum('read_details__read_num'))\
            .order_by('-read_num_sum')
    return blogs[:7]

# 过去30天内热门博客
def get_month_hot_blogs():
    today = timezone.now().date()
    seven_days = today - datetime.timedelta(days=30)
    blogs = Blog.objects\
            .filter(read_details__date__lt=today, read_details__date__gte=seven_days)\
            .values('id', 'title')\
            .annotate(read_num_sum=Sum('read_details__read_num'))\
            .order_by('-read_num_sum')
    return blogs[:7]

# 首页
def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    # 获取7天热门博客的缓存数据
    seven_days_hot_blogs = cache.get('seven_days_hot_blogs')
    month_hot_blogs = cache.get('month_hot_blogs')
    if seven_days_hot_blogs is None:
        seven_days_hot_blogs = get_seven_days_hot_blogs()
        cache.set('seven_days_hot_blogs', seven_days_hot_blogs, 3600)
        print('7 calc')
    else:
        print('7 use cache')
    if month_hot_blogs is None:
        month_hot_blogs = get_month_hot_blogs()
        cache.set('month_hot_blogs', month_hot_blogs, 3600)
        print('30 calc')
    else:
        print('30 use cache')

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['seven_days_hot_blogs'] = seven_days_hot_blogs
    context['month_hot_blogs'] = month_hot_blogs
    return render(request, 'home.html', context)
