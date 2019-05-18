from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from products.models import Product
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
from django.contrib import messages
# Create your views here.
def index(request):
	product_list = Product.objects.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(product_list, 3)
	try:
		products = paginator.page(page)
	except PageNotAnInteger:
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)
	return render(request,'backend/index.html',{'products':products})


def handle_uploaded_file(f):
	with open('products/static/images/'+f.name,'wb+')as destination:
		for chunk in f.chunks():
			destination.write(chunk)

def create(request):
	if request.method =="POST":
		handle_uploaded_file(request.FILES['photo'])
		try:
			product=Product(name=request.POST['name'], price=request.POST['price'], qty=request.POST['qty'], desc=request.POST['desc'],photo=request.FILES['photo'])
			product.save()
			#return HttpResponse('success')
			return HttpResponseRedirect('/backend/')
		except:
			return HttpResponse('fail')
	else:
		#return HttpResponse('success2')
		return render(request,'backend/create.html')


def edit(request, id):
	product = Product.objects.get(id=id)
	return render(request,'backend/edit.html',{'product':product})

def  update(request, id):
	if request.method =="POST":
		product = Product.objects.get(id=id)
		handle_uploaded_file(request.FILES['photo'])
		product.name=request.POST['name']
		product.price=request.POST['price']
		product.qty=request.POST['qty']
		product.desc=request.POST['desc']
		product.photo=request.FILES['photo']
		#product.photo=handle_uploaded_file(request.FILES['photo'])
		product.save()
		return HttpResponseRedirect("/backend/")
	else:
		return render(request,'backend/edit.html',{'product',product})

def  pd_update(request,id):
	product = Product.objects.get(id=id)
	form = ProductForm(request.POST, instance = product)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/backend")
	return render(request,'backend/edit_pd.html',{'product',product})

def delete(request, id):
	product = Product.objects.get(id=id)
	product.delete()
	messages.success(request, product.name + " is successfully deleted.")
	return HttpResponseRedirect("/backend/")


def show_products(request):
	count=0
	for rec in request.session.items():
		count+=1
	products=Product.objects.all()
	context={'products':products,'counts':count}
	return render(request,'frontend/index.html',context)

class ProductItems(object):
	def __init__(self,id,name,price,qty,desc,photo):
		self.id=id
		self.name=name
		self.price=price
		self.qty=qty
		self.desc=desc
		self.photo=photo

	def serialize(self):
		return self.__dict__

def add(request,id):
	count=0;
	product=Product.objects.get(id=id)
	products=[]
	products.append(ProductItems(str(product.id),product.name,str(product.price),str(product.qty),product.desc,str(product.photo)).serialize())
	request.session[id]=products
	for rec in request.session.items():
		count+=1

	products=Product.objects.all()
	return render(request,'frontend/index.html',{'products':products,'counts':count})

def checkout(request):
	count2=0
	for rec in request.session.items():
		count2+=1
	total=0
	sub_total=0

	for rec in request.session.items():
		for i in range(len(rec)):
			if i==0:continue
			subtotal=float(rec[i][0]['price'])* int(rec[i][0]['qty'])
			total=total+subtotal
			#print(total)
	products=request.session.items()
	context={'products':products, 'counts':count2,'total':total}
	return render(request,'frontend/checkout.html',context)	


def remove(request,id):
	found=False
	count2=0
	total=0
	sub_total=0
	products=[]

	print("request id ="+str(id))
	
	count=0
	print("-----------------------\n")
	#print(request.session.items())
	products=list(request.session.items())
	print("before")
	print(products)

	for product in list(products):
		rec=list(product)
		print("id = "+str(rec[0]))
		print(rec[1])

		found=False
		if id==int(rec[0]):
			found_index=count
			found=True
			break
		count+=1
	if found==True:
		#print("found")
		products.remove(products[found_index])

		print("after\n---------\n")
		#print(products)

		request.session.flush()
		for rec in products:
		 	request.session[rec[0]]=rec[1]

		#print(request.session.items())
		count=0
		products=request.session.items();
		for rec in request.session.items():
			count+=1

		total=0
		sub_total=0	
		for rec in request.session.items():
			for i in range(len(rec)):
				if i==0:continue
				subtotal=float(rec[i][0]['price'])* int(rec[i][0]['qty'])
				total=total+subtotal


		return render(request,"frontend/checkout.html",{'products':products,'count':count,'total':total})
	else:
		print("not found...")
		return HttpResponse("fail")
		
def  removeall(request):
	request.session.flush()
	products=Product.objects.all()
	return  render(request,'frontend/index.html',{'products':products,'counts':0})


def remove_me(request,id):
	found=False
	count2=0
	total = 0
	sub_total=0
	for rec in request.session.items():
		#count2=(len(rec)+1)
		for i in range(len(rec)):
			if i>=0:
				del request.session[str(id)]
				#count2 -= 1
				found=True
				break
		if found==True:
			break
	if found == True:
		#print(request.session.items())
		for rec in request.session.items():
			count2 += 1
			for i in range(len(rec)):
				if i == 0: continue
				subtotal = float(rec[i][0]['price']) * int(rec[i][0]['qty'])
				total = total + subtotal
		products = request.session.items()
		context = {'products': products, 'counts': count2, 'total': total}
		return render(request, 'frontend/checkout.html', context)
	else:
		return HttpResponse("fail")



def normalize_query(query_string,
    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
    normspace=re.compile(r'\s{2,}').sub):

    '''
    Splits the query string in invidual keywords, getting rid of unecessary spaces and grouping quoted words together.
    Example:
    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''

    return [normspace('',(t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):

    '''
    Returns a query, that is a combination of Q objects.
    That combination aims to search keywords within a model by testing the given search fields.
    '''

    query = None ## Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None ## Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def search(request):
	query_string = ''
	products = None
	count=0
	if request.method == 'GET':
		if('search' in request.GET) and request.GET['search'].strip():
			query_string = request.GET['search']
			entry_query = get_query(query_string, ['name', 'price', 'desc'])
			products = Product.objects.filter(entry_query).order_by('name')
		else:
			products=Product.objects.all()
		
	for rec in request.session.items():
		count+=1
	context={'products':products,'counts':count, 'search':query_string}
	return render(request,'frontend/index.html',context)