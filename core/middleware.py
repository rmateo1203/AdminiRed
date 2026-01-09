"""
Middleware personalizado para AdminiRed
"""
import re


class NgrokSkipBrowserWarningMiddleware:
    """
    Middleware que agrega el header ngrok-skip-browser-warning
    para evitar la página de advertencia de ngrok en desarrollo.
    
    Según la documentación de ngrok, enviar este header con cualquier valor
    hace que ngrok omita la página de advertencia del navegador.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Patrón para detectar dominios de ngrok
        self.ngrok_pattern = re.compile(r'.*\.(ngrok-free\.dev|ngrok\.io|ngrok\.app)$')

    def __call__(self, request):
        # Detectar si la solicitud viene de ngrok
        host = request.get_host().split(':')[0]  # Remover puerto si existe
        
        response = self.get_response(request)
        
        # Agregar el header en la respuesta si es ngrok
        # Este header le dice a ngrok que omita la página de advertencia
        if self.ngrok_pattern.match(host):
            response['ngrok-skip-browser-warning'] = 'true'
        
        return response

