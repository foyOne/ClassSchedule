import rest_framework_simplejwt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission, SAFE_METHODS
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from datetime import timedelta
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Lesson, Group, Subject
from datetime import date
from .utils import string2date
from django.views.decorators.cache import cache_page, cache_control, never_cache
from django.utils.decorators import method_decorator
from rest_framework.renderers import JSONRenderer


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class LessonYMDView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [rest_framework_simplejwt.authentication.JWTAuthentication]
    renderer_classes = [JSONRenderer]
    http_method_names = ['get', 'post', 'delete']

    def getGroupTime(self, params):
        group = params.get('group')
        time = params.get('time')
        return group, time

    @method_decorator(cache_control(public=True, must_revalidate=True))
    @method_decorator(cache_page(timedelta(hours=1).seconds))
    def get(self, request, year, month, day, format=None, **kwargs):
        params = request.GET
        groupName, _ = self.getGroupTime(params)
        collection = []
        try:
            lessonDate = date(year, month, day)
            group = Group.objects.get(Name=groupName)
            lessons = Lesson.objects.filter(Group=group, Date=lessonDate)
            for l in lessons:
                record = {
                    'id': l.id,
                    'subject': l.Subject.TableName,
                    'classroom': l.Classroom,
                    'time': l.Time,
                    'professor': l.Professor.professor.TableName if l.Professor else 'Unknown'
                }
                collection.append(record)
            
            response = {
                'date': lessonDate.strftime('%Y-%m-%d'),
                'lessons': collection
                }
            return Response(response, status=200)
        
        except ObjectDoesNotExist:
            return Response(status=404)
        
        except:
            Response(status=400)
    
    @never_cache
    def post(self, request, year, month, day, format=None, **kwargs):
        params = request.GET
        groupName, _ = self.getGroupTime(params)
        timeList = ['{}-{}'.format(i, i + 1) for i in range(1, 13, 2)]
        try:
            data = json.loads(request.body)
            time = data.get('time')
            lessonDate = date(year, month, day)
            group = Group.objects.get(Name=groupName)
            lesson = Lesson.objects.filter(Group=group, Date=lessonDate, Time=time)
            if lesson.count() > 0 and time in timeList:
                return Response(status=403)
            
            classroom = data.get('classroom')
            subject = Subject.objects.get(TableName=data.get('subject'))

            lesson = Lesson.objects.create(
                Classroom=classroom,
                Date=lessonDate,
                Time=time,
                Group=group,
                Subject=subject,
                Professor=request.user)
            
            lesson.save()
            return Response(status=200)

        except:
            return Response(status=400)
    
    @never_cache
    def delete(self, request, year, month, day, format=None, **kwargs):
        try:
            d = date(year, month, day)
            lessons = Lesson.objects.filter(Date__lte=d)
            lessons.delete()
            return Response(status=204)
        
        except:
            return Response(status=400)
        

class LessonIdView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [rest_framework_simplejwt.authentication.JWTAuthentication]
    renderer_classes = [JSONRenderer]
    http_method_names = ['get', 'put', 'delete']

    @method_decorator(cache_control(public=True, must_revalidate=True))
    @method_decorator(cache_page(timedelta(hours=1).seconds))
    def get(self, request, id, format=None):
        try:
            lesson = Lesson.objects.get(pk=id)
            content = {
                'id': lesson.id,
                'group': lesson.Group.Name,
                'subject': lesson.Subject.TableName,
                'classroom': lesson.Classroom,
                'date': lesson.Date.strftime('%Y-%m-%d'),
                'time': lesson.Time,
                'professor': lesson.Professor.professor.TableName if lesson.Professor else 'Неизвестно'
            }
            return Response(data=content, status=200)
        
        except ObjectDoesNotExist:
            return Response(status=404)
        
        except:
            return Response(status=400)
    
    @never_cache
    def put(self, request, id, format=None):
        data = json.loads(request.body)
        try:
            group = data.get('group')
            subject = data.get('subject')
            professor = data.get('professor')
            lessonDate = data.get('date')

            lesson = Lesson.objects.get(pk=id)

            if lesson.Professor is None or lesson.Professor.professor.TableName != request.user.professor.TableName:
                return Response(status=403)

            lesson.Classroom = data.get('classroom', lesson.Classroom)
            lesson.Time =data.get('time', lesson.Time)
            lesson.Date = string2date(lessonDate) if lessonDate else lesson.Date
            lesson.Group = Group.objects.get(Name=group) if group else lesson.Group
            lesson.Subject = Subject.objects.get(TableName=subject) if subject else lesson.Subject
            lesson.Professor = User.objects.get(TableName=professor) if professor else lesson.Professor
            lesson.save()
            
            return Response(status=200)

        except ObjectDoesNotExist:
            return Response(status=404)
        
        except:
            return Response(status=400)
    
    @never_cache
    def delete(self, request, id, format=None):
        try:
            lesson = Lesson.objects.get(pk=id)

            if lesson.Professor is None or lesson.Professor.professor.TableName != request.user.professor.TableName:
                return Response(status=403)
            
            lesson.delete()
            return Response(ststus=204)
        
        except ObjectDoesNotExist:
            return Response(status=404)
        
        except:
            return Response(status=400)


