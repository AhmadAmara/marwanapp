from django.db import models

# Create your models here.

class User(models.Model):
    phone_number = models.CharField(primary_key=True, max_length = 10, unique=True)
    first_name = models.CharField(max_length = 24)
    last_name = models.CharField(max_length = 24)
    password = models.CharField(max_length = 24)
    user_type = models.CharField(max_length = 24, default='customer')
    have_booked = models.BooleanField(default=False)

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return  self.last_name + '|' + self.first_name + '|' + self.phone_number + '|' +self.password+ '|' + str(self.have_booked)


class Order(models.Model):
    dt = models.DateField(auto_now_add=False)
    time = models.CharField(max_length = 5, default="00:00")
    booked = models.BooleanField(default=False)
    day_index = models.IntegerField(default=1)

    class Meta:
        ordering = ['day_index']

    def __str__(self):
        return self.time + '|'+ str(self.dt) + '|' + str(self.day_index) + '|' + str(self.booked)


class ActiveOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    class Meta:
        ordering = ['order']

    def __str__(self):
        return str(self.user) + '|' + str(self.order)