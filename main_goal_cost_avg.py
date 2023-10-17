import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import numpy as np


class GoalCostAveraging:
    def __init__(
        self,
        initial_investment,
        current_investment,
        annual_increase,
        target_amount,
        start_date,
        end_date,
        expected_return=0.07,
    ):
        self.initial_investment = initial_investment
        self.current_investment = current_investment
        self.annual_increase = annual_increase
        self.target_amount = target_amount
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.target_end_date = datetime.strptime(end_date, "%Y-%m-%d")
        self.current_date = datetime.now()
        self.expected_return = expected_return

    def months_since_start(self):
        delta = self.current_date - self.start_date
        return delta.days // 30

    def months_until_target_end_date(self):
        delta = self.target_end_date - self.current_date
        return delta.days // 30

    def expected_investment(self):
        months = self.months_since_start()
        expected = self.initial_investment
        for month in range(months):
            expected += self.annual_increase / 12
            expected *= 1 + self.expected_return / 12  # Apply monthly return rate
        return expected

    def suggest_investment(self):
        investment_by_month = self.compute_investment_by_month()
        months_since_start = self.months_since_start()

        return investment_by_month[months_since_start] - self.current_investment

    """
    def suggest_investment(self):
        months_remaining = self.months_until_target_end_date()
        remaining_amount_needed = self.target_amount - self.current_investment
        suggested_monthly_investment = remaining_amount_needed / months_remaining
        return suggested_monthly_investment"""

    def total_months(self):
        delta = self.target_end_date - self.start_date
        return delta.days // 30

    def compute_investment_by_month(self):
        total_months = self.total_months()
        investment_by_month = [self.initial_investment]
        investment = self.initial_investment
        for month in range(total_months):
            remaining_months = total_months - month
            remaining_amount_needed = self.target_amount - investment
            monthly_investment = remaining_amount_needed / remaining_months
            investment += monthly_investment
            investment *= 1 + self.expected_return / 12
            investment_by_month.append(investment)
        return investment_by_month

    def generate_dates(self):
        current_date = (
            self.start_date
            if isinstance(self.start_date, datetime)
            else datetime.strptime(self.start_date, "%Y-%m-%d")
        )
        end_date = (
            self.target_end_date
            if isinstance(self.target_end_date, datetime)
            else datetime.strptime(self.target_end_date, "%Y-%m-%d")
        )
        dates = []
        while current_date <= end_date:
            dates.append(current_date)
            current_date += timedelta(days=30)  # approximate a month as 30 days
        return dates

    def plot_return_by_month(self):
        investment_by_month = self.compute_investment_by_month()
        dates = self.generate_dates()
        months_since_start = self.months_since_start()
        suggested_investment = self.suggest_investment()
        plt.plot(dates, investment_by_month, label="Investment Value")
        plt.scatter(
            dates[months_since_start],
            self.current_investment,
            color="g",
            label="Current Investment",
        )
        plt.annotate(
            f"${self.current_investment:,.2f} ({suggested_investment:,.2f})",
            (dates[months_since_start], self.current_investment),
            textcoords="offset points",
            xytext=(70, -5),
            ha="center",
        )
        plt.axhline(
            y=self.target_amount, color="r", linestyle="--", label="Target Amount"
        )
        plt.annotate(
            f"Target Amount: ${self.target_amount:,.2f}",
            xy=(dates[-1], self.target_amount),
            xytext=(-105, 5),
            textcoords="offset points",
            ha="right",
            va="center",
            fontsize=9,
        )
        plt.title("Investment Growth Over Time")
        plt.xlabel(f"Date (from {self.start_date} to {self.target_end_date})")
        plt.ylabel("Investment Value ($)")
        plt.legend()
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        plt.gca().xaxis.set_major_locator(mdates.YearLocator())
        plt.figtext(
            0.5,
            0.01,
            f"Suggested Investment: ${suggested_investment:,.2f}",
            ha="center",
            fontsize=9,
        )
        plt.gcf().autofmt_xdate()  # Format x-axis date labels for better readability

        plt.show()


# Usage
initial_investment = 500  # Starting with a $10,000 investment
annual_increase = 12000  # Increasing investment by $12,000 each year
target_amount = 90000  # Target amount of $100,000
start_date = "2023-01-01"  # Start date of the investment
end_date = "2030-01-01"  # Target end date of the investment
expected_return = 0.07  # Expected return of 7% per year

# Input
current_investment = 10000  # Current account balance

strategy = GoalCostAveraging(
    initial_investment,
    current_investment,
    annual_increase,
    target_amount,
    start_date,
    end_date,
    expected_return,
)
strategy.plot_return_by_month()
