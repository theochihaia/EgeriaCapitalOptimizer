from enum import Enum

class Portfolio(Enum):
    ROBINHOOD = "robinhood"
    FID_FOLIO = "fid_folio"
    FID_FOLIO_V3 = "fid_folio_v3"
    FID_FOLIO_V4 = "fid_folio_v4"
    TESTING = "testing"
    SP500 = "sp500"
    NOBL = "nobl"
    IJR_SMALL_CAP = "ijr_small_cap"
    IJH_MID_CAP = "ijh_mid_cap"
    IYK_CONSUMER_STAPLES = "iyk_consumer_staples"
    IYW_TECHNOLOGY = "iyw_technology"
    IXJ_HEALTHCARE = "ixj_healthcare"
    IYF_FINANCIAL = "iyf_financial"
    ALEX = "alex"
    SK_ALPHA_DIV_GROWTH = "sk_alpha_div_growth",
    VANGUARD_ETFS = "vanguard_etfs"
