import datetime
import requests

from django.forms import model_to_dict
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from .models import MenuItem, Category, Cart, Order, OrderItem
from django.core.paginator import Paginator, EmptyPage
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from rest_framework import generics
from .serializers import CategorySerializer,MenuItemSerializer,CartSerializer,OrderSerializer,UserSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group,User

from rest_framework import viewsets,status

# # Create your views here.
# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# @throttle_classes([AnonRateThrottle, UserRateThrottle])
# def menu_items(request):
# 	if request.method == "GET":
# 		items = MenuItem.objects.all()
# 		category_name = request.query_params.get("category")
# 		to_price = request.query_params.get('to_price')
# 		search = request.query_params.get("search")
# 		perpage = request.query_params.get("perpage", default=2)
# 		page = request.query_params.get("page", default=1)
# 		if category_name:
# 			items.filter(category__title=category_name)
# 		if to_price:
# 			items.filter(price=to_price)
# 		if search:
# 			items.filter(title__icontains=search)

# 		paginator = Paginator(items, perpage=perpage)
# 		try:
# 			items = paginator.page(number=page)
# 		except EmptyPage:
# 			items = []
# 		return Response(items.values())
# 	else:
# 		if request.user.groups.filter(name="Manager"):
# 			if request.method == "POST":
# 				item = MenuItem(
# 					title=request.data["title"], 
# 					price=request.data["price"], 
# 					featured=request.data["featured"], 
# 					category=Category.objects.get(slug=request.data["category"]))
# 				item.save()
# 				return Response(model_to_dict(item), 201)
# 		else:
# 			return Response({"unauthorized": "You are not authorized to make this request"}, 403)
		
# @api_view(["GET", "PUT", "PATCH", "DELETE"])
# @permission_classes([IsAuthenticated])
# @throttle_classes([AnonRateThrottle, UserRateThrottle])
# def single_menu_item(request, id):
# 	if request.method == "GET":
# 			if MenuItem.objects.filter(id=id).exists():
# 				item = MenuItem.objects.get(id=id)
# 				return JsonResponse(model_to_dict(item))
# 			else:
# 				return Response({"invalid": "This item does not exist"}, 404)
# 	else:
# 		if request.user.groups.filter(name="Manager").exists():
# 			if request.method == "PUT":
# 				if MenuItem.objects.filter(id=id).exists():
# 					item = MenuItem.objects.get(id=id)

# 					item.title = request.data["title"]
# 					item.price = request.data["price"]
# 					item.featured = request.data["featured"]
# 					item.category = Category.objects.get(slug=request.data["category"])
# 					item.save()

# 					return JsonResponse(model_to_dict(item))
# 				else:
# 					return Response({"invalid": "This item does not exist"}, 404)
# 			elif request.method == "PATCH":
# 				if MenuItem.objects.filter(id=id).exists():
# 					item = MenuItem.objects.get(id=id)
# 					for key in request.data.keys():
# 						match key:
# 							case "title": item.title = request.data[key]
# 							case "price": item.price = request.data[key]
# 							case "featured": item.featured = request.data[key]
# 							case "category": item.category = request.data[key]
# 					item.save()
						
# 					return JsonResponse(model_to_dict(item))
# 				else:
# 					return Response({"invalid": "This item does not exist"}, 404)
# 			elif request.method == "DELETE":
# 				if MenuItem.objects.filter(id=id).exists():
# 					item = MenuItem.objects.get(id=id)
# 					item.delete()

# 					return JsonResponse({"message": "Menu item deleted"})
# 				else:
# 					return Response({"invalid": "This item does not exist"}, 404)
# 		else:
# 			return Response({"unauthorized": "You are not authorized to make this request"}, 403)
		
# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# @throttle_classes([AnonRateThrottle, UserRateThrottle])
# def manager_users(request):
# 	if request.user.groups.filter(name="Manager").exists():
# 		if request.method == "GET":
# 			managers = []
# 			for user in User.objects.all():
# 				if user.groups.filter(name="Manager").exists():
# 					managers.append({
# 						"username": user.username,
# 						"email": user.email
# 					})
# 			return Response(managers)
# 		elif request.method == "POST":
# 			group = Group.objects.get(name="Manager")
# 			user = User.objects.get(username=request.data["username"])
# 			group.user_set.add(user)
# 			return Response({"succesful": "User successfully added to managers"})
# 	else:
# 		return Response({"unauthorized": "You are not authorized to make this request"}, 403)
	
