# Imágenes del Proyecto

## Imagen de Torres para Home

Para usar una imagen local en lugar de la URL de Unsplash:

1. Coloca tu imagen de torres en este directorio con el nombre: `torres-hero.jpg` o `torres-hero.png`
2. Actualiza la ruta en `templates/core/home.html`:
   ```html
   <img src="{% static 'images/torres-hero.jpg' %}" ...>
   ```
3. Asegúrate de que la imagen tenga:
   - Resolución recomendada: 1920x600px o superior
   - Formato: JPG, PNG o WebP
   - Peso optimizado: < 500KB

## Imagen de Fondo para Login

Para usar una imagen local en el login:

1. Coloca tu imagen de torres en este directorio con el nombre: `torres-login.jpg` o `torres-login.png`
2. Actualiza el CSS en `templates/core/login.html`:
   ```css
   background-image: url('{% static 'images/torres-login.jpg' %}');
   ```
3. Asegúrate de que la imagen tenga:
   - Resolución recomendada: 1920x1080px o superior (full HD)
   - Formato: JPG, PNG o WebP
   - Peso optimizado: < 800KB
   - La imagen cubrirá toda la pantalla, así que usa una de alta calidad

## Fuentes de Imágenes Gratuitas

- Unsplash: https://unsplash.com/s/photos/telecommunications-tower
- Pexels: https://www.pexels.com/search/telecommunications%20tower/
- Pixabay: https://pixabay.com/images/search/telecommunications%20tower/

