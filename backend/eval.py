from scraper import Scraper


def get_margin_of_safety(ticker):
    """
    Calculates the margin of safety and stick price for a stock with a given ticker.

    Args:
        ticker (str): The stock ticker symbol to calculate a MOS and sticker price for.
    Returns:
        (float, float): A 2-tuple containing the margin of safety and sticker price respectively.
    """
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
    """
    Calculates the price of an equity in `years` years from now given the TTM EPS, EPS growth rate and future P/E ratio.

    Args:
        eps_ttm (float): The current TTM EPS.
        eps_growth_rate (float): The rate to grow the equity over `years` years.
        future_pe (float): The future P/E ratio of the equity in `years` years.
        years (int): The number of years into the future to calculate the equity price.
    Returns:
       float: The price of an equity `years` years from now.
    """
    eps_in_ten_years = eps_ttm * ((1.0 + eps_growth_rate * 0.01) ** years)
    return eps_in_ten_years * future_pe
