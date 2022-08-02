from django.db      import models

from core.models    import TimeStampModel

class Reservation(TimeStampModel):
    number          = models.CharField(max_length = 50)
    check_in        = models.DateField()
    check_out       = models.DateField()
    people          = models.IntegerField()
    price           = models.DecimalField(max_digits = 10, decimal_places = 2)
    room            = models.ForeignKey('rooms.Room', on_delete = models.CASCADE)
    user            = models.ForeignKey('users.User', on_delete = models.CASCADE)

    class Meta:
        db_table    = 'reservations'
