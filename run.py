from auth_service.main import app as auth_app
from catalog_service.main import app as cat_app

if __name__ == '__main__':
    auth = auth_app
    cat = cat_app
    import uvicorn
