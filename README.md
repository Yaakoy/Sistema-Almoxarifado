# Sistema de Almoxarifado

Sistema web para controle de estoque e separação de pedidos em um almoxarifado com múltiplas filiais. Projeto de estudo desenvolvido em Python e Django, inspirado em problemas reais de gestão de estoque.

> Status: em desenvolvimento. Todos os dados usados são fictícios.

## O problema

Sistemas de almoxarifado costumam sofrer com lentidão, quedas e limite de licenças. A proposta é um sistema enxuto, focado só no fluxo essencial:

1. O vendedor consulta o estoque de cada filial.
2. O vendedor cria um pedido.
3. O almoxarife separa e confere o pedido.
4. O sistema gera a etiqueta de expedição em PDF.
5. O pedido é fechado e despachado.

## Tecnologias

- Python
- Django
- SQLite (desenvolvimento), com migração prevista para PostgreSQL
- Git e GitHub

## Modelo de dados

Banco relacional com oito tabelas ligadas por chaves estrangeiras:

- **Filial**: unidades da empresa.
- **Usuario**: login, cargo (vendedor, jovem aprendiz, almoxarife, chefe) e filial.
- **Produto**: código, nome e descrição.
- **Estoque**: saldo de cada produto em cada filial.
- **Pedido** e **ItemPedido**: pedidos e seus produtos.
- **Transferencia**: empréstimo de itens entre filiais.
- **Etiqueta**: histórico de etiquetas geradas por pedido.

## Como rodar

```
git clone https://github.com/Yaakoy/Sistema-Almoxarifado.git
cd almoxarifado-django
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Depois, acesse http://127.0.0.1:8000/admin/ e entre com o usuário criado.

## Próximos passos

- [x] Modelos do banco de dados e painel administrativo
- [ ] Tela de consulta de estoque por filial
- [ ] Criação de pedidos pelo vendedor
- [ ] Separação e conferência pelo almoxarife
- [ ] Geração de etiquetas em PDF
- [ ] Transferência de estoque entre filiais