from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.utils import timezone
from django.core.paginator import Paginator
# Create your views here.


def Home(request):
    product = AllProduct.objects.all().order_by('id').reverse()[:3]
    #product = AllProduct.objects.all().order_by('name').reverse()
    preOrder = AllProduct.objects.filter(quantity__lte=0)
    context = {'product': product, 'preOrder': preOrder}
    return render(request, 'myapp/home.html', context)


def About(request):
    return render(request, 'myapp/about.html')


def Contact(request):
    return render(request, 'myapp/contact.html')


def Portrait(request):
    return render(request, 'myapp/portrait.html')


def AddProduct(request):
    if request.user.profile.userType != 'admin':
        return redirect('home-page')

    if request.method == 'POST' and request.FILES['imageUpload']:
        data = request.POST.copy()
        name = data.get('name')
        price = data.get('price')
        quantity = data.get('quantity')
        unit = data.get('unit')
        detail = data.get('detail')
        imageUrl = data.get('imageUrl')

        new = AllProduct()
        new.name = name
        new.price = price
        new.quantity = quantity
        new.unit = unit
        new.detail = detail
        new.imageUrl = imageUrl
        file_image = request.FILES['imageUpload']
        file_image_name = request.FILES['imageUpload'].name.replace(' ', '')
        print('FILES_IMAGE:', file_image)
        print('IMAGE_NAME:', file_image_name)
        fs = FileSystemStorage()
        filename = fs.save(file_image_name, file_image)
        upload_file_url = fs.url(filename)
        # 6: mean start index 6 up, slide string from 0-5 index
        new.image = upload_file_url[6:]
        new.save()

    return render(request, 'myapp/addProduct.html')


def Register(request):
    if request.method == 'POST':
        data = request.POST.copy()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        newUser = User()
        newUser.username = email
        newUser.email = email
        newUser.first_name = first_name
        newUser.last_name = last_name
        newUser.set_password(password)
        newUser.save()

        profile = Profile()
        profile.user = User.objects.get(username=email)
        profile.save()

        user = authenticate(username=email, password=password)
        login(request, user)

    return render(request, 'myapp/register.html')


def Product(request):

    product = AllProduct.objects.all().order_by('name')
    #product = AllProduct.objects.all().order_by('name').reverse()
    paginator = Paginator(product, 3)
    page = request.GET.get('page')
    product = paginator.get_page(page)
    context = {'product': product}
    return render(request, 'myapp/allProduct.html', context)


def AddToCart(request, pid):
    username = request.user.username
    user = User.objects.get(username=username)
    check = AllProduct.objects.get(id=pid)

    try:
        newCart = Cart.objects.get(user=user, productId=str(pid))
        newQuantity = newCart.quantity + 1
        newCart.quantity = newQuantity
        calculate = newCart.price * newQuantity
        newCart.total = calculate
        newCart.save()

        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updateQuantity = Profile.objects.get(user=user)
        updateQuantity.cartQuantity = count
        updateQuantity.save()

        return redirect('allProduct')
    except:
        newCart = Cart()
        newCart.user = user
        newCart.productId = pid
        newCart.productName = check.name
        newCart.price = int(check.price)
        newCart.quantity = 1
        calculate = int(check.price)
        newCart.total = calculate
        newCart.save()

        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updateQuantity = Profile.objects.get(user=user)
        updateQuantity.cartQuantity = count
        updateQuantity.save()

        return redirect('allProduct')


def MyCart(request):
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}
    if request.method == 'POST':
        data = request.POST.copy()
        productId = data.get('productId')
        item = Cart.objects.get(user=user, productId=productId)
        item.delete()
        context['status'] = 'delete'

        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updateQuantity = Profile.objects.get(user=user)
        updateQuantity.cartQuantity = count
        updateQuantity.save()

    myCart = Cart.objects.filter(user=user)
    count = sum([c.quantity for c in myCart])
    total = sum([c.total for c in myCart])

    context['myCart'] = myCart
    context['count'] = count
    context['total'] = total

    #context = {'myCart': myCart}

    return render(request, 'myapp/myCart.html', context)


