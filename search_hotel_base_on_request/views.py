from django.http import HttpResponse, HttpResponseRedirect
#from polls.models import Poll, Choice
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone


