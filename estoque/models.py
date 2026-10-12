from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Filial(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "filiais"

    def __str__(self):
        return self.nome


class Produto(models.Model):
    codigo = models.CharField(max_length=50, unique= True)
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank= True)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"



class Estoque(models.Model):
        produto = models.ForeignKey(Produto, on_delete= models.PROTECT)
        filial = models.ForeignKey(Filial, on_delete= models.PROTECT)
        quantidade = models.PositiveIntegerField(default= 0)

        class Meta:
            constraints = [
                models.UniqueConstraint(
                    fields=["produto", "filial"],
                    name="estoque_unico_por_filial",
                )
            ]
        
        def __str__(self):
            return f"{self.produto} @ {self.filial}: {self.quantidade}"


class Usuario(AbstractUser):
    class Cargo(models.TextChoices):
        VENDEDOR = "vendedor", "Vendedor"
        APRENDIZ = "aprendiz", "Jovem aprendiz"
        ALMOXARIFE = "almoxarife", "Almoxarife"
        CHEFE = "chefe", "Chefe de almoxarifado"


    cargo = models.CharField(
        max_length=20,
        choices=Cargo.choices,
        default=Cargo.VENDEDOR,
    )
    filial = models.ForeignKey(
        Filial,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        )

    def __str__(self):
        return self.get_full_name() or self.usernome


class Pedido(models.Model):
    class Status(models.TextChoices):
        ABERTO = "aberto", "Aberto"
        EM_SEPARACAO = "em_separacao", "Em separação"
        FECHADO = "fechado", "Fechado"
        CANCELADO = "cancelado", "Cancelado"

    cliente = models.CharField(max_length=150)
    vendedor = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    filial = models.ForeignKey(Filial, on_delete= models.PROTECT)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ABERTO,
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    fechado_em = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete = models.CASCADE,
        related_name="itens",
    )
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["pedido", "produto"],
                name= "item_unico_por_pedido",
            )
        ]
    def __str__(self):
        return f"{self.quantidade} x {self.produto} (pedido {self.pedido_id})"


class Transferencia(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    filial_origem = models.ForeignKey(
        Filial,
        on_delete=models.PROTECT,
        related_name="transferencias_enviadas",
    )
    filial_destino = models.ForeignKey(
        Filial,
        on_delete=models.PROTECT,
        related_name="transferencias_recebidas",
    )
    data = models.DateTimeField(auto_now_add=True)

class Meta:
    verbose_name_plural = "transferencia"
    constraints = [
            models.CheckConstraint(
                condition=~models.Q(filial_origem=models.F("filial_destino")),
                name="transferencia_origem_diferente_destino",
            )
    ]
    def __str__(self):
        return f"{self.quantidade} x {self.produto}: {self.filial_origem} -> {self.filial_destino}"

class Etiqueta(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete= models.CASCADE,
        related_name= "etiquetas",
    )
    quantidade = models.PositiveIntegerField(default=1)
    gerada_por = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    data = models.DateTimeField(auto_now_add=True)
    retirada_por = models.CharField(max_length=150, blank=True)
    observacao = models.TextField(blank=True)

    def __str__(self):
        return f"{self.quantidade} etiqueta(s) do pedido {self.pedido_id}"







# =====================================================
# COLINHA DO MODELS.PY (o que aprendi)
# =====================================================

# --- BÁSICO ---
# class nome(models.Model)  -> cada classe vira uma TABELA no banco.
# Cada linha dentro da classe (nome = models....) vira uma COLUNA.
# id -> o Django cria sozinho, número automático. Não preciso escrever.

# --- TIPOS DE CAMPO ---
# CharField(max_length=N)   -> texto curto, com limite de caracteres.
# TextFieldd                 -> texto longo (descrição, observação).
# PositiveIntegerField      -> número inteiro, nunca negativo.
# DateTimeField             -> data e hora.

# --- OPÇÕES DOS CAMPOS ---
# default=X          -> valor padrão se ninguém preencher.
# unique=True        -> não permite dois iguais (ex: código do produto).
# blank=True         -> pode ficar VAZIO no formulário/tela.
# null=True          -> pode ficar VAZIO no banco (guarda "nada").
#   Regra prática: campo opcional geralmente leva os dois (null=True, blank=True).
#   Texto opcional leva só blank=True (fica vazio como "").
# auto_now_add=True  -> o Django preenche data/hora sozinho ao CRIAR o registro.
#   Ex: criado_em, data da transferência, data da etiqueta.
# fechado_em (Pedido) -> começa vazio (null=True) e só é preenchido
#   quando o pedido é fechado.

# --- LISTAS FECHADAS (TextChoices) ---
# Cargo e Status usam TextChoices: só aceita os valores da lista.
# Evita erro de digitação ("almoxarifi").
# Formato: nome = "valor_no_banco", "Texto que aparece na tela"
# Status do pedido: aberto -> em_separacao -> fechado (ou cancelado).

# --- RELACIOnomeNTOS (o que torna o banco RELACIONAL) ---
# ForeignKey(Tabela)  -> chave estrangeira: esta linha aponta para
#   uma linha de OUTRA tabela (ex: Estoque aponta para Produto e Filial).
# on_delete=PROTECT   -> BLOQUEIA apagar se ainda tem algo ligado.
# on_delete=CASCADE   -> apagar o "pai" apaga os "filhos" junto
#   (pedido apagado leva os itens e as etiquetas).
# related_nome="itens" -> nome para ir pelo caminho inverso:
#   pedido.itens.all() em vez de pedido.itempedido_set.all().
# Duas ForeignKey para a MESMA tabela (Transferencia -> Filial)
#   exigem related_nome diferente em cada uma.

# --- REGRAS DO BANCO (dentro de class Meta) ---
# UniqueConstraint(fields=[...])  -> a COMBINAÇÃO não pode repetir.
#   Ex: um produto só tem 1 linha de estoque por filial.
#   Ex: o mesmo produto não aparece 2x no mesmo pedido.
# CheckConstraint  -> regra que o próprio banco garante.
#   Ex: transferência com origem diferente do destino.
# verbose_nome_plural -> como o plural aparece na tela ("filiais").

# --- MÉTODO __str__ ---
# def __str__(self) -> define o texto que representa um registro
#   na tela. Sem ele, aparece "Filial object (1)".

# --- USUÁRIO PERSONALIZADO ---
# AbstractUser -> já traz login, senha (criptografada), nome e e-mail.
#   Eu só acrescento cargo e filial.
# AUTH_USER_MODEL = "estoque.Usuario" (no settings.py) -> avisa o Django
#   que o usuário do sistema é o meu.
#   Tem que ser definido ANTES da primeira migração.
# "Nível de permissão" sai do CARGO (evita guardar a mesma coisa 2x).

# --- CONFIGURAÇÃO DO PROJETO ---
# venv -> ambiente virtual: pasta isolada com as bibliotecas do projeto.
#   Ativar: venv\Scripts\activate  (aparece (venv) no terminal)
# INSTALLED_APPS (settings.py) -> lista de apps. Sem 'estoque' ali,
#   o Django ignora as minhas tabelas.
# Projeto (almoxarifado) = configurações gerais.
# App (estoque) = as funcionalidades e tabelas.
# =====================================================