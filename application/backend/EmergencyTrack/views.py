import jwt
from django.contrib.auth import get_user_model, login, logout
from django.db import IntegrityError
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from .validations import custom_validation, validate_email, validate_password
from .permissions import Authenticated, AdminPermission, OfficerPermission, DepartmentAccessPermission
from .models import *
from .serializer import *
from .utils import generate_access_token
from .settings import SECRET_KEY


class UserRegister(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        clean_data = custom_validation(request.data)

        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                access_token = generate_access_token(user)
                response_data = {
                    'access_token': access_token,
                    'user': {
                        'user_id': user.user_id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'account_type': user.account_type.account_type if user.account_type else None,
                        'account_type_name': user.account_type.account_type_name if user.account_type else None,
                        'user_icon': user.user_icon
                    }
                }
                response = Response(response_data, status=status.HTTP_201_CREATED)
                response.set_cookie(key='access_token', value=access_token, httponly=True)
                return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)

            if not user:
                raise AuthenticationFailed("User not found.")

            if user.is_active:
                access_token = generate_access_token(user)

                # include token in response
                response_data = {
                    'access_token': access_token,
                    'user': {
                        'user_id': user.user_id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'account_type': user.account_type.account_type if user.account_type else None,
                        'account_type_name': user.account_type.account_type_name if user.account_type else None,
                        'user_icon': user.user_icon
                    }
                }

                response = Response(response_data, status=status.HTTP_200_OK)
                response.set_cookie(key='access_token', value=access_token, httponly=True)

                return response

            return Response({
                'message': 'Something went wrong.'
            })


class UserLogout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        user_token = request.COOKIES.get('access_token', None)
        if user_token:
            response = Response(data={'message': 'Logged out successfully'},
                                status=status.HTTP_200_OK)
            response.delete_cookie('access_token')
            return response
        return Response(data={'message': 'User is already logged out.'})


class UserApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        serializer = UsersSerializer(request.user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)


