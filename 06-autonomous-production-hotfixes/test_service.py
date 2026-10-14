import pytest
from broken_service import calculate_order_discount, process_payment_settlement

def test_calculate_order_discount_vip():
    """Verify VIP discount applies 20% off."""
    assert calculate_order_discount(100.0, "VIP") == 80.0

def test_calculate_order_discount_standard():
    """Verify Standard discount applies 5% off."""
    assert calculate_order_discount(100.0, "Standard") == 95.0

def test_process_payment_settlement_valid():
    """Verify payment splitting across valid positive splits."""
    assert process_payment_settlement(100.0, 2) == 50.0
    assert process_payment_settlement(90.0, 3) == 30.0

def test_process_payment_settlement_zero_splits():
    """
    CRITICAL EDGE CASE: When 0 splits requested, system must not crash with 500 ZeroDivisionError.
    Should safely return the full un-split amount.
    """
    assert process_payment_settlement(100.0, 0) == 100.0

def test_process_payment_settlement_negative():
    """Edge case: negative splits should safely return the un-split amount."""
    assert process_payment_settlement(100.0, -1) == 100.0