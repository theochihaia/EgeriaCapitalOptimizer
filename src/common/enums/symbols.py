from enum import Enum


class SymbolSet(Enum):
    ROBINHOOD = "robinhood"
    FIDELITY = "fidelity"
    FID_FOLIO = "fidelity_fid_folio"
    CHASE = "chase"
    CHASE_INTERNATIONAL = "chase_international"
    TESTING = "testing"


def get_symbols(symbol_set: SymbolSet):
    if symbol_set == SymbolSet.ROBINHOOD:
        return [
            "AAPL",
            "ACN",
            "AMZN",
            "ATO",
            "CL",
            "COST",
            "CRM",
            "CTAS",
            "DE",
            "GD",
            "GOOGL",
            "HES",
            "HRL",
            "JNJ",
            "JPM",
            "LCID",
            "LIN",
            "LLY",
            "MDT",
            "MSFT",
            "NEE",
            "NUE",
            "NVDA",
            "NVO",
            "PEP",
            "PG",
            "PXD",
            "ROP",
            "TGT",
            "TMO",
            "V",
            "WMT",
        ]
    elif symbol_set == SymbolSet.FIDELITY:
        return ["SMH", "VEA", "VOO", "XLK", "XLY", "XLV"]
    elif symbol_set == SymbolSet.FID_FOLIO:
        return [
            "AMN",
            "UNH",
            "NVDA",
            "AVGO",
            "HDB",
            "NVO",
            "MSFT",
            "NEE",
            "FCN",
            "ATO",
            "VRTX",
            "DE",
            "AAPL",
            "KR",
            "MRK",
            "ELMD",
            "GOOGL",
            "GMAB",
            "NOC",
            "PG",
            "NICE",
            "LMT",
            "TTC",
            "TSM",
            "AMZN",
            "ACN",
            "JPM",
            "TGT",
            "PEP",
            "TJX",
            "COST",
            "MSA",
            "ABT",
            "SYY",
            "AMGN",
        ]
    elif symbol_set == SymbolSet.CHASE:
        return ["BLV", "EFG", "FHLC", "FSKAX", "FTEC", "PDI", "PTY", "VCR", "XSD"]
    elif symbol_set == SymbolSet.CHASE_INTERNATIONAL:
        return ["BNDX", "ECH", "EDEN", "EIRL", "EWJ", "EWL", "EWT", "EWY", "SMIN"]
    elif symbol_set == SymbolSet.TESTING:
        return ["AAPL", "ACN", "COST"]
    else:
        raise ValueError(f"Unknown symbol set: {symbol_set}")
