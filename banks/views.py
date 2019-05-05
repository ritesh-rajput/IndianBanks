import json

from django.http import HttpResponse
from banks.models import Bank, BankBranch


def success_response(data):
    return HttpResponse(json.dumps({'status_code': 200, 'status': 'success', 'data': data}),
                        content_type="application/json")


def bad_request(msg):
    return HttpResponse(json.dumps({'status_code': 400, 'status': 'failed', 'message': msg}),
                        content_type="application/json")


def error_response(msg):
    return HttpResponse(json.dumps({'status_code': 500, 'status': 'failed', 'message': msg}),
                        content_type="application/json")


def home(request):
    return HttpResponse(
        'Hey, Read the doc %s. - %s' % ('<a href="https://docs.google.com/document/d/1p9xKq8OnaO-DnUj36qQOm24witRIrbMkT551dcVGAQg/edit?usp=sharing">here</a>', 'Valar Dohaeris!'))

def banks(request):
    city = request.GET.get('city')
    bank_name = request.GET.get('bank_name')

    filter_dict = {}
    if city:
        filter_dict['city'] = city.lower()
    if bank_name:
        filter_dict['bank__name'] = bank_name.lower()

    if filter_dict:
        result_list = BankBranch.objects.filter(**filter_dict)
    else:
        result_list = Bank.objects.filter(is_active=True)

    response = []
    for result in result_list:
        response.append(result.to_json())

    return success_response(response)


def bank_branch_detail(request, ifsc_code):
    if len(ifsc_code) != 11:
        return bad_request('IFSC code should have 11 characters.')

    try:
        bank_details = BankBranch.objects.get(ifsc=ifsc_code.lower())
    except BankBranch.DoesNotExist:
        return error_response('Bank details does not exists with IFSC code %s' % ifsc_code)
    except Exception as e:
        return error_response('Something went wrong. Please try again after some time.')

    return success_response(bank_details.to_json())


def bank_branches(request, bank_id):
    if bank_id < 0:
        return bad_request('Please provide valid bank id')

    try:
        bank_branches = BankBranch.objects.filter(bank_id=bank_id)
    except BankBranch.DoesNotExist:
        return error_response('Bank details does not exists with id %s' % bank_id)

    response = []
    for bank_branch in bank_branches:
        response.append(bank_branch.to_json())

    return success_response(response)