# @api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
# @throttle_classes([AnonRateThrottle, UserRateThrottle])
# def remove_single_manager(request, userId):
# 	if request.user.groups.filter(name="Manager").exists():
# 		if request.method == "DELETE":
# 			group = Group.objects.get(name="Manager")
# 			user = User.objects.get(id=userId)
# 			group.user_set.remove(user)
# 			return Response({"succesful": "User successfully removed from managers"})
# 	else:
# 		return Response({"unauthorized": "You are not authorized to make this request"}, 403)
	
# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# @throttle_classes([AnonRateThrottle, UserRateThrottle])
# def delivery_crew_users(request):
# 	if request.user.groups.filter(name="Manager").exists():
# 		if request.method == "GET":
# 			deliveryCrew = []
# 			for user in User.objects.all():
# 				if user.groups.filter(name="Delivery Crew").exists():
# 					deliveryCrew.append({
# 						"username": user.username,
# 						"email": user.email
# 					})
# 			return Response(deliveryCrew)
# 		elif request.method == "POST":
# 			group = Group.objects.get(name="Delivery Crew")
# 			user = User.objects.get(username=request.data["username"])
# 			group.user_set.add(user)
# 			return Response({"succesful": "User successfully added to delivery crew"})
# 	else:
# 		return Response({"unauthorized": "You are not authorized to make this request"}, 403)
	
# @api_view(["DELETE"])
# @permission_classes([IsAuthenticated])
# @throttle_classes([AnonRateThrottle, UserRateThrottle])
# def remove_single_delivery_crew(request, userId):
# 	if request.user.groups.filter(name="Manager").exists():
# 		if request.method == "DELETE":
# 			group = Group.objects.get(name="Delivery Crew")
# 			user = User.objects.get(id=userId)
# 			group.user_set.remove(user)
# 			return Response({"succesful": "User successfully removed from delivery crew"})
# 	else:
# 		return Response({"unauthorized": "You are not authorized to make this request"}, 403)
	
# @api_view(["GET", "POST", "DELETE"])
# @throttle_classes([AnonRateThrottle, UserRateThrottle])
# @permission_classes([IsAuthenticated])
# def cart(request):
# 	if not request.user.groups.exists():
# 		if request.method == "GET":
# 			cart_items = []
# 			for cart in Cart.objects.all():
# 				if cart.user == request.user:
# 					cart_items.append(model_to_dict(cart))
# 			return Response(cart_items)
# 		elif request.method == "POST":
# 			menu_item = MenuItem.objects.get(title=request.data["title"])
# 			cart = Cart(
# 				user=request.user,
# 				menuitem=menu_item, 
# 				quantity=request.data["quantity"],
# 				unit_price=menu_item.price,
# 				price=int(menu_item.price)*int(request.data["quantity"]))
# 			cart.save()
# 			return Response({"message": "Added item to cart"}, 201)
# 		elif request.method == "DELETE":
# 			for cart in Cart.objects.all():
# 				if cart.user == request.user:
# 					cart.delete()
# 			return Response({"message": "Cart succesfully emptied"})
# 	else:
# 		return Response({"unauthorized": "You are not authorized to make this request"}, 403)
	
# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# @throttle_classes([AnonRateThrottle, UserRateThrottle])
# def orders(request):
# 	if request.method == "GET":
# 		if not request.user.groups.exists():
# 			orders = []
# 			for order in Order.objects.all():
# 				if order.user == request.user:
# 					order_dict = {}
# 					order_dict["order id"] = order.id
# 					order_dict["order items"] = []
# 					for order_item in OrderItem.objects.all():
# 						if order_item.order == order:
# 							order_dict["order items"].append(model_to_dict(order_item))		
# 					orders.append(order_dict)
# 			return Response(orders)
# 		elif request.user.groups.filter(name="Manager").exists():
# 			orders = []
# 			for order in Order.objects.all():
# 				order_dict = model_to_dict(order)
# 				order_dict["order items"] = []
# 				for order_item in OrderItem.objects.all():
# 					if order_item.order == order:
# 						order_dict["order items"].append(model_to_dict(order_item))		
# 				orders.append(order_dict)
# 			return Response(orders)
# 		elif request.user.groups.filter(name="Delivery Crew").exists():
# 			orders = []
# 			for order in Order.objects.all():
# 				if order.delivery_crew == request.user:
# 					order_dict = {}
# 					order_dict["order id"] = order.id
# 					order_dict["order items"] = []
# 					for order_item in OrderItem.objects.all():
# 						if order_item.order == order:
# 							order_dict["order items"].append(model_to_dict(order_item))		
# 					orders.append(order_dict)
# 			return Response(orders)
# 	elif request.method == "POST":
# 		if not request.user.groups.exists():
# 			order = Order(user=request.user, delivery_crew=None, total=0, date=datetime.datetime.now())
# 			order.save()
# 			r = requests.get("http://127.0.0.1:8000/api/cart/menu-items", 
# 					headers={"Authorization": f"Token {request.auth.key}"})
# 			data = r.json()
# 			total = 0
# 			for item in data:
# 				order_item = OrderItem(order=order, 
# 						   menuitem=MenuItem.objects.get(id=item["menuitem"]), 
# 						   quantity=item["quantity"], unit_price=item["unit_price"], 
# 						   price=item["price"])
# 				total += item["price"]
# 				order_item.save()
# 			order.total = total
# 			order.save()
# 			requests.delete("http://127.0.0.1:8000/api/cart/menu-items", 
# 					headers={"Authorization": f"Token {request.auth.key}"})
# 			return Response({"message": "Order succesfully placed"}, 201)

# @api_view(["GET", "PUT", "PATCH", "DELETE"])
# @permission_classes([IsAuthenticated])
# @throttle_classes([AnonRateThrottle, UserRateThrottle])
# def one_order(request, orderId):
# 	if request.method == "GET":
# 		if not request.user.groups.exists():
# 			order = Order.objects.get(id=orderId)
# 			if order.user == request.user:
# 				orders = []
# 				order_dict = {}
# 				order_dict["order id"] = order.id
# 				order_dict["order items"] = []
# 				for order_item in OrderItem.objects.all():
# 					if order_item.order == order:
# 						order_dict["order items"].append(model_to_dict(order_item))		
# 				orders.append(order_dict)
# 				return Response(orders)
# 			else:
# 				return Response({"message": "This order does not belong to you"}, 403)
# 		else:
# 			return Response({"unauthorized": "You are not authorized to make this request"})
# 	elif request.method == "PUT":
# 		if request.user.groups.filter(name="Manager").exists():
# 			order = Order.objects.get(id=orderId)
# 			order.date = request.data["date"]
# 			order.delivery_crew = User.objects.get(id=request.data["delivery_crew_id"])
# 			order.status = request.data["status"]
# 			order.total = request.data["total"]
# 			order.save()
			
# 			return Response({"message": "Order successfully changed."})
# 		else:
# 			return Response({"unauthorized": "You are not authorized to make this request"})
# 	elif request.method == "PATCH":
# 		if request.user.groups.filter(name="Manager").exists():
# 			order = Order.objects.get(id=orderId)
# 			for key in request.data.keys():
# 				match key:
# 					case "date": order.date = request.data[key]
# 					case "delivery_crew_id": order.delivery_crew = User.objects.get(id=request.data[key])
# 					case "status": order.status = request.data[key]
# 					case "total": order.total = request.data[key]
# 			order.save()

# 			return Response({"message": "Order successfully changed"})
# 		elif request.user.groups.filter(name="Delivery Crew").exists():
# 			order = Order.objects.get(id=orderId)
# 			if request.data["status"]:
# 				order.status = request.data["status"]
# 			order.save()
# 			return Response({"message": "Order successfully changed"})
# 		else:
# 			return Response({"unauthorized": "You are not authorized to make this request"})
# 	elif request.method == "DELETE":
# 		if request.user.groups.filter(name="Manager").exists():
# 			order = Order.objects.get(id=orderId)
# 			order.delete()

# 			return Response({"message": "Order successfully deleted"})
# 		else:
# 			return Response({"unauthorized": "You are not authorized to make this request"})

			
   
#    By using class based views


