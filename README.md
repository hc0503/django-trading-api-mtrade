# MTrade API

## Requirements
- Python 3.9
- pipenv
- Postgres 12.6
- Docker (optional)

## Quickstart
```bash
./scripts/launch-postgres.sh
pipenv shell
pipenv install
export $(cat .example.env | xargs)
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

## Directory structure
```text
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

## Development guidelines
### Tests
- Every module must include unit tests
- Tests should consider success and failure scenarios
- During the first development phase, code coverage should be at least of 80% per module, it should eventually be expanded to 100%

### Architecture
- Apps should be isolated
    - Each layer can only include direct calls to functions in lower layers (Interface > Application > Domain > Infrastructure)
    - The application layer is the main point of integration of domain APIs
    - Django apps should not include foreign keys to other django apps.
    - Interactions should be modelled as API/function calls.
    - Django signals can be used to decouple applications.
    - When using Django signals, handlers should be registered in the application layer, avoiding direct calls from one domain module to another.
    - When modules depend on each other directly use dependency inversion.

### Database
- Do not use DB generated ids for entities, use uuid4 instead
- Create model ids in the application, not the database
- For any given operation perform all DB writes atomically in a single transaction
