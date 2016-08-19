def not_null_none(**kwargs):
    list_arg ={}
    for key, value in kwargs.items():
        if value is u"" or value is "":
            pass
        elif key == "start_time":
            list_arg["start_time"+"__gte"]=str(value)
        elif key == "start_time_2":
            list_arg["start_time"+"__lt"]=str(value)
        elif key == "finish_time":
            list_arg["finish_time"+"__gte"]=str(value)
        elif key == "finish_time_2":
            list_arg["finish_time"+"__lt"]=str(value)
        else:
            list_arg[key] = str(value)
    return list_arg

def permission_base(user):
    if user == 'admin':
        user_manage = {
            'base': "",
        }
        live_manage = {
            'base': "",
            'op': "",
            "edit": ""
        }
        node_manage = {
            'base': "",
            'op': ""
        }
        op_manage = {
            'base': ""
        }
    elif user == 'user':
        user_manage = {
            'base': "none"
        }
        live_manage = {
            'base': "",
            'op': "",
            "edit": ""
        }
        node_manage = {
            'base': "",
            'op': "none"
        }
        op_manage = {
            'base': "none"
        }
    elif user == 'guest':
        user_manage = {
            'base': "none"
        }
        live_manage = {
            'base': "",
            'op': "none",
            "edit": "none"
        }
        node_manage = {
            'base': "",
            'op': "none"
        }
        op_manage = {
            'base': "none"
        }
    return user_manage, live_manage, node_manage, op_manage

if __name__ == "__main__":

    # list_dd = not_null_none(a="aa",b="",c=u"",d="11",start_time="1",start_time_2="2",finish_time="1",finish_time_2="3")
    # print list_dd
    a,b,c,d = permission_base('user')
    print a, b, c, d