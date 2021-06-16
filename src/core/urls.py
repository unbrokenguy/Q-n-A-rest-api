from rest_framework.routers import SimpleRouter

from core.views import AuthenticationViewSet

app_name = "core"

router = SimpleRouter()
router.register("auth", AuthenticationViewSet, basename="auth")
urlpatterns = []

urlpatterns += router.urls
