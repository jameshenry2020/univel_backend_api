from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAdminUser
from django.http import Http404
from django.contrib.auth.models import User
from .serializers import CourseSerializer, StudentSerializer, InstructorSerializer, UserSerializer
from .models import Course, Student, Instructor

# Create your views here.



class CourseListView(APIView):
    def get(self, request):
        course=Course.objects.all()
        serializer=CourseSerializer(course, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer=CourseSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CourseDetail(APIView):
    def get_object(self, pk):
        try:
            course = Course.objects.get(id=pk)
            return course
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, pk):	
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        course = self.get_object(pk)
        course.delete()
        return Response({"message":"delete was successfull"}, status=status.HTTP_204_NO_CONTENT)


class StudentApiView(generics.ListCreateAPIView):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer
    lookup_field="pk"


class InstructorListView(generics.GenericAPIView):
    serializer_class=InstructorSerializer
    queryset=Instructor.objects.all()
    permission_classes=[AllowAny]

    def get(self, request, *args, **kwargs):
        obj=self.get_queryset()
        serializer=self.serializer_class(obj, many=True)
        return Response(
            {"data":serializer.data,
             "message":"extra response message"
                         }, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                "data":serializer.data,
                "extra_message":"some extra message"
            }, status=status.HTTP_200_OK)
        
    def get_queryset(self):
        queryset=super().get_queryset()
        query_p=self.request.query_params.get('course')
        if query_p is not None:
            queryset=queryset.filter(course__title__icontains=query_p)
        return queryset


# class CreateNewUser(generics.CreateAPIView):
#     serializer_class=UserSerializer
#     queryset=User.objects.all()
#     permission_classes=[AllowAny]