class CategoriesView(generics.ListCreateAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    
    def get_permissions(self):
        permission_classes=[]
        if self.request.method != 'GET':
            permission_classes= [IsAuthenticated]
        return [permission() for permission in permission_classes]

class MenuItemView(generics.ListCreateAPIView):
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer
    
    search_fields=["category__title"]
    ordering_fields=['price','inventory']        
    
    def get_permissions(self):
        permission_classes =[]
        if self.request.method !='GET':
            permission_classes=[IsAuthenticated]
        return [permission() for permission in permission_classes]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer
    
    def get_permissions(self):
        permission_classes=[]
        if self.request.method != 'GET':
            permission_classes=[IsAuthenticated]
        return [permission() for permission in permission_classes]
    
class CartView(generics.ListCreateAPIView):
    queryset=Cart.objects.all()
    serializer_class=CartSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)
    
    def delete(self,request,*args,**kwargs):
        cart_item=Cart.objects.filter(user=self.request.user)
        cart_item.delete()   
        return Response("ok",status=status.HTTP_204_NO_CONTENT)     

class OrderView(generics.ListCreateAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.groups.count()==0:
            return Order.objects.all().filter(user=self.request.user)
        elif self.request.user.groups.filter(name="Delivery_crew").exists():
            return Order.objects.all().filter(delivery_crew=self.request.user)
        else:
            return Order.objects.all()
    def create(self, request, *args, **kwargs):
        menuitem_count=Cart.objects.all().filter(user=self.request.user).count()
        if menuitem_count == 0:
            return Response({"message":"No item in cart"})  
        data=request.data.copy()
        total=self.get_total_price(self.request.user)
        data['total']=total
        data['user']=self.request.user.id
        order_serializer=OrderSerializer(data=data)
        if (order_serializer.is_valid()):
            order=order_serializer.save()
            
            items= Cart.objects.all().filter(user=self.request.user).all()
            
            for item in items.values():
                orderitem=OrderItem(
					order=order,
					menuitem_id=item['menuitem_id'],
					price=item['price'],
					quantity=item['quantity']
				)
                orderitem.save()
            # DELETE CART ITEMS
            Cart.objects.all().filter(user=self.request.user).delete()  
            result=order_serializer.data.copy()     
            result['total']=total
            return Response(order_serializer.data)
    
    def get_total_price(self,user):
        total=0
        items=Cart.objects.all().filter(user=user).all()
        for item in items.values():
            total += item['price']
        return total
    

class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        if self.request.user.groups.count()==0:              #Normal user , not belonging to any group = Customer
           return Response('Not OK')
        else:     # Every one else - Super Admin, Manager and Delivery crew   
             return super().update(request,*args,**kwargs)

class GroupViewSet(viewsets.ViewSet):
    permission_classes=[IsAdminUser]
    def list(self,request):
        users=User.objects.all().filter(groups__name='Manager')
        items=UserSerializer(users,many=True)
        return Response(items.data)
    
    def create(self,request):
        user=get_object_or_404(User,username=request.data['username'])
        managers=Group.objects.filter(name="Manager")
        managers.user_set.add(user)
        return Response({"message":"User added to the manager group"},200)
    
    def destroy(self,request):
        user=get_object_or_404(User,username=request.data['username'])
        managers=Group.objects.filter(name="Manager")
        managers.user_set.remove(user)
        return Response({"message":"User removed from the manager group"},204)
    


class DeliveryCrewViewSet(viewsets.ViewSet):
    permission_classes=[IsAuthenticated]
    def list(self,request):
        users=User.objects.all().filter(groups__name="Delivery_crew")
        items=UserSerializer(users,many=True)
        return Response(items.data)
    
    def create(self,request):
        # Only for super admin and managers
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name="Manager").exists() == False:
                return Response({"message":"Forbidden"},status.HTTP_403_FORBIDDEN)
        
        user=get_object_or_404(User,username=request.data['username'])
        dc=Group.objects.filter(name="Delivery_crew")
        dc.user_set.add(user)
        return Response({"message":"User added to the delivery crew group"},200)
    
    def destroy(self,request):
            #Only for super admin and managers
        
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name ="Manager").exists():
                return Response({"message":"Forbidden"},status.HTTP_403_FORBIDDEN)
        
        user=get_object_or_404(User,username=request.data['username'])
        dc=Group.objects.filter(name="Delivery_crew")
        dc.user_set.remove(user)
        return Response({"message":"user removerd from the delivery crew group"},status.HTTP_204_NO_CONTENT)          
    