from django.shortcuts import render
from django.http import HttpResponse
from app_restaurantes.models import Restaurante, Tapa
from django.contrib.auth.decorators import login_required
from django import forms
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app_restaurantes.models import Restaurante
from app_restaurantes.serializers import RestauranteSerializer



class TapasForm(forms.Form):
    nombre = forms.CharField(max_length=128, label='Aniadir tapa')
    foto = forms.CharField(max_length=128, label='Aniadir imagen')
    precio = forms.IntegerField(label='Precio de la tapa')
    restaurante = forms.CharField(label='Resturante que pertenece')

def add_tapa(request):
    context={}
    form=TapasForm()


    context={

        'form': form
    }
    if request.method == 'POST':
        form = TapasForm(request.POST)
        context['form']=form

    return render(request,'app_restaurantes/add_tapa.html',context)




def hola_funcion (request):
    return HttpResponse("Hola mundo")


def index (request):
	lista = Restaurante.objects.all()
	lista_tapas = Tapa.objects.all()
	context= {'mensaje': 'restaurantes!', 'restaurante': lista[:4], 'tapas': lista_tapas} #paso los 4 primeros solo
	return render (request, 'base.html', context)


@login_required
def like_category(request):
	cat_id = None
	if request.method == 'GET':
        	cat_id = request.GET.get('me_gusta','')	
	likes = 0
	if cat_id:
		cat = Restaurante.objects.get(id=cat_id)
	if cat:
		likes = cat.me_gusta + 1
		cat.me_gusta =  likes
		cat.save()



	return HttpResponse(likes)


@login_required
def dislike_category(request):
	cat_id = None
	if request.method == 'GET':
        	cat_id = request.GET.get('no_me_gusta','')
	dislikes = 0
	if cat_id:
		cat = Restaurante.objects.get(id=cat_id)
	if cat:
		dislikes = cat.no_me_gusta + 1
		cat.no_me_gusta =  dislikes
		cat.save()



	return HttpResponse(dislikes)


@api_view(['GET','POST'])
def rest_restaurante(request):
	if request.method == 'GET':
		restaurante = Restaurante.objects.all()
		serializer = RestauranteSerializer(restaurante, many=True)
		return Response(serializer.data)

	if request.method == 'POST':
		serializer = RestauranteSerializer(data=request.data)
       

		if serializer.is_valid():
			serializer.save()
  			print('vale')
			return JsonResponse(serializer.data, status=201)
   
	return JsonResponse(serializer.errors, status=400)


@api_view(['GET','PUT','DELETE'])
def rest_element_restaurante(request, nombre):
	try:
		restaurante = Restaurante.objects.get(nombre=nombre)
	except Restaurante.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = RestauranteSerializer(restaurante)
		return Response(serializer.data)

	if request.method == 'DELETE':
		serializer = RestauranteSerializer(restaurante)
		return Response(status=status.HTTP_204_NO_CONTENT)

	if request.method == 'PUT':
		nombreR = Restaurante.objects.get(nombre=nombre)
		#direccionR = Restaurante.objects.get(direccion=direccion)
		#fotoR = Restaurante.objects.get(foto=foto)
		#me_gustaR = Restaurante.objects.get(me_gusta=me_gusta)
		nombreR.save()
		#direccionR.save()
		#fotoR.save()
		#me_gustaR
		return Response(status=status.HTTP_201_OK)


