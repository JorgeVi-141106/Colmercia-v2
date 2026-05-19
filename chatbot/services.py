from products.models import Product, Region, Event
from django.db.models import Q


class ChatbotService:
    def __init__(self):
        self.intents = {
            'saludo': ['hola', 'buenos', 'buenas', 'hola!', 'hi', 'hello'],
            'productos': ['producto', 'productos', 'comprar', 'comprar', 'artículo', 'articulos'],
            'region': ['región', 'region', 'de donde', 'origen', 'donde es'],
            'buscar': ['buscar', 'encontrar', 'busco', 'necesito', 'quiero'],
            'evento': ['evento', 'eventos', 'conecta', 'promoción', 'promocion'],
            'ayuda': ['ayuda', 'help', 'como', 'qué puedes', 'que puedes'],
            'gracias': ['gracias', 'thank', 'agradec'],
            'despedida': ['adiós', 'adios', 'bye', 'chau', 'hasta luego'],
        }

    def process_message(self, message):
        message_lower = message.lower()
        intent = self._detect_intent(message_lower)

        if intent == 'saludo':
            return self._greeting()
        elif intent == 'productos':
            return self._products_info()
        elif intent == 'region':
            return self._regions_info()
        elif intent == 'buscar':
            return self._search_help()
        elif intent == 'evento':
            return self._events_info()
        elif intent == 'ayuda':
            return self._help()
        elif intent == 'gracias':
            return self._thanks()
        elif intent == 'despedida':
            return self._goodbye()
        else:
            return self._fallback()

    def _detect_intent(self, message):
        for intent, keywords in self.intents.items():
            for keyword in keywords:
                if keyword in message:
                    return intent
        return 'desconocido'

    def _greeting(self):
        return {
            'response': '¡Hola! 👋 Bienvenido a Colmercia - Conecta con Colombia. ¿En qué puedo ayudarte hoy? Puedo ayudarte a encontrar productos, explorar regiones o informarte sobre eventos.',
            'suggestions': ['Ver productos', 'Ver regiones', 'Ver eventos']
        }

    def _products_info(self):
        products = Product.objects.filter(activo=True)[:5]
        if products:
            product_list = '\n'.join([f"• {p.nombre} - ${p.precio} ({p.region.nombre})" for p in products])
            return {
                'response': f'Tenemos estos productos disponibles:\n{product_list}\n\nPuedes buscar por región o categoría usando los filtros.',
                'suggestions': ['Buscar por región', 'Ver todas las categorías']
            }
        return {'response': 'No hay productos disponibles en este momento.'}

    def _regions_info(self):
        regions = Region.objects.all()
        if regions:
            region_list = '\n'.join([f"• {r.nombre}" for r in regions])
            return {
                'response': f'Nuestras regiones disponibles:\n{region_list}\n\nCada región tiene productos únicos con historia cultural.',
                'suggestions': ['Ver productos de una región', 'Historia cultural']
            }
        return {'response': 'No hay regiones registradas aún.'}

    def _search_help(self):
        return {
            'response': 'Para buscar productos puedes usar:\n• ?region=uuid (filtrar por región)\n• ?categoria=string (filtrar por categoría)\n• /api/products/products/ para ver todo',
            'suggestions': ['Ver todos los productos', 'Ver regiones']
        }

    def _events_info(self):
        events = Event.objects.filter(activo=True)
        if events:
            event_list = '\n'.join([f"• {e.nombre} ({e.region.nombre}) - Hasta {e.fecha_fin}" for e in events])
            return {
                'response': f'Eventos "Conecta con Colombia":\n{event_list}',
                'suggestions': ['Ver productos del evento']
            }
        return {'response': 'No hay eventos activos en este momento. Próximamente tendrás eventos por región.'}

    def _help(self):
        return {
            'response': 'Puedo ayudarte con:\n• 💡 Recomendaciones de productos\n• 🗺️ Información de regiones\n• 🎉 Eventos disponibles\n• 🔍 Cómo buscar productos\n• 📦 Estado de tus pedidos\n\n¡Simplemente pregúntame!',
            'suggestions': ['Ver productos', 'Ver regiones', 'Mis pedidos']
        }

    def _thanks(self):
        return {'response': '¡De nada! 😊 Estoy aquí para ayudarte. ¿Hay algo más en lo que pueda asistirte?'}

    def _goodbye(self):
        return {'response': '¡Gracias por visitarnos! 🇨🇴 Vuelve pronto a descubrir la riqueza cultural de Colombia.'}

    def _fallback(self):
        return {
            'response': 'No entendí completamente. 😕 Puedes preguntarme sobre:\n• Productos disponibles\n• Regiones de Colombia\n• Eventos "Conecta con Colombia"\n• Cómo buscar productos\n\nO escribe "ayuda" para más opciones.',
            'suggestions': ['Ver productos', 'Ver regiones', 'Ayuda']
        }

    def recommend_products(self, occasion=None, region=None):
        queryset = Product.objects.filter(activo=True)
        if region:
            queryset = queryset.filter(region__nombre__icontains=region)
        products = queryset[:5]

        if not products:
            return {'response': 'No encontré productos con esos criterios. ¿Qué te parece explorar otras regiones?'}

        product_list = '\n'.join([f"• {p.nombre} - ${p.precio}" for p in products])
        return {
            'response': f'Te recomiendo estos productos:\n{product_list}',
            'products': [{'id': str(p.id), 'name': p.nombre, 'price': str(p.precio)} for p in products]
        }