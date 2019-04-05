from django.views.generic import *
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.template import Library
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
import sys
sys.path.append("../visualization_core/")
from Visualization import *
from FilterVis import *
from FilterMax import *
from HeatMap import *
from Datas import *
from Archi import *
'''
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
'''
import json, os
import datetime
#from parsing import parse

my_dict = {"a" : 6}

#CLPATH = "/mysite/static/mysite/Images"
CL_PATH = "./mysite/static/mysite/Images/"
GRAPHS_PATH = "./graphs"
register = Library()

datas = None
vis = None

@register.filter(is_safe=True)
def parse(tab):
  n = len(tab)
  res = {}
  for i in range(0,n):
    res[i] = tab[i]
  print (n, res)
  return json.dumps(res,ensure_ascii=False)


def view(request):
    js_data = simplejson.dumps(my_dict)

    render_template_to_response("my_template.html", {"my_data": js_data})


def index(request):
  return render(request, "interface.html")

def search_graph(request):
    g = os.listdir(GRAPHS_PATH) + Datas._DEFAULT_GRAPHS
    print('liste des reseaux : ' + parse(g))
    return HttpResponse(parse(g))

@csrf_exempt
def reset_nn(request):
  datas.reset()
  return HttpResponse(json.dumps({}, ensure_ascii=False))

@csrf_exempt
def get_model(request):
    global datas
    network = request.POST['net']
    datas = Datas(network)
    archi = Archi(datas)
    architecture = archi.run()
    res = {'net' : network, 'architecture' : architecture}
    #load_model(request.POST.__getitem__('msg'))
    print('reseau choisi : ' + request.POST.__getitem__('net'))
    return HttpResponse(json.dumps(res, ensure_ascii=False))

@csrf_exempt
def get_img(request):
    print('classe selectionnee : ' + request.POST.__getitem__('cl'))
    cl = os.listdir(CL_PATH+request.POST.__getitem__('cl'))
    datas.set_class(request.POST["cl"])
    file_location = request.POST.__getitem__('cl') + '/'
    for i in range(0, len(cl)):
      cl[i] = file_location + cl[i]
    print('liste des images : ' + parse(cl))
    return HttpResponse(parse(cl))

@csrf_exempt
def get_cl(request):
    cl = os.listdir(CL_PATH)
    print(cl)
    print('liste des classes : ' + parse(cl))
    return HttpResponse(parse(cl))

@csrf_exempt
def filter_max(request):
  layer_id = int(request.POST["layer"])
  res = {}
  # Filters
  visu = FilterMax(datas)
  res["filters"] = visu.run()
  # HeatMap
  visu = HeatMap(datas)
  res["heatMap"] = visu.run()
  return HttpResponse(json.dumps(res,ensure_ascii=False))

@csrf_exempt
def get_filters(request):
  layer_id = int(request.POST["layer"])
  datas.set_layer(layer_id)
  res = {}
  # Filters
  visu = FilterVis(datas)
  res["filters"] = visu.run()
  # HeatMap
  visu = HeatMap(datas)
  res["heatMap"] = visu.run()
  return HttpResponse(json.dumps(res,ensure_ascii=False))

# @csrf_exempt
# def img_selected(request):
#     img_selected = request.POST.__getitem__('img')

#     vis1.load_image(img_selected)
#     print(vis1.img)


#     print('image choisie : ' + img_selected)

#     file_location = './Images/' + request.POST.__getitem__('cl') + '/' + request.POST.__getitem__('img')

#     try:
#         with open(file_location, 'r') as f:
#            file_data = f.read()

#         # sending response
#         response = HttpResponse(file_data, content_type='image/jpeg')
#         char = 'attachment; filename=' + img_selected
#         response['Content-Disposition'] = char

#     except IOError:
#         # handle file not exist case here
#         response = HttpResponseNotFound('<h1>File not exist</h1>')

#     return response

@csrf_exempt
def img_selected(request):
    img_selected = request.POST.__getitem__('img')

    datas.set_img(img_selected)

    print('image choisie : ' + img_selected)

    #file_location = request.POST.__getitem__('cl') + '/' + request.POST.__getitem__('img')
    file_location = '/' + request.POST.__getitem__('img')
    res = {'img': file_location}
    return HttpResponse(json.dumps(res, ensure_ascii=False))



def test_get(request):
    print("oui")
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    #return json.dumps({'responseText': "coucou"})
    return HttpResponse("0")

@csrf_exempt
def testpost(request):
    print("-------------------------")
    print(request.POST.__getitem__('msg'))
    print("-------------------------")
    return HttpResponse(request.POST.__getitem__('msg'))




def js(obj):
    return mark_safe(json.dumps(obj))

'''def test_i18n(request):
    nb_chats = 2
    couleur = "blanc"
    chaine = _("J'ai un %(animal)s %(col)s.") % {'animal': 'chat', 'col': couleur}
    infos = ungettext(
        "… et selon mes informations, vous avez %(nb)s chat %(col)s !",
        "… et selon mes informations, vous avez %(nb)s chats %(col)ss !",
        nb_chats) % {'nb': nb_chats, 'col': couleur}

    return render(request, 'test_i18n.html', locals())
    '''
