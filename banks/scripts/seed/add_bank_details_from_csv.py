#!/usr/bin/python
import csv
import sys
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'IndianBanks.settings'

ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/banks')]

if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')

import django
django.setup()

from banks.models import Bank, BankBranch

filename = sys.argv[1]

with open(filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    row_no = 0
    for row in reader:
        ifsc = row['ifsc'].lower()
        branch_name = row['branch'].lower()
        address = row['address'].lower()
        city = row['city'].lower()
        district = row['district'].lower()
        state = row['state'].lower()
        bank_name = row['bank_name'].lower()

        try:
            bank = Bank.objects.get_or_create(name=bank_name)[0]
            BankBranch.objects.get_or_create(bank=bank, ifsc=ifsc, city=city, branch_name=branch_name, address=address,
                                             district=district, state=state)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            continue

        row_no += 1
    print('%s bank details were processed.' % row_no)