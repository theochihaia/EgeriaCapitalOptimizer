from enum import Enum

class SymbolSet(Enum):
    ROBINHOOD = "robinhood"
    FID_FOLIO = "fid_folio"
    FID_FOLIO_V2 = "fid_folio_v2"
    TESTING = "testing"
    SP500 = "sp500"
    NOBL = "nobl"
    IJR_SMALL_CAP = "ijr_small_cap"
    IJH_MID_CAP = "ijh_mid_cap"
    IYK_CONSUMER_STAPLES = "iyk_consumer_staples"
    IYW_TECHNOLOGY = "iyw_technology"
    IYF_FINANCIAL = "iyf_financial"
    ALEX = "alex"

def get_symbols(symbol_set: SymbolSet):
    symbols = set()
    for symbol in symbol_set:
        dir = f"src/common/portfolios/{symbol.value}.txt"
        with open(dir) as f:
            symbols.update(f.read().splitlines())
    return list(symbols)
