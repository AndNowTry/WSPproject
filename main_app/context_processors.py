from main_app.models import MainCategory, SecondaryCategory, TripleCategory


def catalog_processor(request):
    """
        Данные для каталога в базовом шаблоне
    """
    main_categories = MainCategory.objects.all()
    secondary_categories = SecondaryCategory.objects.all()
    triple_categories = TripleCategory.objects.all()

    return {
        "main_categories": main_categories,
        "secondary_categories": secondary_categories,
        "triple_categories": triple_categories,
    }

