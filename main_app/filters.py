import django_filters
from .models import (
    Products,
    Brands,
    CategoryBrands,
    CategoryCharacteristics,
    ProductCharacteristics,
)


NAME_SORT_CHOICES = (
    ('name', 'Имя (А → Я)'),
    ('-name', 'Имя (Я → А)'),
)

BOOLEAN_CHOICES = (
    ('true', 'Есть'),
    ('false', 'Нет'),
)


class ProductsFilter(django_filters.FilterSet):
    """
        Фильтруем товарки
    """
    name_sort = django_filters.ChoiceFilter(
        choices=NAME_SORT_CHOICES,
        label='Сортировка по имени',
        method='filter_name_sort',
        empty_label = 'По умолчанию'
    )

    price_min = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Цена от'
    )
    price_max = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Цена до'
    )

    brand = django_filters.ModelChoiceFilter(
        queryset=Brands.objects.none(),
        label='Бренд',
        empty_label='Все'
    )

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category', None)
        super().__init__(*args, **kwargs)

        print("=== ProductsFilter.__init__ ===")
        print("GET params:", self.data)
        print("Category:", self.category)

        if not self.category:
            return

        self.filters['brand'].queryset = Brands.objects.filter(
            brand_category_brands__category=self.category
        ).distinct()
        print("Brand queryset:", self.filters['brand'].queryset)

        characteristics = CategoryCharacteristics.objects.filter(
            category=self.category
        ).select_related('characteristic')

        for item in characteristics:
            char_obj = item.characteristic
            print(f"Adding dynamic filter: char_{char_obj.id}, type: {char_obj.type}")
            self.add_dynamic_filter(char_obj)

    def add_dynamic_filter(self, char_obj):
        label = char_obj.name.split('____name____')[0].strip()
        field_name = f'char_{char_obj.id}'

        if char_obj.type == 'int':
            self.filters[field_name] = django_filters.NumberFilter(
                method=lambda qs, name, value, cid=char_obj.id: self._filter_characteristic(qs, value, cid),
                label=label
            )
        elif char_obj.type == 'float':
            self.filters[field_name] = django_filters.RangeFilter(
                method=lambda qs, name, value, cid=char_obj.id: self._filter_range_characteristic(qs, value, cid),
                label=f'{label} (от / до)'
            )
        elif char_obj.type == 'bool':
            self.filters[field_name] = django_filters.ChoiceFilter(
                choices=BOOLEAN_CHOICES,
                method=lambda qs, name, value, cid=char_obj.id: self._filter_boolean_characteristic(qs, value, cid),
                label=label,
                empty_label='Стандартно'
            )
        elif char_obj.type == 'str':
            self.filters[field_name] = django_filters.CharFilter(
                method=lambda qs, name, value, cid=char_obj.id: self._filter_characteristic(qs, value, cid),
                label=label
            )

    def filter_name_sort(self, queryset, name, value):
        print("filter_name_sort called:", name, value)
        return queryset.order_by(value) if value else queryset

    def _filter_characteristic(self, queryset, value, char_id):
        print(f"_filter_characteristic called: char_id={char_id}, value={value}")
        if value in [None, '']:
            print("Skipping _filter_characteristic due to empty value")
            return queryset
        return queryset.filter(
            product_characteristics__characteristic_id=char_id,
            product_characteristics__value__icontains=value
        )

    def _filter_boolean_characteristic(self, queryset, value, char_id):
        print(f"_filter_boolean_characteristic called: char_id={char_id}, value={value}")
        if value in [None, '']:
            print("Skipping _filter_boolean_characteristic due to empty value")
            return queryset
        return queryset.filter(
            product_characteristics__characteristic_id=char_id,
            product_characteristics__value__iexact=value
        )

    def _filter_range_characteristic(self, queryset, value, char_id):
        print(f"_filter_range_characteristic called: char_id={char_id}, value={value}")
        if value is None:
            print("Skipping _filter_range_characteristic due to None value")
            return queryset

        start = getattr(value, 'start', None)
        stop = getattr(value, 'stop', None)
        print(f"Range start={start}, stop={stop}")

        if start is not None:
            queryset = queryset.filter(
                product_characteristics__characteristic_id=char_id,
                product_characteristics__value__gte=start
            )
        if stop is not None:
            queryset = queryset.filter(
                product_characteristics__characteristic_id=char_id,
                product_characteristics__value__lte=stop
            )
        return queryset

    class Meta:
        model = Products
        fields = ['name_sort', 'price_min', 'price_max', 'brand']