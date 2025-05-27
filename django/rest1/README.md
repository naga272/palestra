# Django Rest
Quando hai un frontend con Vue.js e un backend con Django, lo scenario tipico è questo:

- Vue (FE) gira come app separata (es. su localhost:5173 o localhost:3000)
- Django (BE) espone delle API (di solito con Django REST Framework) su un altro indirizzo (es. localhost:8000)
- Vue chiama Django tramite richieste HTTP (es. fetch() o axios)
- Serve gestire bene il CORS (Cross-Origin Resource Sharing) perché stai comunicando tra due domini/porte diversi

## 1. Prepara il backend Django con API

Installa Django REST Framework:

```bash
pip install djangorestframework
pip install django-cors-headers
```

Nel tuo settings.py, aggiungi:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOW_ALL_ORIGINS = True  # Per test, poi fallo più sicuro
```

Oppure, se vuoi solo far parlare Vue:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # o la porta che usa Vue
]
```

Poi crea una semplice API, ad esempio:

```python
# file views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def test_api(request):
    return Response({"message": "Ciao da Django!"})


# file urls.py
from django.urls import path
from .views import test_api

urlpatterns = [
    path('api/test/', test_api),
]
```

## 2. Prepara Vue per fare richieste


```bash
npm install axios
```

```js
<script>

import axios from 'axios'

export default {
    mounted() {
        axios.get('http://localhost:8000/api/test/')
        .then(res => {
            console.log(res.data)
        })
        .catch(err => {
            console.error("Errore:", err)
        })
    }
}

</script>
```


## 3. Avvia tutto

- Django: python manage.py runserver
- Vue: npm run dev

Dovresti vedere sulla console il messaggio: "Ciao da Django!"


### Errori tipici

- Errore **CORS**: devi configurare django-cors-headers come sopra
- Errore **404/500**: l'URL potrebbe essere sbagliato o la view non registrata
- **HTTPS**: se sei in produzione, non mischiare http e https
