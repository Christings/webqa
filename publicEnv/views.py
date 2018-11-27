from django.shortcuts import render

# Create your views here.

def deadlink(request):
    # user_id = 'zhangjingjun'
    # user_id = request.COOKIES.get('uid')
    # if request.method == 'GET':
    #     page = request.GET.get('page')
    #     current_page = 1
    #     if page:
    #         current_page = int(page)
    #     try:
    #         task_list = models.InterfaceEval.objects.order_by('id')[::-1]
    #         page_obj = pagination.Page(current_page, len(task_list), 16, 9)
    #         data = task_list[page_obj.start:page_obj.end]
    #         page_str = page_obj.page_str("/fanyi/interface?page=")
    #     except Exception as e:
    #         print(e)
    #         pass
    #     return render(request, 'fanyi/interface.html', {'user_id': user_id, 'li': data, 'page_str': page_str})
    return render(request, 'public/debug.html.html')


def svcheck(request):
    # user_id = 'zhangjingjun'
    # user_id = request.COOKIES.get('uid')
    # if request.method == 'GET':
    #     page = request.GET.get('page')
    #     current_page = 1
    #     if page:
    #         current_page = int(page)
    #     try:
    #         task_list = models.InterfaceEval.objects.order_by('id')[::-1]
    #         page_obj = pagination.Page(current_page, len(task_list), 16, 9)
    #         data = task_list[page_obj.start:page_obj.end]
    #         page_str = page_obj.page_str("/fanyi/interface?page=")
    #     except Exception as e:
    #         print(e)
    #         pass
    #     return render(request, 'fanyi/interface.html', {'user_id': user_id, 'li': data, 'page_str': page_str})
    return render(request, 'public/debug.html.html')