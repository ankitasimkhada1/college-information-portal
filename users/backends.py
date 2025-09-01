# from django.contrib.auth.backends import ModelBackend
# from .models import CustomUser

# class CustomBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             user = CustomUser.objects.get(email=username) or CustomUser.objects.get(phone_number=username) or CustomUser.objects.get(username=username)
#             if user.check_password(password):
#                 return user
#         except CustomUser.DoesNotExist:
#             return None


from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username) or CustomUser.objects.get(phone_number=username)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None