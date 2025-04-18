import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import catalog_router, products_router, inflation_router


if os.getenv('IS_PROD') == 'True':
    origins = [
        os.getenv('FRONTEND_URL')
    ]
else:
    origins = [
        'http://localhost:8000',
        'http://localhost:3000'
    ]


app = FastAPI(
    title='supermarket-py-backend',
    description='API for comparing prices of products across different supermarkets',
    version='1.0.0',
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST'],
    allow_headers=['*'],
)


app.include_router(catalog_router)
app.include_router(products_router)
app.include_router(inflation_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)