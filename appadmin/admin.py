from django.contrib import admin
from .models import (Question,
                    Message,
                    Sequence_Logic,
                    User_Sequence_Logic)

admin.site.register(Question)
admin.site.register(Message)
admin.site.register(Sequence_Logic)
admin.site.register(User_Sequence_Logic)