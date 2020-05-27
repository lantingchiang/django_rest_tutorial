from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Snippet
from .serializers import SnippetSerializer


# @csrf_exempt
@api_view(["GET", "POST"])
# format: to add format suffix to url of this endpoint
def snippet_list(request, format=None):
    """
    Lists all existing snippets or creates a new one
    """
    if request.method == "GET":
        snippets = Snippet.objects.all()
        # INPUT: query set instead of single instance --> gives list of dicts
        serializer = SnippetSerializer(snippets, many=True)
        # first parameter should be dictionary; setting safe=False allows any json serializable object
        # return JsonResponse(serializer.data, safe=False)
        return Response(serializer.data)

    elif request.method == "POST":
        """
        # JSONParser parses JSON request content
        data = JSONParser().parse(request)
        # INPUT: json data (?)
        serializer = SnippetSerializer(data=data)
        """
        serializer = SnippetSerializer(data=request.data)

        if serializer.is_valid():
            # returns snippet object by create() method
            serializer.save()
            # return JsonResponse(serializer.data, status=201)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return JsonResponse(serializer.errors, status=400)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
@api_view(["GET", "PUT", "DELETE"])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete code snippet
    """
    # find the object of interest with pk first
    try:
        # model.pk contains primary key value (whether it's the default id or provided)
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        # return HttpResponse(status=404)
        return Response(status=status.HTTP_404_NOT_FOUND)

    # RETRIEVE case
    if request.method == "GET":
        # INPUT: snippet instance
        serializer = SnippetSerializer(snippet, data=request.data)
        # handles case where request data is flawed
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
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
        # return JsonResponse(serializer.errors, status=400)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

    elif request.method == "DELETE":
        snippet.delete()
        # return HttpResponse(status=204)
        return Response(status=status.HTTP_204_NO_CONTENT)