class GroupView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [rest_framework_simplejwt.authentication.JWTAuthentication]
    renderer_classes = [JSONRenderer]
    http_method_names = ['get', 'post']

    @method_decorator(cache_control(public=True, must_revalidate=True))
    @method_decorator(cache_page(timedelta(hours=1).seconds))
    def get(self, request, format=None):
        try:
            groups = Group.objects.all()
            collection = []
            for g in groups:
                record = {
                    'id': g.id,
                    'name': g.Name
                }
                collection.append(record)
            response = { 'gropus': collection }
            return Response(data=response, status=200)
        except:
            return Response(status=400)
    
    @never_cache
    def post(self, request, format=None):
        data = json.loads(request.body)
        try:
            # uri = request.build_absolute_uri()
            group = Group.objects.create(Name=data.get('name'))
            group.save()
            return Response(status=201)
        except:
            return Response(status=400)


class GroupIdView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [rest_framework_simplejwt.authentication.JWTAuthentication]
    renderer_classes = [JSONRenderer]
    http_method_names = ['get', 'put', 'delete']

    @method_decorator(cache_control(public=True, must_revalidate=True))
    @method_decorator(cache_page(timedelta(hours=1).seconds))
    def get(self, request, id, format=None):
        try:
            group = Group.objects.get(pk=id)
            response = {
                'name': group.Name
            }
            return Response(data=response, status=200)
        except ObjectDoesNotExist:
            return Response(status=404)
        except:
            return Response(status=400)
    
    @never_cache
    def put(self, request, id, format=None):
        data = json.loads(request.body)
        try:
            group = Group.objects.get(pk=id)
            group.Name = data.get('name') if data.get('name') else group.Name
            group.save()
            return Response(status=200)
        except ObjectDoesNotExist:
            return Response(status=404)
        except:
            return Response(status=400)
    
    @never_cache
    def delete(self, request, id, format=None):
        try:
            group = Group.objects.get(pk=id)
            group.delete()
            return Response(status=204)
        except ObjectDoesNotExist:
            return Response(status=404)
        except:
            return Response(status=400)


class SubjectView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [rest_framework_simplejwt.authentication.JWTAuthentication]
    renderer_classes = [JSONRenderer]
    http_method_names = ['get', 'post']

    @method_decorator(cache_control(must_revalidate=True))
    @method_decorator(cache_page(timedelta(hours=1).seconds))
    def get(self, request, format=None):
        try:
            subjects = Subject.objects.all()
            collection = []
            for s in subjects:
                record = {
                    'id': s.id,
                    'name': s.TableName
                }
                collection.append(record)
            response = { 'subjects': collection }
            return Response(data=response, status=200)
        except:
            return Response(status=400)
    
    @never_cache
    def post(self, request, format=None):
        data = json.loads(request.body)
        if data.get('table name'):
            try:
                subject = Subject.objects.create(TableName=data.get('table name'), FullName=data.get('full name', 'Отсутствует'))
                subject.save()
                return Response(status=201)
            except:
                return Response(status=400)
        return Response(status=400)


class SubjectIdView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [rest_framework_simplejwt.authentication.JWTAuthentication]
    http_method_names = ['get', 'put', 'delete']

    @method_decorator(cache_control(public=True, must_revalidate=True))
    @method_decorator(cache_page(timedelta(hours=1).seconds))
    def get(self, request, id, format=None):
        try:
            subject = Subject.objects.get(pk=id)
            response = {
                'subject': subject.TableName
            }
            return Response(data=response, status=200)
        except ObjectDoesNotExist:
            return Response(status=404)
        except:
            return Response(status=400)
    
    @never_cache
    def put(self, request, id, format=None):
        data = json.loads(request.body)
        try:
            subject = Subject.objects.get(pk=id)
            subject.TableName = data.get('table name', subject.TableName)
            subject.FullName = data.get('full name', subject.FullName)
            subject.save()
            return Response(status=200)
        except ObjectDoesNotExist:
            return Response(status=404)
        except:
            return Response(status=400)
    
    @never_cache
    def delete(self, request, id, format=None):
        try:
            subject = Subject.objects.get(pk=id)
            subject.delete()
            return Response(status=204)
        except ObjectDoesNotExist:
            return Response(status=404)
        except:
            return Response(status=400)