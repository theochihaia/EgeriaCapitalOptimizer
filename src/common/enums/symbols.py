from enum import Enum

class SymbolSet(Enum):
    ROBINHOOD = "robinhood"
    FID_FOLIO = "fid_folio"
    TESTING = "testing"
    SP500 = "sp500"
    NOBL = "nobl"
    IJR_SMALL_CAP = "ijr_small_cap"

def get_symbols(symbol_set: SymbolSet):
    dir = f"src/common/portfolios/{symbol_set.value}.txt"
    with open(dir) as f:
        return f.read().splitlines()
