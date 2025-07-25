from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from feedbackapp.views import AdminViewset,CustomerViewset, ManagerViewset, FeedbackViewset, ReplyViewset

router = routers.DefaultRouter()
router = routers.SimpleRouter(trailing_slash=False)
router.register('Ad', AdminViewset)
router.register('customer', CustomerViewset)
router.register('managers', ManagerViewset)
router.register('feedback', FeedbackViewset)
router.register('reply', ReplyViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    # path('feedbackapp/', include(a'feedbackapp.urls')),
    path('rest_framework',include('rest_framework.urls',namespace='rest_framework'))
]
