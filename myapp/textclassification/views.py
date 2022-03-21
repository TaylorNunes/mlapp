from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.core.cache import cache
from .forms import text_form
from .classifier import TextClassifier

# Create your views here.

def index(request):
  classifier = cache.get('clf_key')
  if classifier is None:
    classifier = TextClassifier()
    classifier.load_model()
    cache.set('clf_key', classifier, 600)
  if request.method == 'POST':
    form = text_form(request.POST)
    if form.is_valid():
      post_data = form.cleaned_data
      language, accuracy = classifier.classify(post_data['text'])
      statement = "Language is {} with accuracy of {}%".format(language, accuracy)
      return render(request, 'textclassification/index.html', {'form': form, 'classification_statement':statement})
  return render(request, 'textclassification/index.html',{'form': form})
