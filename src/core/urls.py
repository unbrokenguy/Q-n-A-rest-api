from rest_framework.routers import SimpleRouter

from core.views import AuthenticationViewSet, HashTagViewSet, TicketViewSet

app_name = "core"

router = SimpleRouter()
router.register("auth", AuthenticationViewSet, basename="auth")
router.register("ticket", TicketViewSet, basename="ticket")
router.register("hash_tag", HashTagViewSet, basename="hash_tag")
urlpatterns = []

urlpatterns += router.urls
