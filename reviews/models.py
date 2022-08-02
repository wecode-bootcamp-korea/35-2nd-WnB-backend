from django.db      import models

from core.models    import TimeStampModel

class HostReview(TimeStampModel):
    comment  = models.TextField()
    img_url  = models.CharField(max_length = 500)
    host     = models.ForeignKey('hosts.Host', on_delete = models.CASCADE)
    user     = models.ForeignKey('users.User', on_delete = models.CASCADE)
    
    class Meta:
        db_table = 'host_reviews'

class RoomReview(TimeStampModel):
    comment  = models.TextField()
    img_url  = models.CharField(max_length = 500)
    host     = models.ForeignKey('hosts.Host', on_delete = models.CASCADE)
    user     = models.ForeignKey('users.User', on_delete = models.CASCADE)
    
    class Meta:
        db_table = 'room_reviews'