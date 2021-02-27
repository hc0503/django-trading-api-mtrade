
# django imports
from django.db import models

class COBOrder(models.Model):

    ACTIVE_STATUS = 'active'
    CANCELLED_STATUS = 'cancelled'
    EXPIRED_STATUS = 'expired'
    PENDING_STATUS = 'pending'
    FULL_ALLOCATION_STATUS = 'full-allocation'
    STATUS_CHOICES = [
        (ACTIVE_STATUS, 'Active'),
        (CANCELLED_STATUS, 'Cancelled'),
        (EXPIRED_STATUS, 'Expired'),
        (PENDING_STATUS, 'Pending'),
        (FULL_ALLOCATION_STATUS, 'Full Allocation')
    ]

    BUY_DIRECTION = 'buy'
    SELL_DIRECTION = 'sell'
    DIRECTION_CHOICES = [
        (BUY_DIRECTION, 'Buy'),
        (SELL_DIRECTION, 'Sell')
    ]

    id = models.UUIDField(primary_key=True, editable=False)
    trader_id = models.UUIDField()
    # TODO: Evaluate if institution field should be added here, this would speed up queries
    isin = models.UUIDField()
    submission = models.DateTimeField()
    expiration = models.DateTimeField()
    price = models.DecimalField(max_digits=40, decimal_places=20)
    size = models.IntegerField()
    status = models.CharField(max_length=150, choices=STATUS_CHOICES)
    dirty_price = models.DecimalField(max_digits=40, decimal_places=20)
    notional = models.DecimalField(max_digits=40, decimal_places=20)
    spread = models.DecimalField(
        max_digits=40, decimal_places=20, null=True, blank=True)
    discount_margin = models.DecimalField(
        max_digits=40, decimal_places=20, null=True, blank=True)
    yield_value = models.DecimalField(max_digits=40, decimal_places=20)
    # TODO: Change fields to foreign keys
    parent = models.UUIDField(null=True)
    origin = models.UUIDField(null=True)
    #parent = models.ForeignKey('self', on_delete=models.CASCADE,
    #                                 null=True, blank=True, related_name='child')
    #origin = models.ForeignKey('self', on_delete=models.CASCADE,
    #                                 null=True, blank=True)
    direction = models.CharField(
        max_length=150, choices=DIRECTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
