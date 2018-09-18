from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import LikeRecord, LikeCount

# 操作成功返回结果
def SuccessResponse(like_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['like_num'] = like_num
    return JsonResponse(data)

# 数据错误返回结果
def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

# 点赞或取消点赞
def like_change(request):
    # 获取数据
    user = request.user
    # 判断用户是否登录
    if not user.is_authenticated:
        return ErrorResponse(4000, '对不起！您尚未登录，不能点赞！')

    contentType = request.GET.get('content_type')
    object_id = request.GET.get('object_id')

    try:
        # 多想获取，可能会出错
        content_type = ContentType.objects.get(model=contentType)
        model_class = content_type.model_class()
        model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(4001, '抱歉，点赞对象不存在！')

    is_like = request.GET.get('is_like')

    # 处理数据
    if is_like == 'true':
        # 要点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            # 未点赞过，要进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else:
            # 已点赞，不能重复点赞
            return ErrorResponse(4002, '您已点赞过，不能重复点赞！')
    else:
        # 要取消点赞
        # 判断是否点赞过
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user):
            # 有点赞过，取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            # 点赞总数 -1
            # 查找点赞总数是否存在
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                # 存在点赞总数 -1
                like_count.liked_num -= 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                return ErrorResponse(4004, '数据错误！')
        else:
            # 没有点赞过，不能取消
            return ErrorResponse(4003, '您还未点赞过，不能取消！')

