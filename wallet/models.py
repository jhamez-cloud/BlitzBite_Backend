from django.db import models

# Create your models here.
class Wallet(models.Model):
    class CurrencyAvailable(models.TextChoices):
        DOLLAR = 'Dollar','dollar'
        CEDIS = 'Cedis','cedis'
        NAIRA = 'Naira','naira'
        EURO = 'Euro','euro'
        POUNDS = 'Pounds','pounds'

    wallet_id = models.CharField(max_length=100,unique=True,editable=False)
    user = models.OneToOneField('user.User', on_delete=models.CASCADE, related_name='wallets',unique=True)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    currency = models.CharField(max_length=100,choices=CurrencyAvailable.choices,default=CurrencyAvailable.CEDIS)
    promotional_credits = models.DecimalField(max_digits=10,decimal_places=2,default=0.00) 
    reward_points = models.PositiveIntegerField()

class WalletTransaction(models.Model):
    class TransactionType(models.TextChoices):
        CREDIT = 'Credit','credit'
        DEBIT = 'Debit','debit'
        REFUND = 'Refund','refund'
        REWARD = 'Reward','reward'

    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE,related_name="wallet_transactions")
    type = models.CharField(max_length=100,choices=TransactionType.choices,default=TransactionType.CREDIT)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    date = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=30)

