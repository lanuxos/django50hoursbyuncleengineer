from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import random
import io
import csv
from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.utils import timezone
from django.core.paginator import Paginator

from songline import Sendline
token = 'ZSId8kzP5KNPDqABu5t6Mv87pwhrLK6Iq9kM7AlOEQ3'
messenger = Sendline(token)
# register mail confirm


def GenerateToken(domain='http://localhost:8000/confirm/'):
    allChar = [chr(i) for i in range(65, 91)]
    allChar.extend([chr(i) for i in range(97, 123)])
    allChar.extend([str(i) for i in range(10)])
    emailToken = ''
    for i in range(50):
        emailToken += random.choice(allChar)
    url = domain + emailToken
    return (url, emailToken)


def Confirm(request, token):
    try:
        check = VerifyEmail.objects.get(token=token)
        status = 'found'
        check.approved = True
        check.save()
        context = {'status': status, 'username': check.user.username,
                   'name': check.user.first_name}
    except:
        status = 'notFound'
        context = {'status': status}

    return render(request, 'myapp/confirm.html', context)


# def sendthai(sendto):

#     me = 'uncle.django50@gmail.com'
#     you = sendto

#     # Create message container - the correct MIME type is multipart/alternative.

#     msg = MIMEMultipart('alternative')
#     msg['Subject'] = "Confirmation email"
#     msg['From'] = me
#     msg['To'] = you

#     # Create the body of the message (a plain-text and an HTML version).
#     emailContent = '''
#     For security issue, please confirm your registation.
#     Else, your account would be limited for further purchasing order
#     '''
#     link = GenerateToken()
#     text = "สวัสดี!\nคุณสบายดีไหม?\n {}\n Click here to verify your registation {}".format(
#         emailContent, link)

#     html = """\

# 	<html>

# 	  <head></head>

# 	  <body>

# 	    <p>สวัสดีครับ!<br>

# 	       คุณสบายดีไหม?<br>

# 	    </p>

# 	  </body>

# 	</html>

# 	"""

#     # Record the MIME types of both parts - text/plain and text/html.

#     part1 = MIMEText(text, 'plain')  # ส่งแบบ text
#     # part2 = MIMEText(html, 'html') # ส่งแบบ html
#     msg.attach(part1)

#     # msg.attach(part2)

#     s = smtplib.SMTP('smtp.gmail.com:587')
#     s.ehlo()
#     s.starttls()
#     s.login('uncle.django50@gmail.com', "c0'Fdh50")
#     s.sendmail(me, you.split(','), msg.as_string())

#     #s.sendmail(sender, recipients.split(','), msg.as_string())

#     s.quit()


def sendthai(sendto, subj="ทดสอบส่งเมลลล์", detail="สวัสดี!\nคุณสบายดีไหม?\n"):

    myemail = 'uncle.django50@gmail.com'
    mypassword = "c0'Fdh50"
    receiver = sendto

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subj
    msg['From'] = 'Picturer.com'
    msg['To'] = receiver
    text = detail

    part1 = MIMEText(text, 'plain')
    msg.attach(part1)

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()

    s.login(myemail, mypassword)
    s.sendmail(myemail, receiver.split(','), msg.as_string())
    s.quit()


###########Start sending#############
def EmailConfirm(email, name, token):
    subject = 'Register confirmation email'
    member = name
    content = '''Due to security concern, please confirm your registation.
    otherwise system would banned your account in 24 hours, 
    which you would not able to make an order,
    regard, 
    admin--
    '''
    link = token
    msg = 'Dear {},\n {}\n{}\n'.format(member, content, link)
    #sendthai('phpsth@gmail.com', subject, msg)
    sendthai(email, subject, msg)

# หากต้องการส่งหลายคนสามารถใส่คอมม่าใน string ได้เลย เช่น 'loongTu1@gmail.com,loongTu2@gmail.com'

# sendthai('phpsth@gmail.com')


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

    # if request.method == 'POST' or request.FILES['imageUpload']:
    if request.method == 'POST':
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
        try:
            file_image = request.FILES['imageUpload']
            file_image_name = request.FILES['imageUpload'].name.replace(
                ' ', '')
            print('FILES_IMAGE:', file_image)
            print('IMAGE_NAME:', file_image_name)
            fs = FileSystemStorage()
            filename = fs.save(file_image_name, file_image)
            upload_file_url = fs.url(filename)
            # 6: mean start index 6 up, slide string from 0-5 index
            new.image = upload_file_url[6:]
        except:
            new.image = '/default.jpg'
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

        # function send mail for register confirm
        token, token_code = GenerateToken()
        #print(token, token_code)
        EmailConfirm(email, first_name, token)
        getUser = User.objects.get(username=email)
        addVerify = VerifyEmail()
        addVerify.user = getUser
        addVerify.token = token_code
        print(getUser)
        addVerify.save()
        # sendthai('phpsth@gmail.com')
        # sendthai(email, subject, msg)

        user = authenticate(username=email, password=password)
        login(request, user)

    return render(request, 'myapp/register.html')


def Graph(request):
    product = AllProduct.objects.all()
    pdName = []
    pdQuan = []
    for pd in product:
        pdName.append(pd.name)
        pdQuan.append(pd.quantity)
    context = {'pdName': str(pdName), 'pdQuan': pdQuan}
    return render(request, 'myapp/graph.html', context)


def Product(request):

    product = AllProduct.objects.all().order_by('name')
    #product = AllProduct.objects.all().order_by('name').reverse()
    paginator = Paginator(product, 3)
    page = request.GET.get('page')
    product = paginator.get_page(page)
    context = {'product': product}
    return render(request, 'myapp/allProduct.html', context)


