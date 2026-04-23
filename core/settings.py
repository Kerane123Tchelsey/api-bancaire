REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [],  # ← AJOUTE CETTE LIGNE
}
# Désactiver l'authentification pour Swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': None,
    'USE_SESSION_AUTH': False,
}
# Swagger settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': None,
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    'SUPPORTED_SUBMIT_METHODS': [
        'get',
        'post',
        'put',
        'delete',
        'patch'
    ],
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
}