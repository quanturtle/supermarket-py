# Export routers
from routes.catalog import catalog_router
from routes.products import products_router
from routes.inflation import inflation_router

__all__ = ["catalog_router", "products_router", "inflation_router"]