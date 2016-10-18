from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

def pag(request,name,num):
    paginator = Paginator(name, num)
    d = [i for i in xrange(1, paginator.num_pages + 1)]
    page = request.GET.get('page')
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return d,result