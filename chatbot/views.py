from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .services import ChatbotService


class ChatbotView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        message = request.data.get('message', '')
        context = request.data.get('context', None)

        if not message:
            return Response({'error': 'Message is required'}, status=400)

        service = ChatbotService()

        if context and context.get('type') == 'recommend':
            region = context.get('region')
            response = service.recommend_products(region=region)
        else:
            response = service.process_message(message)

        return Response({
            'message': message,
            'response': response['response'],
            'suggestions': response.get('suggestions', []),
            'products': response.get('products', [])
        })


class ChatbotRecommendView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        region = request.query_params.get('region')
        occasion = request.query_params.get('occasion')

        service = ChatbotService()
        response = service.recommend_products(occasion=occasion, region=region)

        return Response(response)