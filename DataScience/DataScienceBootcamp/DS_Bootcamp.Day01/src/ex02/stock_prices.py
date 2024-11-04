import sys


def get_company_stock_price() -> None:
    """"""

    script_args: list = sys.argv

    COMPANIES: dict = {
        "Nokia": "NOK",
        "Apple": "AAPL",
        "Tesla": "TSLA",
        "Netflix": "NFLX",
        "Microsoft": "MSFT",
    }

    STOCKS: dict = {
        "NOK": 3.37,
        "AAPL": 287.73,
        "MSFT": 173.79,
        "NFLX": 416.90,
        "TSLA": 724.88,
    }

    if len(script_args) == 2:
        if script_args[1].capitalize() in COMPANIES.keys():
            company_ticket: str = COMPANIES[script_args[1].capitalize()]

            print(STOCKS[company_ticket])
        else:
            print("Unknown company")


if __name__ == "__main__":
    get_company_stock_price()