import random
import string
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from .models import WorkerProfile


def getminworker():
    min = WorkerProfile.objects.all()[0].task_count
    for worker in WorkerProfile.objects.all():
        no = worker.task_count
        if min > no:
            min = no
    workerlist = []
    for worker in WorkerProfile.objects.all():
        if min == worker.task_count:
            workerlist.append(worker)
    minworker = random.choice(workerlist)
    return minworker


def addressparser(address):
    if address[-1] == ',':
        address = address[:-1]
    addlist = address.split(',')
    for i in range(len(addlist)):
        element = addlist[i].strip()
        addlist[i] = " ".join(element.split())
    address = ','.join(addlist)
    return address


def genrandomstring(length):
    letters = string.ascii_letters
    connectionHash = ''.join(random.choice(letters)
                             for i in range(length))
    return connectionHash


def genrandomint(length):
    connectionHash = int(''.join(str(random.randint(0, 9))
                                 for i in range(length)))
    return connectionHash


def taskmailbody(connectionHash, receiever):
    SubjectBody = "A task has been Alloted."
    sender = "admin@evoter.com"
    tasklink = settings.SITE_URL+reverse('verify-view', args=(connectionHash,))
    mailbody = f"""
        Dear Admin,
        You have been alloted a task to verify the credentials.
        Click on the link below-
        {tasklink}
        Regards,
        MainAdmin
        (EVoterAuth)
    """
    send_mail(SubjectBody, mailbody, sender, [receiever], fail_silently=False)
    return tasklink
