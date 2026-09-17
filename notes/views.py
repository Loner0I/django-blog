from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Note
from .serializers import NoteSerializer


@api_view(["GET", "POST"])
def note_list(request):
    if request.method == "GET":
        notes = Note.objects.filter(user=request.user)

        search = request.query_params.get("search")
        if search:
            notes = notes.filter(Q(title__icontains=search) | Q(content__icontains=search))

        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == "GET":
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        partial = request.method == "PATCH"
        serializer = NoteSerializer(note, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
