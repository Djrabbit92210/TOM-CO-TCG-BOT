from typing import Any
from sites.fnac.buyer import FnacBuyer

def run_fnac_checkout(buyer: FnacBuyer) -> bool:
    """Execute the automated checkout sequence for Fnac."""
    print("LOG: Execution layer initiating Fnac checkout...")
    return buyer.checkout()