def ProductCategory(request, code):
    select = Category.objects.get(id=code)
    product = AllProduct.objects.filter(
        catName=select).order_by('id').reverse()
    #product = AllProduct.objects.all().order_by('name').reverse()
    paginator = Paginator(product, 3)
    page = request.GET.get('page')
    product = paginator.get_page(page)
    context = {'product': product, 'catName': select.catName}
    return render(request, 'myapp/allProductCat.html', context)


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
            productOrder = ''
            productTotal = 0
            for pd in myCart:
                order = OrderList()
                order.orderId = orderId
                order.productId = pd.productId
                order.productName = pd.productName
                order.price = pd.price
                order.quantity = pd.quantity
                order.total = pd.total
                order.save()
                # product order and total for line notify
                productOrder = productOrder + '- {}\n'.format(pd.productName)
                productTotal += pd.total
            # text for line notify
            textToLine = 'ODID: {}\n--\n{}Sum: USD__{:,.2f}__\n({})'.format(orderId, productOrder,
                                                                            productTotal, name)
            if productTotal > 500000:
                messenger.sticker(14, 1, textToLine)
            else:
                messenger.sendtext(textToLine)

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
    paginator = Paginator(order, 3)
    page = request.GET.get('page')
    order = paginator.get_page(page)
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


def matPrice(m):
    mp = Materials.objects.filter(name='price')
    m1 = Materials.objects.filter(name=m)
    price = 0
    for i in mp:
        for j in m1:
            i.m1 = 0 if i.m1 is None else i.m1
            i.m2 = 0 if i.m2 is None else i.m2
            i.m3 = 0 if i.m3 is None else i.m3
            i.m4 = 0 if i.m4 is None else i.m4
            i.m5 = 0 if i.m5 is None else i.m5
            j.m1 = 0 if j.m1 is None else j.m1
            j.m2 = 0 if j.m2 is None else j.m2
            j.m3 = 0 if j.m3 is None else j.m3
            j.m4 = 0 if j.m4 is None else j.m4
            j.m5 = 0 if j.m5 is None else j.m5
            price = (i.m1*j.m1) + (i.m2*j.m2) + \
                (i.m3 * j.m3) + (i.m4 * j.m4), (i.m5 * j.m5)
            return price


def unitPrice(name, rate=9200):
    price = 0
    matPrice = Materials.objects.filter(name='price')
    components = Materials.objects.filter(name=name)
    for p in matPrice:
        for c in components:
            ####################################
            def zero(z):
                z = 0 if z is None else z
                return(z)
            p.m1 = zero(p.m1)
            p.m2 = zero(p.m2)
            p.m3 = zero(p.m3)
            p.m4 = zero(p.m4)
            p.m5 = zero(p.m5)
            c.m1 = zero(c.m1)
            c.m2 = zero(c.m2)
            c.m3 = zero(c.m3)
            c.m4 = zero(c.m4)
            c.m5 = zero(c.m5)
            price = (p.m1 * c.m1) + (p.m2 * c.m2) + \
                (p.m3 * c.m3) + (p.m4 * c.m4) + (p.m5 * c.m5)
            ####################################
            # p.m1 = 0 if p.m1 is None else p.m1
            # p.m2 = 0 if p.m2 is None else p.m2
            # p.m3 = 0 if p.m3 is None else p.m3 * rate
            # p.m4 = 0 if p.m4 is None else p.m4
            # p.m5 = 0 if p.m5 is None else p.m5
            # c.m1 = 0 if c.m1 is None else c.m1
            # c.m2 = 0 if c.m2 is None else c.m2
            # c.m3 = 0 if c.m3 is None else c.m3
            # c.m4 = 0 if c.m4 is None else c.m4
            # c.m5 = 0 if c.m5 is None else c.m5
            # price = (p.m1 * c.m1) + (p.m2 * c.m2) + \
            #     (p.m3 * c.m3) + (p.m4 * c.m4) + (p.m5 * c.m5)
    return price


def TestFunction(request):
    rate = 10000
    cloth = unitPrice('cloth', rate)
    uniform = unitPrice('uniform', rate)
    hat = unitPrice('hat', rate)

    context = {'cloth': cloth,
               'uniform': uniform, 'hat': hat}
    return render(request, 'myapp/test.html', context)

# https://medium.com/@ramramesh1374/upload-csv-using-django-bulk-create-c75b28fc19f0
# class MaterialsUpload(View):
#     def get(self, request):
#         template_name = 'importfarmer.html'
#         return render(request, template_name)

#     def post(self, request):
#         user = request.user  # get the current login user details
#         paramFile = io.TextIOWrapper(request.FILES['employeefile'].file)
#         portfolio1 = csv.DictReader(paramFile)
#         list_of_dict = list(portfolio1)
#         objs = [
#             Employee(
#                 first_name=row['first_name'],
#                 last_name=row['last_name'],
#                 gender=('F' if row['gender'] == 'Female' else (
#                     'M' if row['gender'] == 'Male' else 'F')),
#                 dob=(row['dob'] if row['dob'] != '' else '1970-01-01'),
#                 village=row['village'],
#                 district=row['district'],
#                 phone_number=row['phone_number'],
#                 father_name=row['father_name'],
#                 preferred_language=row['preferred_language'],
#                 created_by=user,  # This is foreignkey value
#                 updated_by=user,  # This is foreignkey value

#             )
#             for row in list_of_dict
#         ]
#         try:
#             msg = Employee.objects.bulk_create(objs)
#             returnmsg = {"status_code": 200}
#             print('imported successfully')
#         except Exception as e:
#             print('Error While Importing Data: ', e)
#             returnmsg = {"status_code": 500}

#         return JsonResponse(returnmsg)
