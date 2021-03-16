from django.contrib import admin
from .models import (Message, 
                     MessageDelay,
                     TokenBot,
                     UserTelegram,
                     AnswerUser)


admin.site.register(Message)
admin.site.register(AnswerUser)
admin.site.register(UserTelegram)
admin.site.register(MessageDelay)
admin.site.register(TokenBot)
