from django.utils import timezone
from dateutil.relativedelta import relativedelta


from company_structure.models import HOLIDAYS

import holidays

ONE_DAY = timezone.timedelta(days=1)

class RepaymentSchedule:
    def __init__(self, id, date, month_payment, percent_sum, loan_body_sum, loan_remains) -> str:
        self.id = id
        self.date = date
        self.month_payment = month_payment
        self.percent_sum = percent_sum
        self.loan_body_sum = loan_body_sum
        self.loan_remains = loan_remains
    
    def __str__(self) -> str:
        return f'{self.date}'


def next_business_day(date):
    next_day = date
    while next_day.weekday() in holidays.WEEKEND or next_day in HOLIDAYS:
        next_day += ONE_DAY
    return next_day


def generate_repayment_dates(self):
    per_month_percent = self.loan_product.percent / 12
    clear_funding_amount = self.funding_amount - self.first_instalment

    month_payment = round(clear_funding_amount * (per_month_percent + (per_month_percent / ((1 + per_month_percent) ** self.funding_period - 1))), ndigits=2)
    repayment_schedule = []
    payment = RepaymentSchedule(
                id=0,
                date=self.start_date,
                month_payment=0,
                percent_sum=0,
                loan_body_sum=0,
                loan_remains=clear_funding_amount
            )
    repayment_schedule.append(payment)
    
    for prev_loan in range(int(self.funding_period)):
        
        prev_payment = repayment_schedule[prev_loan]
        date = next_business_day(self.start_date + relativedelta(months=prev_payment.id + 1))
        percent_sum = round(prev_payment.loan_remains * per_month_percent, ndigits=2)
        loan_body_sum = month_payment - percent_sum
        
        loan_remains = prev_payment.loan_remains - loan_body_sum
        if prev_loan == self.funding_period - 1:
            loan_body_sum = month_payment - percent_sum + (prev_payment.loan_remains - (month_payment - percent_sum))
            loan_remains = prev_payment.loan_remains - loan_body_sum
            month_payment += prev_payment.loan_remains - (month_payment - percent_sum)
            
        payment = RepaymentSchedule(
            id=prev_payment.id + 1,
            date=date,
            month_payment=month_payment,
            percent_sum=percent_sum,
            loan_body_sum=loan_body_sum,
            loan_remains=loan_remains
        )
        
        repayment_schedule.append(payment)
    return repayment_schedule
