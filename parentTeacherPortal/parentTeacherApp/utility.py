from .models import *


def notifications(**kwargs):
    template = ["AYR", "ANWATY", "FCSAC", "ANAATY", "YHBA"]
    # user is on whom notification will be reiceive
    # user2 is one to whom notification is associated
    if kwargs['Type'] == "AYR":
        notification = Notification.objects.create(user=kwargs["user"], template=template[0])
        notification.belongs_to.add(kwargs["user2"])
    elif kwargs['Type'] == "ANWATY":
        # user=Teacher
        # user2=School
        notification = Notification.objects.create(user=kwargs["user"], template=template[1],
                                                   worksheet=kwargs["worksheet"])
        notification.belongs_to.add(kwargs["user2"])
    elif kwargs['Type'] == "FCSAC":
        # user1=Teacher
        # user2=Student
        notification = Notification.objects.create(user=kwargs["user"], template=template[2],
                                                   assignment=kwargs["assignment"], )
        notification.belongs_to.add(kwargs['user2'])
    elif kwargs['Type'] == "ANAATY":
        # user1=Student
        # user2=Teacher
        notification = Notification.objects.create(user=kwargs["user"], template=template[3],
                                                   assignment=kwargs["assignment"])
        notification.belongs_to.add(kwargs["user2"])
    elif kwargs['Type'] == "YHBA":
        # user1=Teacher
        # user2=School
        notification = Notification.objects.create(user=kwargs["user"], template=template[4],
                                                   standard=kwargs["standard"], subject=kwargs["subject"])
        notification.belongs_to.add(kwargs["user2"])
