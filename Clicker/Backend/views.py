from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from Backend.forms import *
from .models import *
from .serializers import *


class Register(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            core = Core(user=user)  # Создаем экземпляр класса Core и пихаем в него модель юзера
            core.save()  # Сохраняем изменения в базу
            return redirect('index')

        return render(request, 'register.html', {'form': form})


class Login(APIView):
    form = UserForm()

    def get(self, request):
        return render(request, 'login.html', {'form': self.form})

    def post(self, request):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('index')
        return render(request, 'login.html', {'form': self.form, 'invalid': True})


@login_required
def index(request):
    core = Core.objects.get(user=request.user)
    boosts = Boost.objects.filter(core=core)

    return render(request, 'index.html', {
        'core': core,
        'boosts': boosts,
    })


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@api_view(['GET'])
@login_required
def call_click(request):
    core = Core.objects.get(user=request.user)
    is_levelup = core.click()
    if is_levelup:
        Boost.objects.create(core=core, price=core.coins, power=core.level*2)
    core.save()

    return Response({'core': CoreSerializer(core).data, 'is_levelup': is_levelup })


@api_view(['GET'])
@login_required
def get_rank(request, pk):
    rank = Rank.objects.get(power=pk)
    return Response({'rank': RankSerializer(rank).data})


class BoostViewSet(viewsets.ModelViewSet):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer

    def get_queryset(self):
        core = Core.objects.get(user=self.request.user)
        boosts = Boost.objects.filter(core=core)
        return boosts

    def partial_update(self, request, pk):
        coins = request.data['coins']  # Получаем количество монет из тела запроса.
        boost = self.queryset.get(pk=pk)

        is_levelup = boost.levelup(
            coins)  # Передадим количество монет в метод. Этот метод мы скоро немного подкорректируем.
        if not is_levelup:
            return Response({"error": "Не хватает денег"})
        old_boost_stats, new_boost_stats = is_levelup

        return Response({
            "old_boost_stats": self.serializer_class(old_boost_stats).data,
            "new_boost_stats": self.serializer_class(new_boost_stats).data,
        })


@api_view(['POST'])
def update_coins(request):
    coins = request.data['current_coins']
    core = Core.objects.get(user=request.user)

    is_levelup, boost_type = core.set_coins(
        coins)

    if is_levelup:
        Boost.objects.create(core=core, price=core.coins, power=core.level * 2,
                             type=boost_type)
    core.save()

    return Response({
        'core': CoreSerializer(core).data,
        'is_levelup': is_levelup,
    })


@api_view(['GET'])
def get_core(request):
    core = Core.objects.get(user=request.user)
    return Response({'core': CoreSerializer(core).data})