from oi.projects.models import Project, Spec, OINeedsPrjPerms, Release
from rest_framework import viewsets, response, status
from serializers import LDPSerializer

class ProjectSerializer(LDPSerializer):
    class Meta:
        model = Project
        fields = ('@id', 'title', 'author', 'state', 'target', 'ldp:contains', 'descendants', 'spec_set', 'message_set', 'release_set')

class LDPView(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = ProjectSerializer
    def create_with_parent(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            serializer.object.parent = self.get_object()
            serializer.object.save()
            headers = self.get_success_headers(serializer.data)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self, *args, **kwargs):
        if self.model:
            return self.model.objects.all()
        else:
            return super(LDPView, self).get_queryset(*args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        response = super(LDPView, self).dispatch(request, *args, **kwargs)
        response["Content-Type"] = "application/ld+json"
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST,PUT"
        response["Access-Control-Allow-Headers"] = "Content-Type, if-match"
        response["Accept-Post"] = "application/ld+json"
        return response
