from django.urls import path
from django.conf.urls import url

from lpr.views import (
   save_url, edit_roi, LPR_View, fecthLPR, dashboard, add_new_allowed_plate, remove_allowed_plate
)

app_name = 'lpr'
urlpatterns = [
    path('', LPR_View.as_view(), name='lpr'),
    
    path('edit_roi', edit_roi, {}, name='edit_roi'),
    
    path('save_url', save_url, {}, name='save_url'),
    
    path('fecthLPR', fecthLPR, {}, name='fecthLPR'),
    
    path('dashboard', dashboard, name='dashboard'),


    path('add_new_allowed_plate', add_new_allowed_plate, {}, name='add_new_allowed_plate'),
    path('remove_allowed_plate', remove_allowed_plate, {}, name='remove_allowed_plate'),
  #  url(r'^manage_cameras/manage_spots/$', manage_spots, name='manage_spots'),    
]