from scraper import Scraper


def get_margin_of_safety(ticker):
    s = Scraper()
    years = 10

    # Trailing twelve-months EPS
    eps_ttm = s.get_eps_ttm(ticker)

    # The estimated EPS growth rate is the minimum of the average equity growth and the projected earnings growth (5 yr)
    eps_growth_rate = min(s.get_avg_equity_growth(ticker), s.get_avg_earnings_growth(ticker))
    future_pe = min(2 * eps_growth_rate, 0.8 * s.get_recent_pe(ticker))

    future_price = get_future_price(eps_ttm, eps_growth_rate, future_pe, years)
    sticker_price = int(future_price / 4)
    margin_of_safety = sticker_price / 2
    return margin_of_safety, sticker_price


def get_future_price(eps_ttm, eps_growth_rate, future_pe, years):
    eps_in_ten_years = eps_ttm * ((1.0 + eps_growth_rate * 0.01) ** years)
    return eps_in_ten_years * future_pe

if __name__ == '__main__':
    import sys
    ticker = sys.argv[1]
    mos = get_margin_of_safety(ticker)
    print(mos)