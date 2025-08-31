from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_scion'

router = NetBoxRouter()
router.register('organizations', views.OrganizationViewSet)
router.register('isd-ases', views.ISDAViewSet)
router.register('link-assignments', views.SCIONLinkAssignmentViewSet)
urlpatterns = router.urls
