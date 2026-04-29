from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


CATEGORY_CHOICES = [
    ('goods', 'Goods'),
    ('food', 'Food'),
    ('childcare', 'Childcare'),
    ('eldercare', 'Eldercare'),
    ('transportation', 'Transportation'),
    ('housing', 'Housing'),
    ('legal', 'Legal'),
    ('medical', 'Medical'),
    ('mental_health', 'Mental Health'),
    ('education', 'Education'),
    ('labor', 'Labor'),
    ('technology', 'Technology'),
    ('financial', 'Financial'),
    ('clothing', 'Clothing'),
    ('other', 'Other'),
]

LISTING_TYPE_CHOICES = [
    ('need', 'Need'),
    ('offer', 'Offer'),
]

LISTING_KIND_CHOICES = [
    ('good', 'Good'),
    ('service', 'Service'),
]

LISTING_STATUS_CHOICES = [
    ('open', 'Open'),
    ('fulfilled', 'Fulfilled'),
    ('closed', 'Closed'),
]

CONNECTION_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('completed', 'Completed'),
]


class Profile(models.Model):
    """
    Shared participant identity — owned by either a UserProfile or an Organization.
    Listings and Connections point here, so the rest of the app doesn't care which.
    """
    location = models.CharField(max_length=10)  # zip code
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if hasattr(self, 'userprofile'):
            return str(self.userprofile)
        if hasattr(self, 'organization'):
            return str(self.organization)
        return f'Profile {self.id}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='userprofile')
    display_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.display_name or self.user.username


class Organization(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='organization')
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, blank=True, related_name='organizations')
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class VolunteerInterest(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='volunteer_interests')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    class Meta:
        unique_together = ('profile', 'category')

    def __str__(self):
        return f'{self.profile} → {self.get_category_display()}'


class Listing(models.Model):
    posted_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='listings')
    listing_type = models.CharField(max_length=5, choices=LISTING_TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    kind = models.CharField(max_length=10, choices=LISTING_KIND_CHOICES)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_volunteer = models.BooleanField(default=False)
    location = models.CharField(max_length=10)  # zip code
    status = models.CharField(max_length=10, choices=LISTING_STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_listing_type_display()} — {self.title}'


class Connection(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='connections')
    responder = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='connections')
    status = models.CharField(max_length=10, choices=CONNECTION_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.responder} → {self.listing}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(location='', bio='')
        UserProfile.objects.create(user=instance, profile=profile)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
