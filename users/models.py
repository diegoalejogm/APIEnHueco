from django.db import models
from django.utils import timezone
from django.conf import settings

#---------

def generate_filename(self, filename):
    url = "img/profile/%s.%s" % (self.login, filename.split(".")[-1].lower())

    return url

class User(models.Model):

    ### User Data
    login = models.CharField(max_length=30, primary_key=True, default=None)
    firstNames = models.CharField(max_length=50, null=False, blank=False, default=None)
    lastNames = models.CharField(max_length=50, null=False, default=None)
    phoneNumber = models.CharField(max_length=30, default="")
    imageURL = models.ImageField(upload_to= generate_filename)
    # imageURL = models.CharField(max_length=200)

    ### Privacy Handling
    shares_user_nearby = models.BooleanField(default=True)
    shares_event_names = models.BooleanField(default=True)
    shares_event_locations = models.BooleanField(default=True)

    ### Relationship handlers
    schedule_updated_on = models.DateTimeField(default=timezone.now)

    ### Control Attributes
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    ### Relationship
    friends = models.ManyToManyField('self', symmetrical=False, related_name='friends+', through='Friendship')
    requests_sent= models.ManyToManyField('self', through='FriendRequest',symmetrical=False, related_name='requests_received')

    def isFriendsWith(self, otherUser):
        return otherUser in self.friends.all()

    @classmethod
    def create(cls, login, firstNames, lastNames):
        me = cls(login=login, firstNames=firstNames, lastNames=lastNames)
        return me

    def __str__(self):
        return '{} : {} {}'.format(self.login, self.firstNames, self.lastNames)

    @classmethod
    def apply_privacy_settings_to_queryset(cls, friends):
        for friend in friends:
            ## Check event locations
            if not friend.shares_event_locations:
                for event in friend.gap_set.all():
                    event.location = ""

            ## Check event names
            if not friend.shares_event_names:
                schedule = friend.gap_set.all()
                for event in schedule:
                    event.name = ""

        return friends

class FriendRequest(models.Model):

    fromUser = models.ForeignKey(settings.USER_MODEL, related_name='+')
    toUser = models.ForeignKey(settings.USER_MODEL, related_name='+')

    # Control Attributes
    created_on = models.DateTimeField(default=timezone.now)
    # lastUpdated_on = models.DateTimeField(auto_now=True)

class Friendship(models.Model):

    firstUser = models.ForeignKey(settings.USER_MODEL, related_name='+')
    secondUser = models.ForeignKey(settings.USER_MODEL, related_name='+')

    # Control Attributes
    created_on = models.DateTimeField(default=timezone.now)
    lastUpdated_on = models.DateTimeField(auto_now=True)


    @classmethod
    def areFriends(cls, user1, user2):
        """
        :param user1: User
        :param user2: User
        :return:
        """
        return user2 in user1.friends.all()

    @classmethod
    def areFriendsPK(cls, user1, user2):
        """
        :param user1: String
        :param user2: String
        :return:
        """
        usr1 = User.objects.filter(login=user1).first()
        usr2 = User.objects.filter(login=user2).first()

        if(usr1 is not None and usr2 is not None):

            return cls.areFriends(usr1,usr2)

        else:
            return False