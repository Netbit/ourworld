from haystack import indexes
from mapapp.models import Construction


class PlaceIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    unsigned_name = indexes.CharField(model_attr='unsigned_name')
    address = indexes.CharField(model_attr='get_address')
    location = indexes.CharField(model_attr='location')
    
    def get_model(self):
        return Construction
    
    def index_queryset(self):
        return self.get_model().objects.all()