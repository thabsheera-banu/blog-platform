from django.shortcuts import render
from rest_framework import generics
from .serializers import BlogSerializers , ProfileSerializers
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from . models import BlogPost,UserProfile
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination



# Create your views here.

#pagination view
class Pagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100

# to show the all blogs
class PublicView(generics.ListAPIView):
    serializer_class = BlogSerializers
    pagination_class = Pagination

    def get_queryset(self):
        queryset = BlogPost.objects.all()
        search_query = self.request.query_params.get('search', None)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query)
            )

        return queryset
    

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self , request):
        try:
            blogs = BlogPost.objects.filter(user = request.user)

            # search functionality
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains =search) | Q(content__icontains = search))

        
            serializer = BlogSerializers(blogs,many = True)
            return Response({
                'data' : serializer.data,
                'message' : 'blog fetched successfully '

            },status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({
                'data' : {},
                'message' : 'somthing wrong in data'
            },status=status.HTTP_400_BAD_REQUEST)

    def post(self , request):
        try:
            data = request.data
            print(request.user)
            data['user']  = request.user.id
            serializer = BlogSerializers(data=data)
            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message' : 'somthing wrong data'
                },status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data' : serializer.data,
                'message' : 'blog successfully created'

            },status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({
                'data' : {},
                'message' : 'somthing wrong'
            },status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self , request):
        try:
            data = request.data
            blog = BlogPost.objects.filter(uid = data.get('uid'))

            if not blog.exists():
                return Response({
                        'data':{},
                        'message' : 'invalid user'
                    },status=status.HTTP_400_BAD_REQUEST)


            if request.user != blog[0].user:
                return Response({
                        'data':{},
                        'message' : 'You are not autherized user'
                    },status=status.HTTP_400_BAD_REQUEST)
            serializer = BlogSerializers( blog[0] ,data=data ,partial = True)

            if not serializer.is_valid():
                    return Response({
                        'data':serializer.errors,
                        'message' : 'somthing wrong data'
                    },status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                    'data' : serializer.data,
                    'message' : 'blog successfully updated'

                },status=status.HTTP_201_CREATED)


        except Exception as e:
            print(e)
            return Response({
                'data' : {},
                'message' : 'somthing wrong'
            },status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        try:
            data = request.data
            blog = BlogPost.objects.filter(uid = data.get('uid'))

            if not blog.exists():
                return Response({
                        'data':{},
                        'message' : 'invalid user'
                    },status=status.HTTP_400_BAD_REQUEST)


            if request.user != blog[0].user:
                return Response({
                        'data':{},
                        'message' : 'You are not autherized user'
                    },status=status.HTTP_400_BAD_REQUEST)
            blog[0].delete()

            
            return Response({
                    'data' : {},
                    'message' : 'blog successfully deleted'

                },status=status.HTTP_201_CREATED)


        except Exception as e:
            print(e)
            return Response({
                'data' : {},
                'message' : 'somthing wrong'
            },status=status.HTTP_400_BAD_REQUEST)
        

# update User profile

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        return self.request.user.userprofile



