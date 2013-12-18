from haystack import indexes
from django.utils import timezone
from website.models import Listing

class ListingIndex(indexes.SearchIndex, indexes.Indexable):

    # search results
    # there can BE ONLY ONE document=True per model
    text = indexes.CharField(document=True, use_template=True)
    # the use_template is in the app directory, just a text file
    # with the fields that we want to display when returning results

    # search filtering
    date_created = indexes.DateTimeField(model_attr='date_created')

    def get_model(self):
        return Listing

    def index_queryset(self, using=None):
        """When the entire index for model is updated."""
	return self.get_model().objects.filter(date_created=timezone.now())