def MyCartEdit(request):
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}
    if request.method == 'POST':
        data = request.POST.copy()

        if data.get('clear') == 'clear':
            Cart.objects.filter(user=user).delete()
            updateQuantity = Profile.objects.get(user=user)
            updateQuantity.cartQuantity = 0
            updateQuantity.save()
            return redirect('myCart')

        editList = []
        for k, v in data.items():
            if k[:2] == 'pd':
                pid = int(k.split('_')[1])
                dt = [pid, int(v)]
                editList.append(dt)

        for ed in editList:
            edit = Cart.objects.get(productId=ed[0], user=user)
            edit.quantity = ed[1]
            edit.total = edit.price * ed[1]
            edit.save()

            count = Cart.objects.filter(user=user)
            count = sum([c.quantity for c in count])
            updateQuantity = Profile.objects.get(user=user)
            updateQuantity.cartQuantity = count
            updateQuantity.save()

        return redirect('myCart')

    myCart = Cart.objects.filter(user=user)
    context = {'myCart': myCart}

    return render(request, 'myapp/myCartEdit.html', context)


def CheckOut(request):
    username = request.user.username
    user = User.objects.get(username=username)
    if request.method == 'POST':
        data = request.POST.copy()
        name = data.get('name')
        tel = data.get('tel')
        address = data.get('address')
        shipping = data.get('shipping')
        payment = data.get('payment')
        other = data.get('other')
        page = data.get('page')

        if page == 'information':
            context = {}
            context['name'] = name
            context['tel'] = tel
            context['address'] = address
            context['shipping'] = shipping
            context['payment'] = payment
            context['other'] = other
            myCart = Cart.objects.filter(user=user)
            count = sum([c.quantity for c in myCart])
            total = sum([c.total for c in myCart])

            context['myCart'] = myCart
            context['count'] = count
            context['total'] = total
            return render(request, 'myapp/checkOut2.html', context)

        if page == 'confirm':
            myCart = Cart.objects.filter(user=user)
            mid = str(user.id).zfill(4)
            dt = datetime.now().strftime('%Y%m%d%H%M%S')
            orderId = 'OD' + mid + dt
            for pd in myCart:
                order = OrderList()
                order.orderId = orderId
                order.productId = pd.productId
                order.productName = pd.productName
                order.price = pd.price
                order.quantity = pd.quantity
                order.total = pd.total
                order.save()

            odp = OrderPending()
            odp.orderId = orderId
            odp.user = user
            odp.name = name
            odp.tel = tel
            odp.address = address
            odp.shipping = shipping
            odp.payment = payment
            odp.other = other
            odp.save()

            Cart.objects.filter(user=user).delete()
            updateQuantity = Profile.objects.get(user=user)
            updateQuantity.cartQuantity = 0
            updateQuantity.save()
            return redirect('myCart')

    return render(request, 'myapp/checkOut1.html')


def OrderListPage(request):
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}

    order = OrderPending.objects.filter(user=user)

    for od in order:
        orderId = od.orderId
        odList = OrderList.objects.filter(orderId=orderId)
        total = sum([c.total for c in odList])
        od.total = total

        count = sum([c.quantity for c in odList])
        #odDetail = OrderPending.objects.get(orderId=orderId)
        if od.shipping == 'ems':
            shipCost = sum([10000 if i == 0 else 5000 for i in range(count)])
        # first piece shipment cost is 10k and 5k a piece for the second piece
        else:
            shipCost = sum([5000 if i == 0 else 2000 for i in range(count)])

        if od.payment == 'cod':
            shipCost += 5000

        od.shipCost = shipCost

    context['allOrder'] = order

    return render(request, 'myapp/orderList.html', context)


def AllOrderListPage(request):
    context = {}

    order = OrderPending.objects.all()

    for od in order:
        orderId = od.orderId
        odList = OrderList.objects.filter(orderId=orderId)
        total = sum([c.total for c in odList])
        od.total = total

        count = sum([c.quantity for c in odList])
        #odDetail = OrderPending.objects.get(orderId=orderId)
        if od.shipping == 'ems':
            shipCost = sum([10000 if i == 0 else 5000 for i in range(count)])
        # first piece shipment cost is 10k and 5k a piece for the second piece
        else:
            shipCost = sum([5000 if i == 0 else 2000 for i in range(count)])

        if od.payment == 'cod':
            shipCost += 5000

        od.shipCost = shipCost

    context['allOrder'] = order

    return render(request, 'myapp/allOrderList.html', context)


