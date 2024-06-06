from django.db import models
from django.contrib.auth.models import User
from loginApp.models import CustomerSignUp
import uuid
# Create your models here.


class loanCategory(models.Model):
    loan_name = models.CharField(max_length=250)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    creation_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.loan_name


class loanRequest(models.Model):
    customer = models.ForeignKey(CustomerSignUp, on_delete=models.CASCADE, related_name='loan_customer')
    category = models.ForeignKey(loanCategory, on_delete=models.CASCADE, null=True)
    request_date = models.DateField(auto_now_add=True)
    status_date = models.CharField(
        max_length=150, null=True, blank=True, default=None)
    reason = models.TextField()
    status = models.CharField(max_length=100, default='pending')
    amount = models.PositiveIntegerField(default=0)
    year = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.customer.user.username

    def calculate_interest(self):
        # Calculate interest based on the amount, interest rate, and time (years)
        print(self.category.interest_rate.to_decimal() * 12)
        interest = (self.amount * float(self.category.interest_rate.to_decimal()) * self.year) / 100
        return interest

    def total_amount_with_interest(self):
        # Calculate total amount including interest
        total_amount = self.amount + self.calculate_interest()
        return total_amount

    def get_interest_rate(self):
        return self.category.interest_rate


class CustomerLoan(models.Model):
    customer = models.ForeignKey(CustomerSignUp, on_delete=models.CASCADE, related_name='loan_user')
    total_loan = models.PositiveIntegerField(default=0)
    payable_loan = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.customer.user.username


class loanTransaction(models.Model):
    customer = models.ForeignKey(CustomerSignUp, on_delete=models.CASCADE, related_name='transaction_customer')
    category = models.ForeignKey(loanCategory, on_delete=models.CASCADE, null=True)
    transaction = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.PositiveIntegerField(default=0)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer.user.username
