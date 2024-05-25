from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.db.models import Subquery, OuterRef, Q
from django.utils.html import format_html

from .models import Registrator, Price, TeamMember

DATE_TIME_FORMAT = "%m/%d/%Y, %H:%M:%S"

admin.site.empty_value_display = "Нет данных"


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "title", "contact", "photo", "sex")
    search_fields = ("name", "title", "contact", "sex")


class PriceRegistratorInline(admin.TabularInline):
    model = Price
    readonly_fields = ("last_change_at", "parse_at")
    fields = (
        "last_change_at",
        "parse_at",
        "domain",
        "price_reg",
        "reg_status",
        "price_prolong",
        "prolong_status",
        "price_change",
        "change_status",
    )
    extra = 1
    min_num = 1
    ordering = ("-parse__date",)

    @admin.display(description="Дата парсинга")
    def parse_at(self, obj):
        return obj.parse.date.strftime(DATE_TIME_FORMAT)

    @admin.display(description="Последнее изменение")
    def last_change_at(self, obj):
        return obj.updated_at.strftime(DATE_TIME_FORMAT)


class EmptyPriceFilter(admin.SimpleListFilter):
    title = "Стоимость"
    parameter_name = "empty_price"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Нет данных"),
            ("no", "Стоимость указана"),
        )

    def queryset(self, request, queryset):
        is_empty = (
            Q(last_reg__isnull=True)
            | Q(last_prolong__isnull=True)
            | Q(last_change__isnull=True)
        )
        if self.value() == "yes":
            return queryset.filter(is_empty)
        elif self.value() == "no":
            return queryset.exclude(is_empty)


@admin.register(Registrator)
class RegistratorAdmin(admin.ModelAdmin):
    inlines = (PriceRegistratorInline,)
    list_display = (
        "name",
        "website_link",
        "city",
        "price_reg",
        "price_prolong",
        "price_change",
    )
    list_filter = ("city", EmptyPriceFilter)

    @admin.display(description="Сайт")
    def website_link(self, obj):
        return format_html(
            "<a href='{0}' target='_blank'>{0}</a>", obj.website
        )

    def get_latest_price_subquery(self, field_name):
        return Subquery(
            Price.objects.filter(registrator=OuterRef("pk"))
            .order_by("-id")
            .values(field_name)[:1]
        )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        latest_price_fields = {
            "last_reg": self.get_latest_price_subquery("price_reg"),
            "last_prolong": self.get_latest_price_subquery("price_prolong"),
            "last_change": self.get_latest_price_subquery("price_change"),
        }
        return queryset.annotate(**latest_price_fields)

    @admin.display(description="Регистрация", ordering="last_reg")
    def price_reg(self, obj):
        return obj.last_reg

    @admin.display(description="Продление", ordering="last_prolong")
    def price_prolong(self, obj):
        return obj.last_prolong

    @admin.display(description="Перенос", ordering="last_change")
    def price_change(self, obj):
        return obj.last_change


admin.site.site_title = "Администрирование Ecodomen"
admin.site.site_header = "Администрирование Ecodomen"

admin.site.unregister(Group)
admin.site.unregister(User)
