

from .serializers import LoginSerializer
from .serializers import UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


# Register
class RegisterView(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = UserRegistrationSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message' : 'somthing wrong data'
                },status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data' : {},
                'message' : 'Account successfully created'

            },status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({
                'data' : {},
                'message' : 'somthing wrong'
            },status=status.HTTP_400_BAD_REQUEST)
        
# Login

class LoginView(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message' : 'somthing wrong data'
                },status=status.HTTP_400_BAD_REQUEST)
            res = serializer.get_jwt_token(serializer.data)
            return Response(res,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            print(e)
            return Response({
                'data' : {},
                'message' : 'somthing wrong'
            },status=status.HTTP_400_BAD_REQUEST)


            

        


