def calculate_order_discount(total: float, tier: str) -> float:
    """Calculate the discounted order total based on customer tier.
    
    Args:
        total: The original order total.
        tier: The customer tier ('VIP' or 'Standard').
    
    Returns:
        The total after applying the discount.
    """
    if tier == "VIP":
        return total * 0.80
    elif tier == "Standard":
        return total * 0.95
    return total


def process_payment_settlement(amount: float, num_splits: int) -> float:
    """Split a payment amount evenly across a number of splits.
    
    Args:
        amount: The total payment amount.
        num_splits: The number of ways to split the payment.
    
    Returns:
        The per-split amount, rounded to 2 decimal places.
    
    Note:
        Bug: if num_splits == 0, causes ZeroDivisionError.
    """
    return round(amount / num_splits, 2)