import django_filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets, status,filters
from rest_framework.response import Response
from .models import File
from .serializers import FileSerializer

# Create your views here.

class FileRecordFilter(FilterSet):
    min_size = django_filters.NumberFilter(field_name="size", lookup_expr='gte')
    max_size = django_filters.NumberFilter(field_name="size", lookup_expr='lte')
    uploaded_after = django_filters.DateFilter(field_name="uploaded_at", lookup_expr='gte')
    uploaded_before = django_filters.DateFilter(field_name="uploaded_at", lookup_expr='lte')

    class Meta:
        model = File
        fields = ['file_type', 'min_size', 'max_size', 'uploaded_after', 'uploaded_before']


class FileViewSet(viewsets.ModelViewSet):
    queryset = File .objects.all().order_by('-uploaded_at')
    serializer_class = FileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = FileRecordFilter

    # filterset_fields = ['file_type', 'uploaded_at']
    search_fields = ['original_filename', 'file_type']
    ordering_fields = ['uploaded_at', 'size']
    ordering = ['-uploaded_at','original_filename']

    def create(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate hash
        import hashlib
        sha256 = hashlib.sha256()
        for chunk in file_obj.chunks():
            sha256.update(chunk)
        file_hash = sha256.hexdigest()

        # Check for duplicate
        existing = File.objects.filter(file_hash=file_hash).first()
        if existing:
            serializer = self.get_serializer(existing)
            return Response(serializer.data, status=200)

        # Save new file
        data = {
            'file': file_obj,
            'file_hash': file_hash,
            'original_filename': file_obj.name,
            'file_type': file_obj.content_type,
            'size': file_obj.size
        }
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
