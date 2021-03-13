from django.apps import AppConfig


class ControlePedidosConfig(AppConfig):
    name = 'controle_pedidos'

    def ready(self):
        import core.signals
