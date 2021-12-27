from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class Account(models.Model):
    owner = models.ForeignKey(User, on_delete=CASCADE)
    account_name = models.CharField(max_length=100)
    currency = models.CharField(max_length=5)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.account_name + " in " + self.currency


class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=CASCADE)
    name = models.CharField(max_length=32)
    types_of_transactions = (
        ("income", "income"),
        ("expense", "expense")
    )
    type = models.CharField(
        max_length=32,
        choices=types_of_transactions,
        default='income'
    )

    def __str__(self):
        return self.name + " by " + self.owner.username


class Transaction(models.Model):
    types_of_transactions = (
        ("income", "income"),
        ("expense", "expense")
    )
    type = models.CharField(
        max_length=32,
        choices=types_of_transactions,
        default='income'
    )
    account = models.ForeignKey(Account, on_delete=CASCADE)
    amount = models.PositiveIntegerField()
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=CASCADE)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description
