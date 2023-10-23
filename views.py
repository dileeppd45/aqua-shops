from urllib import request

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage



def index(request):
    return render(request,'HomePage.html')

def AdminHomePage(request):
    return render(request, 'Admin/AdminHomePage.html')

def UserHome(request):
    return render(request,"User/UserHome.html")

def SellersHome(request):
    return render(request,"Seller/SellersHome.html")

def login(request):
    return render(request,"login.html")

def login1(request):
    if request.method == "POST":
        name = request.POST['un']
        password = request.POST['pass']
        request.session['lid']=name
        cursor = connection.cursor()
        cursor.execute ("select * from login where admin_id='" + name + "' and password='" + password + "'")
        print("select * from login where admin_id='" + name + "' and password='" + password + "'")
        pins = cursor.fetchone()
        flag='error'
        if pins == None:
            print("not admin")
            cursorF = connection.cursor()
            cursorF.execute("select * from user_register where user_id='" + name + "' and password='" + password + "'")
            print("select * from user_register where user_id='" + name + "' and password='" + password + "'")
            sell = cursorF.fetchone()
            if sell == None:
                print("not user")
                cursorx = connection.cursor()
                cursorx.execute("select status,seller_id from sellers where seller_id='" + name + "' and password='" + password + "'")
                print("select status,seller_id from sellers where seller_id='" + name + "' and password='" + password + "'")
                nut=cursorx.fetchone()
                if nut is not None:
                    n = nut[0]
                    status = n
                    print(status)
                    x = nut[1]
                    print(x)
                    request.session['hid'] = x
                    if (status == 'pending'):
                        return HttpResponse("<script>alert('Pending please wait');window.location='login';</script>")
                    elif (status == 'rejected'):
                        return HttpResponse("<script>alert('Your Request Rejected');window.location='login';</script>")
                    elif (status == 'approve'):
                        return redirect("/SellersHome")
            else:
                flag = 'sell'
                print("food insp")
        else:
            flag="admin"
            print("this is admin")
    print("flag is:"+flag)
    if flag=="admin":
        return redirect("/AdminHomePage")
    if flag=="sell":
        return redirect("/UserHome")
    if flag == "error":
        return HttpResponse("<script>alert('invalid');window.location='login';</script>")

    return HttpResponse("<script>alert('invalid');window.location='login';</script>")


def logout(request):
    return render(request,'Admin/logout.html')
def ulogout(request):
    return render(request,'User/logout.html')
def slogout(request):
    return render(request,'Seller/logout.html')


def viewAllNewSellerRequest(request):
    cursor = connection.cursor()
    cursor.execute("select * from sellers where status='pending'")
    pin = cursor.fetchall()
    print(pin)
    return render(request,"Admin/viewAllNewSellerRequest.html",{'data':pin})

def approvesell(request,sid):
    cursor = connection.cursor()
    cursor.execute("update sellers set status='approve' where seller_id='" + str(sid) + "'")
    return redirect("/viewAllNewSellerRequest")

def Rejectsell(request,sid):
    cursor = connection.cursor()
    cursor.execute("update sellers set status='rejected' where seller_id='" + str(sid) + "'")
    return redirect("/viewAllNewSellerRequest")


def viewsellerBookingsAdmin(request):
    cursor = connection.cursor()
    cursor.execute("select * from user_bookings where status='paid'")
    pin = cursor.fetchall()
    return render(request,"Admin/viewsellerBookingsAdmin.html",{'data':pin})


def viewsellerAdmin(request):
    cursor = connection.cursor()
    cursor.execute("select * from sellers where status='approve'")
    pin = cursor.fetchall()
    return render(request,"Admin/viewsellerAdmin.html",{'data':pin})


def viewcustomer (request):
    cursor = connection.cursor()
    cursor.execute("select * from user_register ")
    pin = cursor.fetchall()
    print(pin)
    return render(request,"Admin/viewcustomer.html",{'data':pin})




def addCategory(request):
    if request.method == "POST":
        name = request.POST['txtname']
        cursor = connection.cursor()
        cursor.execute("insert into category values(null,'" +name+"')")
        return HttpResponse("<script>alert('Category Added');window.location='/AdminHomePage';</script>")
    return render(request,"Admin/addCategory.html")



