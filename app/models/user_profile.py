from django.db import models
from django.contrib.auth.models import User

OTP_CHOICES = (
	('NEW', 'New'),
    ('FORGOT', 'Forgot'),
    ('CARD', 'Card'),
    ('OTHER', 'Other'),
)

class UserProfile(User):
    google_id = models.CharField('google_id', max_length=200, null=True)
    google_image = models.CharField('google_image', max_length=500, null=True)
    facebook_id = models.CharField('facebook_id', max_length=200, null=True)
    dob = models.DateField(null=True)

    def __unicode__(self):
         return self.last_name + self.first_name

    def calculate_age(self):
        today = date.today()

        try: 
            birthday = self.dob.replace(year=today.year)
        # raised when birth date is February 29 and the current year is not a leap year
        except ValueError:
            birthday = self.dob.replace(year=today.year, day=born.day-1)

        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year


class OneTimePassword(models.Model):
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User)
    otp = models.CharField(max_length=50)
    otp_types = models.CharField(max_length=10, choices=OTP_CHOICES,
                                      default='NEW')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return str(self.user.first_name)

    class Meta:
        db_table = 'one_time_password'