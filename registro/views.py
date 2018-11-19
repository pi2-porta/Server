from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings

# from .decorators import validate_request_data
from .models import Registros

from .models import Profile
from .serializers import RegistrosSerializer, TokenSerializer, UserSerializer

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from .serializers import RegistrosSerializer
from .decorators import validate_request_data

#face recognition
import face_recognition
import numpy as np
import cv2
import base64

#system
import sys

##### To copy and paste when working on shell
# from django.contrib.auth.models import User
# from registro.models import Profile
# import face_recognition

class ListCreateRegistrosView(generics.ListCreateAPIView):
    """
    GET songs/
    POST songs/
    """
    queryset = Registros.objects.all()
    serializer_class = RegistrosSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        r = Registros.objects.create(
            title=request.data["title"],
            description=request.data["description"],
            author=request.user
        )

        return Response(
            data=RegistrosSerializer(r).data,
            status=status.HTTP_201_CREATED
        )

class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class RegisterUsersView(generics.CreateAPIView):
    """
    POST auth/register/

    http -f -a admin:toortoor POST http://127.0.0.1:8000/auth/register/ username='anderson-a3' password='toortoor' email='teste@email.com' photo@a3.jpg

    http -f -a admin:toortoor POST http://127.0.0.1:8000/auth/register/ username='anderson-a1' password='toortoor' email='teste@email.com' photo@a1.jpg


    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        photo = request.data.get("photo")

        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )

        new_user.profile.image = photo


        new_face = face_recognition.load_image_file(new_user.profile.image.path)

        try:
             new_face_encoding = face_recognition.face_encodings(new_face)[0]

        except IndexError:
            print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")


        new_user.profile.encode = base64.b64encode(new_face_encoding)

        new_user.save()

        return Response(status=status.HTTP_201_CREATED)

class SearchUserPhotoView(generics.ListCreateAPIView):




    permission_classes = (permissions.AllowAny,)



    def post(self, request, *args, **kwargs):

        print('*********************')
        print('Trying to search')
        print('*********************')

        queryset = User.objects.all()

        users_list = []

        for u in queryset:
            if u.username != 'admin':
                users_list.append(u)



        photo = request.data.get("photo")
        jpg_original = base64.b64decode(photo)
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        image_buffer = cv2.imdecode(jpg_as_np, flags=1)

        # unknown_face = face_recognition.load_image_file(photo.path)
        #
        # try:
        #      unknown_face_encoding = face_recognition.face_encodings(unknown_face)
        #
        # except IndexError:
        #     print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")

        rgb_frame = image_buffer[:, :, ::-1]
        a = face_recognition.face_locations(rgb_frame)


        unknown_face = face_recognition.face_encodings(rgb_frame, a)



        # print(request.data)

        resultado = False
        for u in users_list:

            found = False
            results = []

            encode = u.profile.encode
            t = base64.decodestring(bytes(encode[2:-1], 'utf-8'))
            q = np.frombuffer(t, dtype=np.float64)

            results = face_recognition.compare_faces(unknown_face, q)

            # print(results)


            if True in results:
                resultado = True


        return Response(
            data=resultado,
            status=status.HTTP_201_CREATED
        )

    def str_to_float(self, member):

        aux = ''

        for digit in member:
            if digit.isdigit() or digit == '-' or digit == '.':
                aux = aux + digit

        return float(aux)


    def to_float(self, encode):

        list_float = []

        for member in encode:

            try:
                a = float(member)
                list_float.append(a)

            except ValueError:

                a = self.str_to_float(member)
                list_float.append(a)


        return list_float


##### How to perform a search #####

        ## 1 load the images
        # images of anderson
        # know_face1 = [-0.13063231110572815, 0.07222828269004822, 0.031763479113578796, -0.04685777425765991, 0.04825626686215401, -0.061730142682790756, -0.012349395081400871, -0.049780916422605515, 0.16156131029129028, 0.03774203360080719, 0.2385108470916748, -0.0692657083272934, -0.27687427401542664, -0.07049239426851273, -0.059916555881500244, 0.08086176961660385, -0.15758967399597168, -0.046624861657619476, -0.022897994145751, -0.06899455934762955, 0.16142918169498444, 0.0325346402823925, 0.04822288081049919, 0.11169326305389404, -0.1765935868024826, -0.25906816124916077, -0.11103732883930206, -0.23083223402500153, -0.033194974064826965, -0.11424095183610916, 0.003196246922016144, 0.04642607271671295, -0.17114272713661194, -0.09613554179668427, 0.043350398540496826, 0.04807956516742706, 0.029366742819547653, -0.0029822951182723045, 0.1568576991558075, -0.02314198762178421, -0.06785973906517029, 0.025691993534564972, 0.07861651480197906, 0.2500036060810089, 0.11328930407762527, 0.08197513967752457, 0.0326819010078907, -0.0731767863035202, 0.0736461877822876, -0.1639249175786972, 0.03604254126548767, 0.14915665984153748, 0.1101657822728157, 0.10603848099708557, 0.11799561232328415, -0.21999052166938782, 0.040403928607702255, 0.058643121272325516, -0.1947893351316452, 0.10494764149188995, 0.009523062035441399, 0.04591841995716095, 0.023345869034528732, 0.01174921914935112, 0.1470184028148651, 0.013395896181464195, -0.13693572580814362, -0.13161778450012207, 0.10418816655874252, -0.124150350689888, 0.006612334866076708, 0.15244977176189423, -0.1655939668416977, -0.21261538565158844, -0.2107650637626648, 0.06774765253067017, 0.37779825925827026, 0.10254441946744919, -0.1619906723499298, 0.06742089986801147, -0.14698411524295807, -0.06122663617134094, -0.0051563153974711895, -0.029112113639712334, -0.06375546753406525, 0.06383908540010452, -0.11176241934299469, 0.046253662556409836, 0.12393170595169067, -0.009638517163693905, -0.005097255110740662, 0.22301527857780457, -0.03319810703396797, 0.02581140026450157, 0.03488681837916374, 0.051913440227508545, -0.14157575368881226, 0.029413556680083275, -0.10066477954387665, -0.0034109968692064285, -0.00012092851102352142, -0.0980582982301712, -0.015634719282388687, 0.04325712099671364, -0.1813959926366806, 0.057252150028944016, 0.0090958122164011, -0.05859658122062683, -0.14791423082351685, 0.091862753033638, -0.18304342031478882, 0.011791463010013103, 0.15200425684452057, -0.3103831708431244, 0.20633459091186523, 0.1685505211353302, 0.05102265626192093, 0.1069159209728241, 0.03604549542069435, 0.04542996734380722, 0.0017627449706196785, -0.011518938466906548, -0.10516496002674103, -0.07143016159534454, 0.06797703355550766, 0.01782984659075737, 0.030334187671542168, -0.01718980073928833]
        # know_face2 = [-0.13000649213790894, -0.005401216447353363, -0.01768871396780014, -0.04193537309765816, 0.022879011929035187, -0.07784784585237503, 0.0026793479919433594, -0.08824603259563446, 0.17868760228157043, -0.047364380210638046, 0.25111621618270874, -0.14315766096115112, -0.27892589569091797, -0.04912521317601204, -0.0427793487906456, 0.10899307578802109, -0.1273891031742096, -0.04858766496181488, -0.031227000057697296, -0.1426539123058319, 0.1006137877702713, -0.026030711829662323, 0.040069833397865295, 0.11242645978927612, -0.16925643384456635, -0.28571075201034546, -0.11957480013370514, -0.195742666721344, -0.028554577380418777, -0.11072291433811188, 0.00960079301148653, 0.09213856607675552, -0.14014050364494324, -0.05923163890838623, 0.04379504173994064, 0.09890919178724289, -0.01407563779503107, -0.07460770010948181, 0.1808795928955078, -0.06260817497968674, -0.06221398711204529, -0.0038498910143971443, 0.06345327198505402, 0.21183818578720093, 0.05283612757921219, 0.019843198359012604, 0.05372127890586853, -0.08727855980396271, 0.10538564622402191, -0.2048777937889099, 0.004695497453212738, 0.11592253297567368, 0.06807945668697357, 0.09673892706632614, 0.12198566645383835, -0.2216232866048813, 0.07867345213890076, 0.1243555098772049, -0.19108663499355316, 0.11597792059183121, 0.026076722890138626, 0.004250654950737953, -0.017903070896863937, 0.027013063430786133, 0.2130969911813736, 0.09427732229232788, -0.1726042628288269, -0.10240693390369415, 0.14280559122562408, -0.11480828374624252, 0.03283035755157471, 0.1263718456029892, -0.12979629635810852, -0.279413640499115, -0.21322672069072723, 0.11505253612995148, 0.42050594091415405, 0.10984590649604797, -0.16433842480182648, 0.0750989094376564, -0.09056331217288971, -0.007056993432343006, 0.07506296783685684, 0.032762255519628525, -0.09495681524276733, 0.027809932827949524, -0.12597015500068665, 0.018353722989559174, 0.13689911365509033, 0.012857012450695038, -0.05041830986738205, 0.2199835181236267, -0.035099130123853683, 0.07440488785505295, 0.06330433487892151, 0.08151236921548843, -0.13606007397174835, -0.008932802826166153, -0.08361651003360748, 0.038641929626464844, 0.06641673296689987, -0.15184080600738525, -0.04903388023376465, 0.027278264984488487, -0.15259277820587158, 0.09668848663568497, -0.023563750088214874, -0.05640627443790436, -0.12136223912239075, 0.07460220903158188, -0.13702085614204407, 0.05298686400055885, 0.12481347471475601, -0.3832443356513977, 0.18600891530513763, 0.1672016978263855, 0.07583265751600266, 0.1981685608625412, 0.04950713366270065, 0.04828707128763199, 0.03781736269593239, -0.021873120218515396, -0.1272525191307068, -0.07510857284069061, 0.04061233252286911, 0.03389164060354233, -0.015510239638388157, -0.0027051903307437897]

        # list float

        #####
        ## 2 store into an list
        # know_faces = [
        #     know_face1,
        #     know_face2
        # ]

        # list of list

        ## 3 ivk the compare method, that store the results on array
        # r = face_recognition.compare_faces(new_user.profile.encode, know_faces)

        # print('***')
        # print(r)
        # print('***')