class UsersAdminApiView(APIView):
    # Default permission class for all methods
    permission_classes = [AdminPermission]
    authentication_classes = [TokenAuthentication, ]

    # List all users
    def get(self, request, *args, **kwargs):
        # get all users in the db
        users = Users.objects
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersAdminDetailApiView(APIView):
    # Default permission class for all methods
    permission_classes = [AdminPermission]
    authentication_classes = [TokenAuthentication, ]

    def get_object(self, user_id):
        try:
            return Users.objects.get(user_id=user_id)
        except Users.DoesNotExist:
            return None

    def get(self, request, id, *args, **kwargs):
        # get the users that match the given email
        user = Users.objects.filter(email__icontains=id)
        if not user:
            return Response(
                {"res": "There is no user with the given email"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UsersSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        # update a specific user
        user = self.get_object(user_id=id)
        if not user:
            Response(
                {"res": "User with given user id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "email": request.data.get("email"),
            "email_status": request.data.get("email_status"),
            "account_type": request.data.get("account_type"),
            "user_icon": request.data.get("user_icon"),
        }
        serializer = UsersSerializer(instance=user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        # delete the user with a specific dataset id
        user = self.get_object(dataset_id=id)
        if not user:
            Response(
                {"res": "User with given user id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.delete()
        return Response(
            {"res": "User deleted!"},
            status=status.HTTP_200_OK
        )


class PendingOfficersApiView(APIView):
    # Default permission class for all methods
    permission_classes = [AdminPermission]
    authentication_classes = [TokenAuthentication, ]

    # List all users
    def get(self, request, *args, **kwargs):
        # get all users in the db
        users = Users.objects.filter(account_type__account_type=1)
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionApiView(APIView):
    # Default permission class for all methods
    permission_classes = [Authenticated]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, *args, **kwargs):
        # get the users subscriptions
        county = request.data.get("county")

        # get the user
        user_token = request.COOKIES.get('access_token')
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        subscribed_departments = Subscriptions.objects.filter(user__user_id=user.user_id,
                                                              department__county__county_id=county)
        serializer = DepartmentSerializer(subscribed_departments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # subscribe to a department
        county = request.data.get("county")
        department_type = request.data.get("department")

        department = Departments.objects.get(county__county_id=county, department_type__department_name=department_type)

        # get the user
        user_token = request.COOKIES.get('access_token')
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        data = {
            "user": user.user_id,
            "department": department.department_id,
        }
        try:
            serializer = SubscriptionsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({"error": "Subscription already exists for this user and department."},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # unsubscribe from a department
        county = request.data.get("county")
        department_type = request.data.get("department")

        department = Departments.objects.get(county__county_id=county, department_type__department_name=department_type)

        # get the user
        user_token = request.COOKIES.get('access_token')
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        print(user.user_id, department.department_id)

        try:
            subscription = Subscriptions.objects.get(user=user.user_id, department=department.department_id)
            subscription.delete()
            return Response(
                {"res": "Subscription deleted!"},
                status=status.HTTP_200_OK
            )
        except Subscriptions.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CountysApiView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        output = [
            {
                "county_id": output.county_id,
                "county_name": output.county_name,
                "county_population": output.county_population,
            }
            for output in Countys.objects.all()
        ]
        return Response(output)


class CovidApiView(APIView):
    # Default permission class for all methods
    permission_classes = [OfficerPermission, DepartmentAccessPermission]
    authentication_classes = [TokenAuthentication,]

    def get_permissions(self):
        # Modify permissions for POST method
        if self.request.method == "GET":
            return [permissions.AllowAny()]  # Allow any user GET data
        return super().get_permissions()

    # List all covid cases
    def get(self, request, *args, **kwargs):
        # get all covid cases in the db
        covid_cases = CovidCases.objects
        serializer = CovidSerializer(covid_cases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Create a covid case
    def post(self, request, *args, **kwargs):
        # get the user
        user_token = request.COOKIES.get('access_token')
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        # add a covid case to the db
        data = {
            "number_of_cases": request.data.get("number_of_cases"),
            "report_date": request.data.get("report_date"),
            "county": request.data.get("county"),
            "officer": user.user_id,
        }
        serializer = CovidSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CovidDetailApiView(APIView):
    # Default permission class for all methods
    permission_classes = [OfficerPermission, DepartmentAccessPermission]
    authentication_classes = [TokenAuthentication,]

    def get_permissions(self):
        # Modify permissions for POST method
        if self.request.method == "GET":
            return [permissions.AllowAny()]  # Allow any user GET data
        return super().get_permissions()

    def get_object(self, dataset_id):
        try:
            return CovidCases.objects.get(dataset_id=dataset_id)
        except CovidCases.DoesNotExist:
            return None

    def get(self, request, id,  *args, **kwargs):
        # get the covid cased of a county
        covid_cases = CovidCases.objects.filter(county=id)
        if not covid_cases:
            return Response(
                {"res": "No covid case in given county"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CovidSerializer(covid_cases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        # update a specific covid case
        covid_case = self.get_object(dataset_id=id)
        if not covid_case:
            Response(
                {"res": "Covid Case with given dataset id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # get the user
        user_token = request.COOKIES.get('access_token')
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        data = {
            "number_of_cases": request.data.get("number_of_cases"),
            "report_date": request.data.get("report_date"),
            "county": request.data.get("county"),
            "officer": user.user_id,
        }
        serializer = CovidSerializer(instance=covid_case, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        # delete the covid case with a specific dataset id
        covid_case = self.get_object(dataset_id=id)
        if not covid_case:
            Response(
                {"res": "Covid Case with given dataset id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        covid_case.delete()
        return Response(
            {"res": "Covid case deleted!"},
            status=status.HTTP_200_OK
        )


class DeathApiView(APIView):
    # Default permission class for all methods
    permission_classes = [OfficerPermission, DepartmentAccessPermission]
    authentication_classes = [TokenAuthentication,]

    def get_permissions(self):
        # Modify permissions for POST method
        if self.request.method == "GET":
            return [permissions.AllowAny()]  # Allow any user GET data
        return super().get_permissions()

    # List all deaths
    def get(self, request, *args, **kwargs):
        # get all death in the db
        deaths = Deaths.objects
        serializer = DeathSerializer(deaths, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Create a covid case
    def post(self, request, *args, **kwargs):
        # add a covid case to the db

        # get the user
        user_token = request.COOKIES.get('access_token')
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        data = {
            "number_of_deaths": request.data.get("number_of_cases"),
            "cause_of_deaths": request.data.get("cause_of_deaths"),
            "report_date": request.data.get("report_date"),
            "county": request.data.get("county"),
            "officer": user.user_id
        }
        serializer = DeathSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeathDetailApiView(APIView):
    # Default permission class for all methods
    permission_classes = [OfficerPermission, DepartmentAccessPermission]
    authentication_classes = [TokenAuthentication,]

    def get_permissions(self):
        # Modify permissions for POST method
        if self.request.method == "GET":
            return [permissions.AllowAny()]  # Allow any user GET data
        return super().get_permissions()

    def get_object(self, dataset_id):
        try:
            return Deaths.objects.get(dataset_id=dataset_id)
        except Deaths.DoesNotExist:
            return None

    def get(self, request, id, *args, **kwargs):
        # get the deaths of a county
        deaths = Deaths.objects.filter(county=id)
        if not deaths:
            return Response(
                {"res": "No deaths in given county"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = DeathSerializer(deaths, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        # update a specific covid case
        death = self.get_object(dataset_id=id)
        if not death:
            Response(
                {"res": "Death with given dataset id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # get the user
        user_token = request.COOKIES.get('access_token')
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        data = {
            "number_of_deaths": request.data.get("number_of_cases"),
            "cause_of_deaths": request.data.get("cause_of_deaths"),
            "report_date": request.data.get("report_date"),
            "county": request.data.get("county"),
            "officer": user.user_id,
        }
        serializer = DeathSerializer(instance=death, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        # delete the covid case with a specific dataset id
        death = self.get_object(dataset_id=id)
        if not death:
            Response(
                {"res": "Death with given dataset id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        death.delete()
        return Response(
            {"res": "Death deleted!"},
            status=status.HTTP_200_OK
        )


class BlockedRoadsApiView(APIView):
    # Default permission class for all methods
    permission_classes = [OfficerPermission, DepartmentAccessPermission]
    authentication_classes = [TokenAuthentication,]

    def get_permissions(self):
        # Modify permissions for POST method
        if self.request.method == "GET":
            return [permissions.AllowAny()]  # Allow any user GET data
        return super().get_permissions()

    # List every dataset in db
    def get(self, request, *args, **kwargs):
        # get all covid cases in the db
        objects = BlockedRoads.objects
        serializer = BlockedRoadsSerializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # create a dataset
    def post(self, request, *args, **kwargs):
        # get the user
        user_token = request.COOKIES.get('access_token')
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        data = {
            "road_name": request.data.get("road_name"),
            "location_x_coordinate": request.data.get("location_x_coordinate"),
            "location_y_coordinate": request.data.get("location_y_coordinate"),
            "reason": request.data.get("reason"),
            "intersection1": request.data.get("intersection1"),
            "intersection2": request.data.get("intersection2"),
            "starting_datetime": request.data.get("starting_datetime"),
            "ending_datetime": request.data.get("ending_datetime"),
            "informations_for_public": request.data.get("informations_for_public"),
            "county": request.data.get("county"),
            "officer": user.user_id,
        }
        serializer = BlockedRoadsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlockedRoadsDetailApiView(APIView):
    # Default permission class for all methods
    permission_classes = [OfficerPermission, DepartmentAccessPermission]
    authentication_classes = [TokenAuthentication,]

    def get_permissions(self):
        # Modify permissions for POST method
        if self.request.method == "GET":
            return [permissions.AllowAny()]  # Allow any user GET data
        return super().get_permissions()

    # helper function to get the dataset specified by the dataset id
    def get_object(self, dataset_id):
        try:
            return BlockedRoads.objects.get(dataset_id=dataset_id)
        except BlockedRoads.DoesNotExist:
            return None

    # get all the datasets that contain the given sting in the county name
    def get(self, request, id, *args, **kwargs):
        object = self.get_object(dataset_id=id)
        if not object:
            return Response(
                {"res": "No dataset with the given dataset id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = BlockedRoadsSerializer(object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # update a specific dataset
    def put(self, request, id, *args, **kwargs):
        object = self.get_object(dataset_id=id)
        if not object:
            Response(
                {"res": "No dataset with the given dataset id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # get the user
        user_token = request.COOKIES.get('access_token')
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        data = {
            "road_name": request.data.get("road_name"),
            "location_x_coordinate": request.data.get("location_x_coordinate"),
            "location_y_coordinate": request.data.get("location_y_coordinate"),
            "reason": request.data.get("reason"),
            "intersection1": request.data.get("intersection1"),
            "intersection2": request.data.get("intersection2"),
            "starting_datetime": request.data.get("starting_datetime"),
            "ending_datetime": request.data.get("ending_datetime"),
            "informations_for_public": request.data.get("informations_for_public"),
            "county": request.data.get("county"),
            "officer": user.user_id
        }
        serializer = BlockedRoadsSerializer(instance=object, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a specific dataset
    def delete(self, request, id, *args, **kwargs):
        object = self.get_object(dataset_id=id)
        if not object:
            Response(
                {"res": "No dataset with the given dataset id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        object.delete()
        return Response(
            {"res": "Dataset deleted!"},
            status=status.HTTP_200_OK
        )


class SecurityConcernsApiView(APIView):
    # Default permission class for all methods
    permission_classes = [OfficerPermission, DepartmentAccessPermission]
    authentication_classes = [TokenAuthentication,]

    def get_permissions(self):
        # Modify permissions for POST method
        if self.request.method == "GET":
            return [permissions.AllowAny()]  # Allow any user GET data
        return super().get_permissions()

    # List every dataset in db
    def get(self, request, *args, **kwargs):
        # get all covid cases in the db
        objects = SecurityConcerns.objects
        serializer = SecurityConcernsSerializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # create a dataset
    def post(self, request, *args, **kwargs):
        # get the user
        user_token = request.COOKIES.get('access_token')
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        data = {
            "location_name": request.data.get("location_name"),
            "location_x_coordinate": request.data.get("location_x_coordinate"),
            "location_y_coordinate": request.data.get("location_y_coordinate"),
            "cause_of_concern": request.data.get("cause_of_concern"),
            "reported_datetime": request.data.get("reported_datetime"),
            "instructions_for_public": request.data.get("instructions_for_public"),
            "concern_is_present": request.data.get("concern_is_present"),
            "county": request.data.get("county"),
            "officer": user.user_id
        }
        serializer = SecurityConcernsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SecurityConcernsDetailApiView(APIView):
    # Default permission class for all methods
    permission_classes = [OfficerPermission, DepartmentAccessPermission]
    authentication_classes = [TokenAuthentication,]

    def get_permissions(self):
        # Modify permissions for POST method
        if self.request.method == "GET":
            return [permissions.AllowAny()]  # Allow any user GET data
        return super().get_permissions()

    # helper function to get the dataset specified by the dataset id
    def get_object(self, dataset_id):
        try:
            return SecurityConcerns.objects.get(dataset_id=dataset_id)
        except SecurityConcerns.DoesNotExist:
            return None

    # get all the datasets that contain the given sting in the county name
    def get(self, request, id, *args, **kwargs):
        object = self.get_object(dataset_id=id)
        if not object:
            Response(
                {"res": "No dataset with the given dataset id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SecurityConcernsSerializer(object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # update a specific dataset
    def put(self, request, id, *args, **kwargs):
        object = self.get_object(dataset_id=id)
        if not object:
            Response(
                {"res": "No dataset with the given dataset id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # get the user
        user_token = request.COOKIES.get('access_token')
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        data = {
            "location_name": request.data.get("location_name"),
            "location_x_coordinate": request.data.get("location_x_coordinate"),
            "location_y_coordinate": request.data.get("location_y_coordinate"),
            "cause_of_concern": request.data.get("cause_of_concern"),
            "reported_datetime": request.data.get("reported_datetime"),
            "instructions_for_public": request.data.get("instructions_for_public"),
            "concern_is_present": request.data.get("concern_is_present"),
            "county": request.data.get("county"),
            "officer": user.user_id
        }
        serializer = SecurityConcernsSerializer(instance=object, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a specific dataset
    def delete(self, request, id, *args, **kwargs):
        object = self.get_object(dataset_id=id)
        if not object:
            Response(
                {"res": "No dataset with the given dataset id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        object.delete()
        return Response(
            {"res": "Dataset deleted!"},
            status=status.HTTP_200_OK
        )


class WeatherEventsApiView(APIView):
    # Default permission class for all methods
    permission_classes = [OfficerPermission, DepartmentAccessPermission]
    authentication_classes = [TokenAuthentication,]

    def get_permissions(self):
        # Modify permissions for POST method
        if self.request.method == "GET":
            return [permissions.AllowAny()]  # Allow any user GET data
        return super().get_permissions()

    # List every dataset in db
    def get(self, request, *args, **kwargs):
        # get all covid cases in the db
        objects = WeatherEvents.objects
        serializer = WeatherEventsSerializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # create a dataset
    def post(self, request, *args, **kwargs):
        # get the user
        user_token = request.COOKIES.get('access_token')
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        data = {
            "location_name": request.data.get("location_name"),
            "location_x_coordinate": request.data.get("location_x_coordinate"),
            "location_y_coordinate": request.data.get("location_y_coordinate"),
            "event_type": request.data.get("event_type"),
            "estimated_datetime": request.data.get("estimated_datetime"),
            "event_radius": request.data.get("event_radius"),
            "instructions_for_public": request.data.get("instructions_for_public"),
            "level_of_evacuation": request.data.get("level_of_evacuation"),
            "event_is_active": request.data.get("event_is_active"),
            "county": request.data.get("county"),
            "officer": user.user_id
        }
        serializer = WeatherEventsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WeatherEventsDetailApiView(APIView):
    # Default permission class for all methods
    permission_classes = [OfficerPermission, DepartmentAccessPermission]
    authentication_classes = [TokenAuthentication,]

    def get_permissions(self):
        # Modify permissions for POST method
        if self.request.method == "GET":
            return [permissions.AllowAny()]  # Allow any user GET data
        return super().get_permissions()

    # helper function to get the dataset specified by the dataset id
    def get_object(self, dataset_id):
        try:
            return WeatherEvents.objects.get(dataset_id=dataset_id)
        except WeatherEvents.DoesNotExist:
            return None

    # get all the datasets that contain the given sting in the county name
    def get(self, request, id, *args, **kwargs):
        object = self.get_object(dataset_id=id)
        if not object:
            Response(
                {"res": "No dataset with the given dataset id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = WeatherEventsSerializer(object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # update a specific dataset
    def put(self, request, id, *args, **kwargs):
        object = self.get_object(dataset_id=id)
        if not object:
            Response(
                {"res": "No dataset with the given dataset id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # get the user
        user_token = request.COOKIES.get('access_token')
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        data = {
            "location_name": request.data.get("location_name"),
            "location_x_coordinate": request.data.get("location_x_coordinate"),
            "location_y_coordinate": request.data.get("location_y_coordinate"),
            "event_type": request.data.get("event_type"),
            "estimated_datetime": request.data.get("estimated_datetime"),
            "event_radius": request.data.get("event_radius"),
            "instructions_for_public": request.data.get("instructions_for_public"),
            "level_of_evacuation": request.data.get("level_of_evacuation"),
            "event_is_active": request.data.get("event_is_active"),
            "county": request.data.get("county"),
            "officer": user.user_id
        }
        serializer = WeatherEventsSerializer(instance=object, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a specific dataset
    def delete(self, request, id, *args, **kwargs):
        object = self.get_object(dataset_id=id)
        if not object:
            Response(
                {"res": "No dataset with the given dataset id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        object.delete()
        return Response(
            {"res": "Dataset deleted!"},
            status=status.HTTP_200_OK
        )


class WildfiresApiView(APIView):
    # Default permission class for all methods
    permission_classes = [OfficerPermission, DepartmentAccessPermission]
    authentication_classes = [TokenAuthentication,]

    def get_permissions(self):
        # Modify permissions for POST method
        if self.request.method == "GET":
            return [permissions.AllowAny()]  # Allow any user GET data
        return super().get_permissions()

    # List every dataset in db
    def get(self, request, *args, **kwargs):
        # get all covid cases in the db
        objects = Wildfires.objects
        serializer = WildfiresSerializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # create a dataset
    def post(self, request, *args, **kwargs):
        # get the user
        user_token = request.COOKIES.get('access_token')
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        data = {
            "location_name": request.data.get("location_name"),
            "location_x_coordinate": request.data.get("location_x_coordinate"),
            "location_y_coordinate": request.data.get("location_y_coordinate"),
            "cause_of_fire": request.data.get("cause_of_fire"),
            "date_of_fire": request.data.get("date_of_fire"),
            "instructions_for_public": request.data.get("instructions_for_public"),
            "level_of_evacuation": request.data.get("level_of_evacuation"),
            "fire_is_active": request.data.get("fire_is_active"),
            "county": request.data.get("county"),
            "officer": user.user_id
        }
        serializer = WildfiresSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WildfiresDetailApiView(APIView):
    # Default permission class for all methods
    permission_classes = [OfficerPermission, DepartmentAccessPermission]
    authentication_classes = [TokenAuthentication,]

    def get_permissions(self):
        # Modify permissions for POST method
        if self.request.method == "GET":
            return [permissions.AllowAny()]  # Allow any user GET data
        return super().get_permissions()

    # helper function to get the dataset specified by the dataset id
    def get_object(self, dataset_id):
        try:
            return Wildfires.objects.get(dataset_id=dataset_id)
        except Wildfires.DoesNotExist:
            return None

    # get all the datasets that contain the given sting in the county name
    def get(self, request, id, *args, **kwargs):
        object = self.get_object(dataset_id=id)
        if not object:
            Response(
                {"res": "No dataset with the given dataset id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = WildfiresSerializer(object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # update a specific dataset
    def put(self, request, id, *args, **kwargs):
        object = self.get_object(dataset_id=id)
        if not object:
            Response(
                {"res": "No dataset with the given dataset id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # get the user
        user_token = request.COOKIES.get('access_token')
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        data = {
            "location_name": request.data.get("location_name"),
            "location_x_coordinate": request.data.get("location_x_coordinate"),
            "location_y_coordinate": request.data.get("location_y_coordinate"),
            "cause_of_fire": request.data.get("cause_of_fire"),
            "date_of_fire": request.data.get("date_of_fire"),
            "instructions_for_public": request.data.get("instructions_for_public"),
            "level_of_evacuation": request.data.get("level_of_evacuation"),
            "fire_is_active": request.data.get("fire_is_active"),
            "county": request.data.get("county"),
            "officer": user.user_id
        }
        serializer = WildfiresSerializer(instance=object, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a specific dataset
    def delete(self, request, id, *args, **kwargs):
        object = self.get_object(dataset_id=id)
        if not object:
            Response(
                {"res": "No dataset with the given dataset id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        object.delete()
        return Response(
            {"res": "Dataset deleted!"},
            status=status.HTTP_200_OK
        )


class CountyStatisticsApiView(APIView):
    # permission class to check if the user is authenticated
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    # List the statistics of all county's
    def get(self, request, *args, **kwargs):
        # get all county statistics in the db
        county_stats = CountyStatistics.objects
        serializer = CountyStatisticsSerializer(county_stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CountyStatisticsDetailApiView(APIView):
    # permission class to check if the user is authenticated
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, name, *args, **kwargs):
        # get the covid cased of all countys that contain the name string
        county_stats = CountyStatistics.objects.filter(county_name__icontains=name)
        if not county_stats:
            return Response(
                {"res": "There is no county with the given name"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CountyStatisticsSerializer(county_stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StateStatisticsApiView(APIView):
    # permission class to check if the user is authenticated
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    # List the statistics of all states
    def get(self, request, *args, **kwargs):
        # get all county statistics in the db
        state_stats = StateStatistics.objects
        serializer = StateStatisticsSerializer(state_stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StateStatisticsDetailApiView(APIView):
    # permission class to check if the user is authenticated
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, state_id, *args, **kwargs):
        # get the statistics of the state with the given id
        state_stats = StateStatistics.objects.filter(state_id=state_id)
        if not state_stats:
            return Response(
                {"res": "There is no state with the given id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = StateStatisticsSerializer(state_stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CovidCaseStatisticsApiView(APIView):
    # permission class to check if the user is authenticated
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    # List all the covid case statistics
    def get(self, request, *args, **kwargs):
        # get all covid case statistics in the db
        covid_stats = CovidCaseStatistics.objects
        serializer = CovidCaseStatisticsSerializer(covid_stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CovidCaseStatisticsDetailApiView(APIView):
    # permission class to check if the user is authenticated
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, name, *args, **kwargs):
        # get the covid case statistics of all countys that contain the name string
        covid_stats = CovidCaseStatistics.objects.filter(county_name__icontains=name)
        if not covid_stats:
            return Response(
                {"res": "There is no county with the given name"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CovidCaseStatisticsSerializer(covid_stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeathStatisticsApiView(APIView):
    # permission class to check if the user is authenticated
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    # List all the covid case statistics
    def get(self, request, *args, **kwargs):
        # get all covid case statistics in the db
        death_stats = DeathStatistics.objects
        serializer = DeathStatisticsSerializer(death_stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeathStatisticsDetailApiView(APIView):
    # permission class to check if the user is authenticated
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, name, *args, **kwargs):
        # get the covid case statistics of all countys that contain the name string
        death_stats = DeathStatistics.objects.filter(county_name__icontains=name)
        if not death_stats:
            return Response(
                {"res": "There is no county with the given name"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = DeathStatisticsSerializer(death_stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DepartmentsApiView(APIView):
    # permission class to check if the user is authenticated
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    # List all the departments in the database
    def get(self, request, *args, **kwargs):
        # get all departments in the db
        departments = Departments.objects
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DepartmentsDetailApiView(APIView):
    # permission class to check if the user is authenticated
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, id, *args, **kwargs):
        # get the departments of the given county id
        departments = Departments.objects.filter(county_id=id)
        if not departments:
            return Response(
                {"res": "There is department in the county with the given county id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LocationsApiView(APIView):
    # permission class to check if the user is authenticated
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        searched_county = request.GET.get('county')
        department = request.GET.get('department')
        print("search: ", searched_county)
        print("department: ", department)

        if searched_county is not None and department is not None:
            dataset = []
            success = False
            if department == "wildfires" or department == "all":
                success = True
                # send location data of all wildfires
                if searched_county == "":
                    new_dataset = list(Wildfires.objects.all())
                else:
                    new_dataset = list(Wildfires.objects.filter(county__county_name__icontains=searched_county))
                for data_item in new_dataset:
                    data_item.department = "wildfires"

                dataset += new_dataset

            if department == "blocked_roads" or department == "all":
                success = True
                # send location data of all the blocked roads
                if searched_county == "":
                    new_dataset = list(BlockedRoads.objects.all())
                else:
                    new_dataset = list(BlockedRoads.objects.filter(county__county_name__icontains=searched_county))
                for data_item in new_dataset:
                    data_item.department = "blocked_roads"

                dataset += new_dataset

            if department == "security" or department == "all":
                success = True
                # send location data of all the security concerns
                if searched_county == "":
                    new_dataset = list(SecurityConcerns.objects.all())
                else:
                    new_dataset = list(SecurityConcerns.objects.filter(county__county_name__icontains=searched_county))
                for data_item in new_dataset:
                    data_item.department = "security"

                dataset += new_dataset

            if department == "weather" or department == "all":
                success = True
                # send location data of all the weather events
                if searched_county == "":
                    new_dataset = list(WeatherEvents.objects.all())
                else:
                    new_dataset = list(WeatherEvents.objects.filter(county__county_name__icontains=searched_county))
                for data_item in new_dataset:
                    data_item.department = "weather"

                dataset += new_dataset

            if not success:
                # department doesn't exist
                return Response(
                    {"res": "Department doesn't exist"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not dataset:
                return Response(
                    {"res": "There is no dataset in a county that matches the search"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = LocationSerializer(dataset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            # one or both parameters missing
            return Response(
                {"res": "Request didn't provide county and department values"},
                status=status.HTTP_400_BAD_REQUEST
            )

