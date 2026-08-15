# wallet/services.py
from decimal import Decimal
from django.db import transaction
from .models import Wallet, WalletTransaction


@transaction.atomic
def create_wallet_transaction(wallet_id, transaction_type, amount, description, reference):
    """The only sanctioned way to move money in/out of a wallet — locks the
    wallet row, applies the change, and records the transaction, all atomically.
    'amount' is always positive; direction is determined by transaction_type."""
    amount = Decimal(amount)
    if amount <= 0:
        raise ValueError("amount must be positive.")

    wallet = Wallet.objects.select_for_update().get(pk=wallet_id)

    if transaction_type in (WalletTransaction.TransactionType.CREDIT, WalletTransaction.TransactionType.REFUND, WalletTransaction.TransactionType.REWARD):
        wallet.balance += amount
    elif transaction_type == WalletTransaction.TransactionType.DEBIT:
        if wallet.balance < amount:
            raise ValueError("Insufficient wallet balance.")
        wallet.balance -= amount
    else:
        raise ValueError(f"Unknown transaction type: {transaction_type}")

    wallet.save(update_fields=['balance'])

    return WalletTransaction.objects.create(
        wallet=wallet,
        type=transaction_type,
        amount=amount,
        description=description,
        reference=reference,
    )