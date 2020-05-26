from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializers import SnippetSerializer


@csrf_exempt
def snippet_list(request):
    """
    Lists all existing snippets or creates a new one
    """
    if request.method == "GET":
        snippets = Snippet.objects.all()
        # INPUT: query set instead of single instance --> gives list of dicts
        serializer = SnippetSerializer(snippets, many=True)
        # first parameter should be dictionary; setting safe=False allows any json serializable object
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        # JSONParser parses JSON request content
        data = JSONParser().parse(request)
        # INPUT: json data (?)
        serializer = SnippetSerializer(data=data)

        if serializer.is_valid():
            # returns snippet object by create() method
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete code snippet
    """
    # find the object of interest with pk first
    try:
        # model.pk contains primary key value (whether it's the default id or provided)
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    # RETRIEVE case
    if request.method == "GET":
        # INPUT: snippet instance
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    # UPDATE case
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        # INPUT: snippet instance + data
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            # calls update() method in serializer with given instance & data
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        snippet.delete()
        return HttpResponse(status=204)
