
from django.contrib import admin
from django.urls import path, include
from aquaapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('login1', views.login1, name='login1'),
    path('logout', views.logout, name='logout'),
    path('ulogout', views.ulogout, name='ulogout'),
    path('slogout', views.slogout, name='slogout'),
    path('AdminHomePage', views.AdminHomePage, name='AdminHomePage'),
    path('viewAllNewSellerRequest', views.viewAllNewSellerRequest, name='viewAllNewSellerRequest'),
    path('approvesell/<str:sid>', views.approvesell, name='approvesell'),
    path('Rejectsell/<str:sid>', views.Rejectsell, name='Rejectsell'),
    path('viewsellerAdmin', views.viewsellerAdmin, name='viewsellerAdmin'),
    path('addCategory', views.addCategory, name='addCategory'),
    path('viewCategory', views.viewCategory, name='viewCategory'),
    path('deleteCategory/<int:cid>', views.deleteCategory, name='deleteCategory'),
    path('viewsellerBookingsAdmin', views.viewsellerBookingsAdmin, name='viewsellerBookingsAdmin'),
    path('viewsellerAdmin', views.viewsellerAdmin, name='viewsellerAdmin'),
    path('viewcustomer', views.viewcustomer, name='viewcustomer'),
    path('ViewNotificationAdmin', views.ViewNotificationAdmin, name='ViewNotificationAdmin'),
    path('approvenoti/<int:id>', views.approvenoti, name='approvenoti'),
    path('ViewNotificationAdminApproved', views.ViewNotificationAdminApproved, name='ViewNotificationAdminApproved'),
    path('editCategory/<int:id>', views.editCategory, name='editCategory'),
    path('UpdateCategory/<int:id>', views.UpdateCategory, name='UpdateCategory'),


#---------------------------------------------------Seller----------------------------------------------------------------------#
    path('SellersHome', views.SellersHome, name='SellersHome'),
    path('addseller', views.addseller, name='addseller'),
    path('viewcategorys', views.viewcategorys, name='viewcategorys'),
    path('additemdetails/<int:id>', views.additemdetails, name='additemdetails'),
    path('viewItemDetials', views.viewItemDetials, name='viewItemDetials'),
    path('deleteitems/<int:id>', views.deleteitems, name='deleteitems'),
    path('viewuserbookings', views.viewuserbookings, name='viewuserbookings'),
    path('Vieworders', views.vieworders, name='vieworders'),
    path('approvebook/<int:id>', views.approvebook, name='approvebook'),
    path('viewusernotificationseller', views.viewusernotificationseller, name='viewusernotificationseller'),
    path('sReply/<int:id>', views.sReply, name='sReply'),
    path('editItemdetials/<int:id>', views.editItemdetials, name='editItemdetials'),
    path('UpdateItems/<int:id>', views.UpdateItems, name='UpdateItems'),
    path('deletenoti/<int:id>', views.deletenoti, name='deletenoti'),
    path('viewreplyednotificationseller/<int:id>', views.viewreplyednotificationseller, name='viewreplyednotificationseller'),



#-----------------------------------------------User--------------------------------------------------------------------------------#
    path('UserHome', views.UserHome, name='UserHome'),
    path('adduser', views.adduser, name='adduser'),
    path('viewcategoryuser', views.viewcategoryuser, name='viewcategoryuser'),
    path('viewItemsuser/<int:id>', views.viewItemsuser, name='viewItemsuser'),
    path('Addcart/<int:id>/<str:pid>/<str:sid>', views.Addcart, name='Addcart'),
    path('Addcarts', views.Addcarts, name='Addcarts'),
    path('Viewcart', views.Viewcart, name='Viewcart'),
    path('Bank/<int:id>', views.Bank, name='Bank'),
    path('Sendnotification', views.Sendnotification, name='Sendnotification'),
    path('ViewNoti', views.ViewNoti, name='ViewNoti'),
    path('ViewNotiReply/<int:id>', views.ViewNotiReply, name='ViewNotiReply'),



]