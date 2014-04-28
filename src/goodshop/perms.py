from goodshop.utils import add_user_context

class MyAdaptorEditInline(object):
    @classmethod
    def can_edit(cls, adaptor_field):
        user = adaptor_field.request.user
        obj = adaptor_field.obj
        can_edit = False
        if user.is_anonymous():
            pass
        elif user.is_superuser:
            can_edit = True
        else:
            add_user_context(adaptor_field.request)
            can_edit = adaptor_field.request.vendor
        return can_edit