def UploadSlip(request, orderId):
    if request.method == 'POST' and request.FILES['slip']:
        data = request.POST.copy()
        slipTime = data.get('slipTime')
        update = OrderPending.objects.get(orderId=orderId)
        update.slipTime = slipTime
        file_image = request.FILES['slip']
        file_image_name = request.FILES['slip'].name.replace(' ', '')
        print('FILE_IMAGE:', file_image)
        print('IMAGE_NAME', file_image_name)
        fs = FileSystemStorage()
        filename = fs.save(file_image_name, file_image)
        upload_file_url = fs.url(filename)
        update.slip = upload_file_url[6:]
        update.save()

    odList = OrderList.objects.filter(orderId=orderId)
    total = sum([c.total for c in odList])
    odDetail = OrderPending.objects.get(orderId=orderId)
    count = sum([c.quantity for c in odList])
    #print('COUNT>>>', count)
    if odDetail.shipping == 'ems':
        shipCost = sum([10000 if i == 0 else 5000 for i in range(count)])
        # first piece shipment cost is 10k and 5k a piece for the second piece
    else:
        shipCost = sum([5000 if i == 0 else 2000 for i in range(count)])

    if odDetail.payment == 'cod':
        shipCost += 5000
    context = {'orderId': orderId, 'total': total, 'grandTotal': total + shipCost,
               'shipCost': shipCost, 'odDetail': odDetail, 'count': count}

    return render(request, 'myapp/uploadSlip.html', context)


def UpdatePaid(request, orderId, status):

    if request.user.profile.userType != 'admin':
        return redirect('home-page')

    order = OrderPending.objects.get(orderId=orderId)
    if status == 'confirm':
        order.paid = True
    elif status == 'cancel':
        order.paid = False
    order.save()

    return redirect('allOrderList')


def UpdateTracking(request, orderId):
    if request.user.profile.userType != 'admin':
        return redirect('home-page')

    if request.method == 'POST':
        order = OrderPending.objects.get(orderId=orderId)
        data = request.POST.copy()
        trackingNumber = data.get('trackingNumber')
        order.trackingNumber = trackingNumber
        order.save()
        return redirect('allOrderList')

    order = OrderPending.objects.get(orderId=orderId)
    odList = OrderList.objects.filter(orderId=orderId)

    total = sum([c.total for c in odList])
    order.total = total
    count = sum([c.quantity for c in odList])
    #print('COUNT>>>', count)
    if order.shipping == 'ems':
        shipCost = sum([10000 if i == 0 else 5000 for i in range(count)])
        # first piece shipment cost is 10k and 5k a piece for the second piece
    else:
        shipCost = sum([5000 if i == 0 else 2000 for i in range(count)])

    if order.payment == 'cod':
        shipCost += 5000

    order.shipCost = shipCost

    context = {'order': order, 'odList': odList,
               'total': total, 'count': count}

    return render(request, 'myapp/updateTracking.html', context)


def MyOrder(request, orderId):
    username = request.user.username
    user = User.objects.get(username=username)

    order = OrderPending.objects.get(orderId=orderId)
    if user != order.user:
        return redirect('allProduct')
    odList = OrderList.objects.filter(orderId=orderId)

    total = sum([c.total for c in odList])
    order.total = total
    count = sum([c.quantity for c in odList])
    #print('COUNT>>>', count)
    if order.shipping == 'ems':
        shipCost = sum([10000 if i == 0 else 5000 for i in range(count)])
        # first piece shipment cost is 10k and 5k a piece for the second piece
    else:
        shipCost = sum([5000 if i == 0 else 2000 for i in range(count)])

    if order.payment == 'cod':
        shipCost += 5000

    order.shipCost = shipCost

    context = {'order': order, 'odList': odList,
               'total': total, 'count': count}

    return render(request, 'myapp/myOrder.html', context)
