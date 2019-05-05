from django.core.validators import MinLengthValidator
from django.db import models

class Bank(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now=True)
    modified_on = models.DateTimeField(auto_now=True)

    def to_json(self):
        return {
                'id': self.id,
                'name': self.name.upper(),
                'is_active': self.is_active
                }

    def __unicode__(self):
        return '%s' % (self.name)


class BankBranch(models.Model):
    ifsc = models.CharField(max_length=11, unique=True, db_index=True, validators=[MinLengthValidator(11)])
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    branch_name = models.CharField(max_length=100, db_index=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=50, db_index=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        unique_together = ('bank', 'branch_name', 'city')

    def __unicode__(self):
        return '%s - %s' % (self.bank.name, self.branch_name)

    def to_json(self):
        return {
            'id': self.id,
            'ifsc': self.ifsc.upper(),
            'bank_name': self.bank.name.upper(),
            'branch_name': self.branch_name.upper(),
            'city': self.city.upper(),
            'district': self.district.upper(),
            'state': self.state.upper(),
            'address': self.address.upper()
        }