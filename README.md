# MTrade API

## Requirements
- Python 3.9
- pipenv

## Quickstart
```
pipenv shell
pipenv install
```

## Directory structure
```
root/
    mtrade/             -> The base project directory
        settings.py
        drivers/        -> asgi.py and wsgi.py
        interface/      -> interface layer modules
        application/    -> application layer modules
        domain/         -> domain layer modules
        infrastructure/ -> infrastructure layer modules
    lib/                -> reusable modules
    external-apps/      -> apps not following the project's dev guidelines
    manage.py
    ...
```

## General development guidelines
- Every module must include unit tests, consider success and failure scenarios
- Apps should be isolated
    - Each layer can only include direct calls to functions in lower layers (Interface > Application > Domain > Infrastructure)
    - The application layer is the main point of integration of domain APIs
    - Django apps should not include foreign keys to other django apps. Interactions should be modelled as API calls. Django signals can be used to decouple applications.
        - When using Django signals, handlers should be registered in the application layer, avoiding direct calls from one domain module to another.
    - Use dependency inversion for infrastructure modules whenever possible.
