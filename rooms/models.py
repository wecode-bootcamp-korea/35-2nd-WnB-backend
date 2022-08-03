from django.db      import models
from core.models    import TimeStampModel

class Category(models.Model): 
    name    = models.CharField(max_length = 50)
    img_url = models.CharField(max_length = 200)
    
    class Meta: 
        db_table = 'categories'
        
class RoomType(models.Model): 
    name = models.CharField(max_length = 50)
    
    class Meta: 
        db_table = 'room_types'
        
class Room(TimeStampModel): 
    name              = models.CharField(max_length = 50)
    address           = models.CharField(max_length = 50)
    detail_address    = models.CharField(max_length = 50)
    price             = models.DecimalField(max_digits = 10, decimal_places = 2)
    description       = models.TextField()
    latitude          = models.DecimalField(max_digits=18, decimal_places=10)
    longitude         = models.DecimalField(max_digits=18, decimal_places=10)
    maximum_occupancy = models.IntegerField()
    bedroom           = models.IntegerField()
    bathroom          = models.IntegerField()
    bed               = models.IntegerField()
    host              = models.ForeignKey('hosts.Host', on_delete = models.CASCADE, null = True)
    category          = models.ForeignKey('Category', on_delete = models.CASCADE)
    room_type         = models.ForeignKey('RoomType', on_delete = models.CASCADE)
    facilities        = models.ManyToManyField('Facility', through = 'RoomFacility')
    
    class Meta: 
        db_table = 'rooms'
        
class Facility(models.Model): 
    name = models.CharField(max_length = 50)
    
    class Meta: 
        db_table = 'facilities'
        
class RoomFacility(models.Model): 
    room          = models.ForeignKey('Room', on_delete = models.CASCADE)
    room_facility = models.ForeignKey('Facility', on_delete = models.CASCADE)
    
    class Meta: 
        db_table = 'rooms_facilities'
        
class Image(models.Model): 
    url  = models.CharField(max_length = 200)
    room = models.ForeignKey('Room', on_delete = models.CASCADE)
    
    class Meta: 
        db_table = 'images'
        
class DetailImage(models.Model): 
    url  = models.CharField(max_length = 200)
    room = models.ForeignKey('Room', on_delete = models.CASCADE)
    
    class Meta: 
        db_table = 'detail_images'