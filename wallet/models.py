# wallet/models.py
from django.db import models


class Wallet(models.Model):
    class CurrencyAvailable(models.TextChoices):
        DOLLAR = 'dollar', 'Dollar'
        CEDIS = 'cedis', 'Cedis'
        NAIRA = 'naira', 'Naira'
        EURO = 'euro', 'Euro'
        POUNDS = 'pounds', 'Pounds'

    wallet_id = models.CharField(max_length=100, unique=True, editable=False)
    user = models.OneToOneField('user.User', on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=20, choices=CurrencyAvailable.choices, default=CurrencyAvailable.CEDIS)
    promotional_credits = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reward_points = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.wallet_id:
            self.wallet_id = f"wallet_{self.pk:03d}"
            Wallet.objects.filter(pk=self.pk).update(wallet_id=self.wallet_id)


class WalletTransaction(models.Model):
    class TransactionType(models.TextChoices):
        CREDIT = 'credit', 'Credit'
        DEBIT = 'debit', 'Debit'
        REFUND = 'refund', 'Refund'
        REWARD = 'reward', 'Reward'

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="wallet_transactions")
    type = models.CharField(max_length=20, choices=TransactionType.choices, default=TransactionType.CREDIT)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['-date']