from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Etiqueta,
    Estoque,
    Filial,
    ItemPedido,
    Pedido,
    Produto,
    Transferencia,
    Usuario,
)


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Dados do almoxarifado", {"fields": ("cargo", "filial")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Dados do almoxarifado", {"fields": ("cargo", "filial")}),
    )


admin.site.register(Filial)
admin.site.register(Produto)
admin.site.register(Estoque)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
admin.site.register(Transferencia)
admin.site.register(Etiqueta)