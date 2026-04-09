"""Fnac.fr adapter (httpx session + POST /basket/add)."""

from sites.fnac.buyer import AddToCartResult, FnacBuyer, FnacSite
from sites.fnac.config import SITE_ID
from sites.fnac.endpoints import CHECKLIST, Endpoint
from sites.fnac.http_client import ApiResult, FnacHttpClient
from sites.fnac.interface import fnac_watch_from_interface, is_fnac_job
from sites.fnac.models import FnacWatchConfig
from sites.fnac.monitor import FnacMonitor, WatchSnapshot

__all__ = [
    "AddToCartResult",
    "ApiResult",
    "CHECKLIST",
    "Endpoint",
    "FnacBuyer",
    "FnacHttpClient",
    "FnacMonitor",
    "FnacSite",
    "FnacWatchConfig",
    "SITE_ID",
    "WatchSnapshot",
    "fnac_watch_from_interface",
    "is_fnac_job",
]
