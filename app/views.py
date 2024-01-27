from django.shortcuts import render, redirect
from .models import *
from .forms import *
import telebot
import requests
from .forms import *


# Create your views here.


def index(req):
    items = Tovar.objects.all()
    data = {'tovar': items}
    return render(req, 'index.html', data)




def toCart(req):
    items = Cart.objects.filter(user=req.user)
    forma = OrderForm()
    total = 0
    for i in items:
        total += i.calcSumma()
    total = round(total, 2)  # округление цены
    if req.POST:
        forma = OrderForm(req.POST)
        k1 = req.POST.get('adres')
        k2 = req.POST.get('tel')
        k3 = req.POST.get('email')
        if forma.is_valid():
            print(k1, k2, k3)
            k1 = forma.cleaned_data.get('adres')
            k2 = forma.cleaned_data.get('tel')
            k3 = forma.cleaned_data.get('email')
            print(k1, k2, k3)
            myzakaz = ''
            for one in items:
                myzakaz += one.tovar.name + ' '
                myzakaz += 'количество ' + str(one.count) + ' '
                myzakaz += 'сумма ' + str(one.summa) + ' '
                myzakaz += 'скидка ' + str(one.tovar.discount) + ' '
            neworder = Order.objects.create(adres=k1, tel=k2, email=k3,
                                 total=total, myzakaz = myzakaz,
                                 user=req.user)
            items.delete()
            ##################################################################################
            #в телеграм
            telegram(neworder)


            return render(req, 'sps.html')


    data = {'tovari': items, 'total': total, 'formaorder': forma}
    return render(req, 'cart.html', data)
def buy(req, id):
    item = Tovar.objects.get(id=id)
    curuser = req.user
    if Cart.objects.filter(tovar=item, user=curuser):
        getTovar = Cart.objects.get(tovar_id=id)
        getTovar.count += 1
        getTovar.summa = getTovar.calcSumma()
        getTovar.save()
    else:
        Cart.objects.create(tovar=item, count=1, user=curuser, summa=item.price)
        data = {}
    return redirect('home')


def delete(req, id):
    item = Cart.objects.get(id=id)
    item.delete()
    return redirect('tocart')


def cartCount(req, num, id):
    num = int(num)
    item = Cart.objects.get(id=id)
    item.count += num
    if item.count < 0:
        item.count = 0
    item.summa = item.calcSumma()
    item.save()
    return redirect('tocart')


# def telegram(neworder):
#     token = '6912404517:AAGymoL3sJpf10K3bOUF3xokTPM47lrDOgI'
#     #t.me/
#     chat = '528849379'
#     message = neworder.user.username + ' '+neworder.tel+ ' '+neworder.myzakaz
#     bot = telebot.TeleBot(chat,'новый заказ')
#     bot.send_message(chat, message)

    # 6912404517:AAGymoL3sJpf10K3bOUF3xokTPM47lrDOgI   токен телеграмм бота
    # t.me/pogodka2023_bot   канал телеграмм бота

    #новый  6913165680:AAEZERrWPJNyGoE8t3bzgULvO1iu8AMCsro
    #t.me/korzina326_bot

import requests
def telegram(neworder):
        token = '6913165680:AAEZERrWPJNyGoE8t3bzgULvO1iu8AMCsro'
        # t.me/turtle3000_bot
        chat = '528849379'
        message = neworder.user.username + ' ' + neworder.tel + ' ' + neworder.myzakaz
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat}&text={message}"
        requests.get(url)