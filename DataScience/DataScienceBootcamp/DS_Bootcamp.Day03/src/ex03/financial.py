#!/usr/bin/env python3

import sys
import bs4
import time
import requests


def main() -> None:
    """"""

    request_base_url: str = (
        "https://finance.yahoo.com/quote/@TICKET@/financials/"
    )

    request_headers: dict = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
        + "image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0)"
        + " Gecko/20100101 Firefox/131.0",
    }

    parsed_data: tuple = get_parsed_data(request_base_url, request_headers)

    print(parsed_data)


def get_parsed_data(request_base_url: str, request_headers: dict) -> tuple:
    """"""

    time.sleep(5)

    correct_tickets: list = [
        "EBIT",
        "EBITDA",
        "Basic EPS",
        "Diluted EPS",
        "Gross Profit",
        "Pretax Income",
        "Tax Provision",
        "Total Revenue",
        "Total Expenses",
        "Cost of Revenue",
        "Interest Income",
        "Interest Expense",
        "Operating Income",
        "Normalized EBITDA",
        "Normalized Income",
        "Operating Expense",
        "Tax Rate for Calcs",
        "Net Interest Income",
        "Total Unusual Items",
        "Basic Average Shares",
        "Other Income Expense",
        "Diluted Average Shares",
        "Reconciled Depreciation",
        "Reconciled Cost of Revenue",
        "Tax Effect of Unusual Items",
        "Net Income Common Stockholders",
        "Net Non Operating Interest Income",
        "Total Operating Income as Reported",
        "Total Unusual Items Excluding Goodwill",
        "Diluted NI Available to Com Stockholders",
        "Net Income from Continuing & Discontinued Operation",
        "Net Income from Continuing Operation Net Minority Interest",
    ]

    script_args: list = sys.argv

    parsed_data: list = []

    request_ticket: str | None = None
    required_field: str | None = None

    try:
        request_ticket: str = script_args[1]
        required_field: str = script_args[2]
    except Exception as err:
        raise Exception(f"ERROR! Incorrect script arguments. {err}")

    if required_field not in correct_tickets:
        raise ValueError("ERROR! Incorrect required field.")

    parsed_data.append(required_field)

    request_url: str = request_base_url.replace("@TICKET@", request_ticket)

    response: object = requests.get(request_url, headers=request_headers)

    if response.status_code == 200:
        try:
            response_content: str = response.text
            soup: bs4.BeautifulSoup = bs4.BeautifulSoup(
                response_content, "html.parser"
            )

            temp_elements: list = soup.find_all(
                "div", attrs={"title": required_field}
            )

            required_data_fields: list = (
                temp_elements[0]
                .find_parent()
                .find_parent()
                .find_all(
                    "div",
                    attrs={
                        "class": ["column yf-t22klz", "column yf-t22klz alt"]
                    },
                )
            )

            for index in range(len(required_data_fields)):
                parsed_data.append(required_data_fields[index].text.rstrip())

            return tuple(parsed_data)
        except Exception as err:
            raise Exception(f"ERROR! {err}")
    else:
        raise Exception("ERROR!. Incorrect request URL.")


if __name__ == "__main__":
    main()
