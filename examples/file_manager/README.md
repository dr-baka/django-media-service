# Django File Manager Example

Contoh aplikasi Django sederhana yang menggunakan `django-media-service` sebagai dependency.

## Menjalankan

```bash
cd examples/file_manager
python -m venv .venv
source .venv/bin/activate
pip install -e ../..
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Endpoint utama

- API root: `http://127.0.0.1:8000/media/`
- Django admin: `http://127.0.0.1:8000/admin/`

## Konfigurasi storage (RustFS default)

Aplikasi ini default ke backend `rustfs` melalui `DJANGO_MEDIA_SERVICE` pada `settings.py`.
Silakan sesuaikan `ENDPOINT`, `ACCESS_KEY`, `SECRET_KEY`, dan `BUCKET_NAME`.