def viewCategory(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    pin = cursor.fetchall()
    print(pin)
    return render(request,"Admin/viewCategory.html",{'data':pin})


def editCategory(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from category where category_id='"+str(id)+"'")
    pin = cursor.fetchall()
    print(pin)
    return render(request,"Admin/editCategory.html",{'data':pin})

def UpdateCategory(request,id):
    if request.method == "POST":
        name = request.POST['name']
        cursor = connection.cursor()
        cursor.execute("update category set name='" + name + "' where category_id='" + str(id) + "'")
        return HttpResponse("<script>alert('Updated');window.location='/viewCategory';</script>")
    return render(request,"Admin/editCategory.html")





def deleteCategory(request,cid):
    cursor = connection.cursor()
    cursor.execute ("delete from category where category_id='"+str(cid)+"'")
    return HttpResponse( "<script>alert('Deleted Succesfully');window.location='/viewCategory';</script>")



def ViewNotificationAdmin(request):
    cursor = connection.cursor()
    cursor.execute("select * from notification where status='pending'")
    pin = cursor.fetchall()
    print(pin)
    return render(request,"Admin/ViewNotificationAdmin.html",{'data':pin})


def approvenoti(request,id):
    cursor = connection.cursor()
    cursor.execute("update notification set status='approved' where idnotification='" + str(id) + "'")
    return redirect("/ViewNotificationAdmin")


def ViewNotificationAdminApproved(request):
    cursor = connection.cursor()
    cursor.execute("select * from notification where status='approved'")
    pin = cursor.fetchall()
    print(pin)
    return render(request,"Admin/ViewNotificationAdminApproved.html",{'data':pin})



#-------------------------------------------Seller------------------------------------------------------------------------#



def addseller(request):
    if request.method == "POST":
        seller_id = request.POST['seller_id']
        name = request.POST['TxtName']
        address = request.POST['TxtAddress']
        phone = request.POST['TxtPhone']
        email = request.POST['TxtEmail']
        password = request.POST['password']
        cursor = connection.cursor()
        cursor.execute("select * from login where admin_id ='"+str(seller_id)+"' ")
        data = cursor.fetchone()
        if data == None:
            cursor.execute("select * from user_register where user_id ='"+str(seller_id)+"' ")
            data = cursor.fetchone()
            if data == None:
                cursor.execute("select * from sellers where seller_id = '"+str(seller_id)+"'")
                data = cursor.fetchone()
                if data == None:
                    cursor.execute ("insert into sellers values('" + seller_id + "','" + name + "','" + address + "','" + phone + "','" + email + "','" + password + "','pending')")
                    return HttpResponse("<script>alert('Registered');window.location='/login';</script>")
        return HttpResponse("<script>alert('id already exists');window.location='/login';</script>")
    return render(request,"Seller/addseller.html")


def viewcategorys(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    pin = cursor.fetchall()
    return render(request,"Seller/viewcategorys.html",{'data':pin})


def additemdetails(request,id):
    sid=request.session['hid']
    print(sid)
    if request.method == "POST":
        category_id = id
        item_name = request.POST['item_name']
        price = request.POST['price']
        image = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(image.name, image)
        file_url = fss.url(file)

        seller_id=str(sid)
        cursor = connection.cursor()
        cursor.execute ("insert into item_details values(null,'" + str(category_id) + "','" + seller_id + "',curdate(),'" + item_name + "','" + price + "','pending','"+str(image)+"')")
        return HttpResponse("<script>alert('Item Added');window.location='/SellersHome';</script>")
    return render(request,"Seller/additemdetails.html")


def viewItemDetials(request):
    sid = request.session['hid']
    cursor = connection.cursor()
    cursor.execute("select i.iditem_details,c.name,i.seller_id,i.posted_date,i.item_name,i.price,i.status,i.image from item_details as i join category as c on i.category_id=c.category_id where i.seller_id='"+str(sid)+"' ")
    pin = cursor.fetchall()
    return render(request,"Seller/viewItemDetials.html",{'data':pin})



def editItemdetials(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from item_details where iditem_details='"+str(id)+"'")
    pin = cursor.fetchall()
    print(pin)
    return render(request,"Seller/editItemdetials.html",{'data':pin})



def UpdateItems(request,id):
    if request.method == "POST":
        item_name = request.POST['item_name']
        price = request.POST['price']
        image = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(image.name, image)
        file_url = fss.url(file)
        cursor = connection.cursor()
        cursor.execute("update item_details set posted_date=curdate(),item_name='" + item_name + "',price='" + price + "',image ='"+str(image)+"' where iditem_details='" + str(id) + "'")
        return HttpResponse("<script>alert('Updated');window.location='/viewItemDetials';</script>")
    return render(request,"Admin/editCategory.html")



def deleteitems(request,id):
    cursor = connection.cursor()
    cursor.execute ("delete from item_details where iditem_details='"+str(id)+"'")
    return HttpResponse( "<script>alert('Deleted Succesfully');window.location='/viewItemDetials';</script>")


def viewuserbookings(request):
    sid = request.session['hid']
    cursor = connection.cursor()
    cursor.execute("select u.iduser_bookings,u.user_id,i.item_name,u.booking_date,u.quantity,u.total_price,u.status,u.seller_id,i.image from user_bookings as u join item_details as i on u.iditem_details=i.iditem_details where u.seller_id='"+str(sid)+"' ")
    pin = cursor.fetchall()
    return render(request,"Seller/viewuserbookings.html",{'data':pin})



def approvebook(request,id):
    cursor = connection.cursor()
    cursor.execute("update user_bookings set status='order shipped' where iduser_bookings='" + str(id) + "'")
    return redirect("/viewuserbookings")






def viewusernotificationseller(request):
    cursor = connection.cursor()
    cursor.execute("select * from notification where status='approved' ")
    pin = cursor.fetchall()
    return render(request,"Seller/viewusernotificationseller.html",{'data':pin})



def sReply(request,id):
    sid = request.session['hid']
    if request.method == "POST":
        reply = request.POST['TxtReply']
        idnotification =id
        seller_id =sid
        cursor = connection.cursor()
        cursor.execute ("insert into notification_reply values(null,'" + str(idnotification) + "','" + seller_id + "','" + reply + "',curdate())")
        return HttpResponse("<script>alert('Replayed');window.location='/viewusernotificationseller';</script>")
    return render(request,"Seller/sReply.html")


def viewreplyednotificationseller(request,id):
    sid = request.session['hid']
    cursor = connection.cursor()
    cursor.execute("select * from notification_reply where seller_id='"+str(sid)+"' and idnotification='"+str(id)+"' ")
    pin = cursor.fetchall()
    return render(request,"Seller/viewreplyednotificationseller.html",{'data':pin})


def deletenoti(request,id):
    cursor = connection.cursor()
    cursor.execute ("delete from notification_reply where idnotification_reply='"+str(id)+"'")
    return HttpResponse( "<script>alert('Deleted Succesfully');window.location='/viewreplyednotificationseller';</script>")



#--------------------------------------------------------------------User-------------------------------------------------------------------------------#


def adduser(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['TxtAddress']
        phone = request.POST['TxtPhone']
        email = request.POST['TxtEmail']
        city = request.POST['city']
        pincode = request.POST['pincode']
        country = request.POST['country']
        state = request.POST['state']
        password = request.POST['password']
        cursor = connection.cursor()
        cursor.execute("select * from login where admin_id ='" + str(user_id) + "' ")
        data = cursor.fetchone()
        if data == None:
            cursor.execute("select * from user_register where user_id ='" + str(user_id) + "' ")
            data = cursor.fetchone()
            if data == None:
                cursor.execute("select * from sellers where seller_id = '" + str(user_id) + "'")
                data = cursor.fetchone()
                if data == None:
                    cursor.execute ("insert into user_register values('" + user_id + "','" + first_name + "','" + last_name + "','" + email + "','" + phone + "','" + address + "','" + city + "','" + pincode + "','" + country + "','" + state + "','" + password + "')")
                    return HttpResponse("<script>alert('Registered');window.location='/login';</script>")
        return HttpResponse("<script>alert('Id already exist');window.location='/login';</script>")
    return render(request,"User/adduser.html")






def viewcategoryuser(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    pin = cursor.fetchall()
    return render(request,"User/viewcategoryuser.html",{'data':pin})


def viewItemsuser(request,id):
    cursor = connection.cursor()
    cursor.execute("SELECT  ids.iditem_details,c.name,ids.seller_id,ids.posted_date,ids.item_name,ids.price,ids.status,ids.image FROM item_details as ids join category as c on ids.category_id=c.category_id where ids.category_id='"+str(id)+"'")
    pin = cursor.fetchall()
    return render(request,"User/viewItemsuser.html",{'data':pin})

def Addcart(request,id,pid,sid):
    return render(request, "User/Addcart.html",{'id':id,'pid':pid,'sid':sid})

def Addcarts(request):
    if request.method == "POST":
        id =request.POST['id']
        sid = request.POST['sid']
        pid = request.POST['pid']
        print(sid)
        uid = request.session['lid']
        quantity = request.POST['quantity']
        n=sid
        iditem_details =id
        user_id =uid
        total_price =int(quantity)*int(n)
        a =(total_price/100)*10
        shopprice =total_price-a
        seller_id =str(pid)
        cursor = connection.cursor()
        cursor.execute ("insert into user_bookings values(null,'" + str(user_id) + "','" + str(iditem_details) + "',curdate(),'" + str(quantity) + "','" + str(total_price) + "','ADDED TO CART','" + seller_id + "','"+str(shopprice)+"','"+str(a)+"')")
        return HttpResponse("<script>alert('ADDED tO CART');window.location='/UserHome';</script>")


def Viewcart(request):
    id=request.session['lid']
    cursor = connection.cursor()
    cursor.execute("SELECT us.iduser_bookings,us.user_id,i.item_name,us.booking_date,us.quantity,us.total_price,us.status,us.seller_id   FROM user_bookings as us join item_details as i on us.iditem_details=i.iditem_details  where us.user_id='"+str(id)+"' and us.status='ADDED TO CART' ")
    data =cursor.fetchone()
    if data == None:
        return HttpResponse("<script>alert('No Carts Added Yet');window.location='/UserHome';</script>")
    cursor.execute("SELECT us.iduser_bookings,us.user_id,i.item_name,us.booking_date,us.quantity,us.total_price,us.status,us.seller_id   FROM user_bookings as us join item_details as i on us.iditem_details=i.iditem_details  where us.user_id='"+str(id)+"' and us.status='ADDED TO CART' ")
    pin = cursor.fetchall()
    return render(request,"User/Viewcart.html",{'data':pin})

def vieworders(request):
    id = request.session['lid']
    cursor = connection.cursor()
    cursor.execute("select u.iduser_bookings,u.user_id,i.item_name,u.booking_date,u.quantity,u.total_price,u.status,u.seller_id,i.image from user_bookings as u join item_details as i on u.iditem_details=i.iditem_details where u.user_id='"+str(id)+"' ")
    pin = cursor.fetchall()
    return render(request,"User/viewuserbookings.html",{'data':pin})


def Bank(request,id):
    sid = request.session['lid']
    if request.method == "POST":
        card_no =request.POST['card_no']
        card_cvv = request.POST['card_cvv']
        card_expiry_date =request.POST['card_expiry_date']
        card_holder_name =request.POST['card_holder_name']
        cursor = connection.cursor()
        cursor.execute ("select * from account_details where card_no='" + card_no + "' and card_cvv='" + card_cvv + "' and card_holder_name='" + card_holder_name + "' and card_expiry_date='" + card_expiry_date + "'  ")
        cursor.execute("update item_details set status='Order placed' where iditem_details='" + str(id) + "'")
        cursor.execute("update user_bookings set status='paid' where user_id='" + str(sid) + "'")
        return HttpResponse("<script>alert('PAIDED');window.location='/UserHome';</script>")
    return render(request,"User/Bank.html")



def Sendnotification(request):
    id = request.session['lid']
    if request.method == "POST":
        user_id = id
        details = request.POST['details']
        title = request.POST['title']
        cursor = connection.cursor()
        cursor.execute ("insert into notification values(null,curdate(),'" + details + "','pending','" + user_id + "','" + title  + "')")
        return HttpResponse("<script>alert('Registered');window.location='/UserHome';</script>")
    return render(request,"User/Sendnotification.html")


def ViewNoti(request):
    id=request.session['lid']
    cursor = connection.cursor()
    cursor.execute("select * from notification where user_id='"+str(id)+"'")
    pin = cursor.fetchall()
    return render(request,"User/ViewNoti.html",{'data':pin})


def ViewNotiReply(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from notification_reply where idnotification='"+str(id)+"'")
    pin = cursor.fetchall()
    if pin==None:
        return HttpResponse("<script>alert('No DATA');window.location='/UserHome';</script>")
    return render(request,"User/ViewNotiReply.html",{'data':pin})
