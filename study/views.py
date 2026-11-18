from django.conf import settings
from django.db import DatabaseError, transaction
from django.shortcuts import get_object_or_404, redirect, render

from .demo import DEMO_TEXT, DEMO_TITLE
from .forms import SourceForm
from .models import Flashcard, Source
from .services import GenerationError, generate_cards


def home(request):
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            try:
                # Full validation finishes before any database write.
                cards = generate_cards(form.cleaned_data['text'])
            except GenerationError as exc:
                form.add_error(None, str(exc))
            else:
                try:
                    with transaction.atomic():
                        source = Source.objects.create(
                            title=form.cleaned_data['title'],
                            text=form.cleaned_data['text'],
                            generation_mode=settings.TEACHME_MODE,
                        )
                        for position, card in enumerate(cards, 1):
                            Flashcard.objects.create(source=source, position=position, **card)
                except DatabaseError:
                    form.add_error(None, 'Карточкаларды сақтау мүмкін болмады. Қайтадан көріңіз.')
                else:
                    return redirect('source_detail', pk=source.pk)
    else:
        form = SourceForm(initial={'title': DEMO_TITLE, 'text': DEMO_TEXT})
    context = {
        'form': form,
        'mode': settings.TEACHME_MODE,
        'sources': Source.objects.order_by('-created_at')[:20],
    }
    return render(request, 'study/home.html', context)


def source_detail(request, pk):
    source = get_object_or_404(Source, pk=pk)
    cards = source.cards.order_by('position')
    return render(request, 'study/source_detail.html', {'source': source, 'cards': cards})
