# Python libraries
import io
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter as xw

# Django libraries
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Local imports
from .forms import RequestForm, RequestFormRu
from .models import UserRequest, UserRequestRu
from .utils.arbitration import ai_chooser
from .utils.arbitration_ru import ai_chooser_ru
from .tasks import get_rates


def home(request):
    """ Eng version of Home page with Calculator UI (based on RequestForm).
        If valid data is submitted via POST request UserRequest object is created,
        UserRequest object id is stored in session, corresponding Cost objects
        are created via ai_chooser function call, user is redirected to Results page.
        Otherwise Home page refreshes and error messages are shown (if any)
    """
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            req = form.save()
            request.session['last_id'] = req.pk
            amount = req.amount
            arbs = req.arbs
            proc = req.proc
            parties = req.parties
            measures = req.ea
            ais = req.ai.all()
            ai_chooser(req, ais, amount, arbs, proc, parties, measures)
            return HttpResponseRedirect(reverse('calc:result'))
        else:   # Server-side validation fails
            context = {
                'title': 'Arbitration Fee Calculator',
                'form': form,
            }
            return render(request, 'calc/home.html', context)
    else:
        form = RequestForm()
        context = {
            'form': form,
            'title': 'Arbitration Calculator',
        }
        return render(request, 'calc/home.html', context)


def home_ru(request):
    """ Ru version of Home page with Calculator UI (based on RequestFormRu).
        If valid data is submitted via POST request UserRequestRu object is created,
        UserRequestRu object id is stored in session, corresponding CostRu objects
        are created via ai_chooser_ru function call, user is redirected to Results page.
        Otherwise Home page refreshes and error messages are shown (if any)
    """
    if request.method == 'POST':
        form = RequestFormRu(request.POST)
        if form.is_valid():
            req = form.save()
            request.session['last_id'] = req.pk
            amount = req.amount
            arbs = req.arbs
            proc = req.proc
            type = req.type
            ais = req.ai.all()
            ai_chooser_ru(req, ais, amount, arbs, proc, type)
            return HttpResponseRedirect(reverse('calc:result-ru'))
        else:   # Server-side validation fails
            context = {
                'title': 'Арбитражный калькулятор',
                'form': form,
            }
            return render(request, 'calc/home-ru.html', context)
    else:
        form = RequestFormRu()
        context = {
            'form': form,
            'title': 'Арбитражный калькулятор',
        }
        return render(request, 'calc/home-ru.html', context)


def result(request):
    """ Eng version of the page with results for user's request (UserRequest object).
        If session contains request id (last_id key) all results (Cost objects)
        for corresponding request are displayed.
        Otherwise user is redirected to Home page
    """
    if 'last_id' in request.session:
        last_id = request.session['last_id']
        req = UserRequest.objects.get(pk=last_id)
        amount = req.amount
        arbs = req.arbs
        proc = req.proc
        parties = req.parties
        measures = req.ea
        res = req.costs.all().order_by('arb_fee')
        context = {
            'title': 'Arbitration Fee Calculator - Results',
            'result': res,
            'amount': amount,
            'arbs': arbs,
            'proc': proc,
            'parties': parties,
            'measures': measures,
        }
        return render(request, 'calc/result.html', context)
    else:   # no 'last_id' in session
        return HttpResponseRedirect(reverse('calc:home'))


def result_ru(request):
    """ Ru version of the page with results for user's request (UserRequest object).
        If session contains request id (last_id key) all results (Cost objects)
        for corresponding request are displayed.
        Otherwise user is redirected to Home page
    """
    if 'last_id' in request.session:
        last_id = request.session['last_id']
        req = UserRequestRu.objects.get(pk=last_id)
        amount = req.amount
        arbs = req.arbs
        proc = req.proc
        type = req.type
        res = req.costs.all().order_by('arb_fee')
        context = {
            'title': 'Арбитражный калькулятор - результаты',
            'result': res,
            'amount': amount,
            'arbs': arbs,
            'proc': proc,
            'type': type,
        }
        return render(request, 'calc/result-ru.html', context)
    else:   # no 'last_id' in session
        return HttpResponseRedirect(reverse('calc:home-ru'))


def about(request):
    """ About page """
    context = {'title': 'Arbitration Fee Calculator - About'}
    return render(request, 'calc/about.html', context)


def about_ru(request):
    """ About page (Russian version) """
    context = {'title': 'О калькуляторе'}
    return render(request, 'calc/about-ru.html', context)


def to_xlsx(request):
    """ Creates an xlsx workbook with results in buffer and returns it in
        a HttpResponse object
    """
    # get a request object and corresponding results
    if 'last_id' in request.session:
        last_id = request.session['last_id']
        req = UserRequest.objects.get(pk=last_id)
        res = req.costs.all().order_by('ai__arb_inst')

    # create a workbook and add a worksheet in memory stream
    output = io.BytesIO()
    res_workbook = xw.Workbook(output, {'in_memory': True})
    res_worksheet = res_workbook.add_worksheet(name='Results')

    # cells formatting
    ttl = res_workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'center',
        'bg_color': '#E1E1E1',
        'font_size': 14,
        })
    column_name = res_workbook.add_format({
        'bold': True,
        'bg_color': '#E1E1E1',
        'align': 'center',
        'valign': 'center',
    })
    currency = res_workbook.add_format({'num_format': '#,##0.00'})

    # add title with all parameters
    res_worksheet.merge_range('A1:I1', 'Merged Range')
    title = (
        f'Fees for {req.amount} USD, {req.arbs} Arbitrator(s), {req.parties} '
        f'Parties, {req.proc} Procedure, Emergency Measures: {req.ea}.'
    )
    res_worksheet.write('A1', title, ttl)

    # set columns widths rows hieghts
    res_worksheet.set_column('A:F', 20)
    res_worksheet.set_column('G:I', 40)
    res_worksheet.set_row(0, 30)
    res_worksheet.set_row(1, 30)

    # wrap text
    cell_format = res_workbook.add_format()
    cell_format.set_text_wrap()

    # add column names
    res_worksheet.write('A2', 'Arbitral Institution', column_name)
    res_worksheet.write('B2', 'Arbitration Fee (USD)', column_name)
    res_worksheet.write('C2', 'Arbitrators Fee (USD)', column_name)
    res_worksheet.write('D2', 'Administration Fee (USD)', column_name)
    res_worksheet.write('E2', 'Registration Fee (USD)', column_name)
    res_worksheet.write('F2', 'Emergency Measures (USD)', column_name)
    res_worksheet.write('G2', 'NB', column_name)
    res_worksheet.write('H2', 'Comment 1', column_name)
    res_worksheet.write('I2', 'Comment 2', column_name)

    # add data
    row = 2
    col = 0
    for ai in res:
        res_worksheet.write(row, col, ai.ai.arb_inst)
        res_worksheet.write(row, col+1, ai.arb_fee, currency)
        res_worksheet.write(row, col+2, ai.arbs_fee, currency)
        res_worksheet.write(row, col+3, ai.admin_fee, currency)
        res_worksheet.write(row, col+4, ai.reg_fee, currency)
        if ai.ea_fee:
            res_worksheet.write(row, col+5, ai.ea_fee, currency)
        if ai.comment0:
            res_worksheet.write(row, col+6, ai.comment0, cell_format)
        res_worksheet.write(row, col+7, ai.comment1, cell_format)
        if ai.comment2:
            res_worksheet.write(row, col+8, ai.comment2, cell_format)
        row += 1

    res_workbook.close()

    # creating response
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # telling the browser what the file is named
    response['Content-Disposition'] = "attachment; filename=Results.xlsx"

    # putting the spreadsheet data into the HttpResponse object
    response.write(output.getvalue())

    return response


def to_xlsx_ru(request):
    """ Creates an xlsx workbook with results in buffer and returns it in
        a HttpResponse object
    """
    # get a request object and corresponding results
    if 'last_id' in request.session:
        last_id = request.session['last_id']
        req = UserRequestRu.objects.get(pk=last_id)
        res = req.costs.all().order_by('ai__arb_inst')

    # create a workbook and add a worksheet in memory stream
    output = io.BytesIO()
    res_workbook = xw.Workbook(output, {'in_memory': True})
    res_worksheet = res_workbook.add_worksheet(name='Results')

    # cells formatting
    ttl = res_workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'center',
        'bg_color': '#E1E1E1',
        'font_size': 14,
        })
    column_name = res_workbook.add_format({
        'bold': True,
        'bg_color': '#E1E1E1',
        'align': 'center',
        'valign': 'center',
    })
    currency = res_workbook.add_format({'num_format': '#,##0.00'})

    # add title with all parameters
    res_worksheet.merge_range('A1:H1', 'Merged Range')
    title = (
        f'Условия: {req.amount} руб., {req.arbs} арбитр(а), {req.proc} процеду'
        f'ра, {req.type} спор.'
    )
    res_worksheet.write('A1', title, ttl)

    # set columns widths rows hieghts
    res_worksheet.set_column('A:E', 25)
    res_worksheet.set_column('F:H', 40)
    res_worksheet.set_row(0, 30)
    res_worksheet.set_row(1, 30)

    # wrap text
    cell_format = res_workbook.add_format()
    cell_format.set_text_wrap()

    # add column names
    res_worksheet.write('A2', 'Арбитражное учредение', column_name)
    res_worksheet.write('B2', 'Арбитражный сбор (руб.)', column_name)
    res_worksheet.write('C2', 'Гонораный сбор (руб.)', column_name)
    res_worksheet.write('D2', 'Административный сбор (руб.)', column_name)
    res_worksheet.write('E2', 'Регистрационный сбор (руб.)', column_name)
    res_worksheet.write('F2', 'NB', column_name)
    res_worksheet.write('G2', 'Комментарий 1', column_name)
    res_worksheet.write('H2', 'Комментарий 2', column_name)

    # add data
    row = 2
    col = 0
    for ai in res:
        res_worksheet.write(row, col, ai.ai.arb_inst)
        res_worksheet.write(row, col+1, ai.arb_fee, currency)
        res_worksheet.write(row, col+2, ai.arbs_fee, currency)
        res_worksheet.write(row, col+3, ai.admin_fee, currency)
        res_worksheet.write(row, col+4, ai.reg_fee, currency)
        if ai.comment0:
            res_worksheet.write(row, col+5, ai.comment0, cell_format)
        res_worksheet.write(row, col+6, ai.comment1, cell_format)
        if ai.comment2:
            res_worksheet.write(row, col+7, ai.comment2, cell_format)
        row += 1

    res_workbook.close()

    # creating response
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # telling the browser what the file is named
    response['Content-Disposition'] = "attachment; filename=Results.xlsx"

    # putting the spreadsheet data into the HttpResponse object
    response.write(output.getvalue())

    return response


def bar_chart(request):
    """ Creates a PDF file with group bar chart of the results in buffer and
        returns it in a HttpResponse object
    """
    # get a request object and corresponding results
    if 'last_id' in request.session:
        last_id = request.session['last_id']
        req = UserRequest.objects.get(pk=last_id)
        res = req.costs.all().order_by('arb_fee')

    # creating chart
    plt.style.use('fivethirtyeight')
    plt.rcParams.update({'font.size': 7})

    # data to plot
    ai = [cost.ai.arb_inst.split()[0] for cost in res]
    arbs_fee = np.array([ai.arbs_fee for ai in res])
    admin_fee = np.array([ai.admin_fee for ai in res])
    ea_fee = np.array([ai.ea_fee for ai in res])

    # creating bar
    ind = [x for x, _ in enumerate(ai)]
    plt.bar(
        ind, ea_fee, width=0.8, label='Emergency Measures',
        color='#d9c1c1', bottom=arbs_fee+admin_fee
    )
    plt.bar(
        ind, admin_fee, width=0.8, label='Administrative Fee',
        color='silver', bottom=arbs_fee
    )
    plt.bar(
        ind, arbs_fee, width=0.8, label='Arbitrators Fee',
        color='#CDD5CD',
    )

    # editing ticks, labels, legend and title
    ax = plt.gca()
    ax.get_yaxis().set_tick_params(direction='out', pad=3, labelright=True)
    ax.get_xaxis().set_tick_params(direction='out', pad=2)

    for tick in ax.yaxis.get_majorticklabels():
        tick.set_verticalalignment('center')

    plt.yticks(rotation='90', fontsize=8)
    plt.xticks(ind, ai, rotation='27.5', fontsize=8)

    plt.ylabel('Arbitration Fee in USD', fontsize=10)

    plt.legend(fontsize=10)

    ttl = (
        f'FEES FOR\n'
        f'{req.amount} USD | {req.arbs} Arbitrator(s) | {req.parties} Parties'
        f'\n{req.proc} Procedure | Emergency Measures: {req.ea}'
    )
    plt.title(f"{ttl}", fontsize=10)

    # saving chart as pdf to memory stream
    buf_chart = io.BytesIO()
    plt.savefig(buf_chart, format='pdf', dpi=200)
    plt.close()

    # creating HttpResponse object
    response = HttpResponse(content_type='application/pdf')

    # telling the browser what the file is named
    response['Content-Disposition'] = "attachment; filename=Results.pdf"

    # putting the spreadsheet data into the HttpResponse object
    response.write(buf_chart.getvalue())

    return response


def bar_chart_ru(request):
    """ Creates a PDF file with group bar chart of the results in buffer and
        returns it in a HttpResponse object
    """
    # get a request object and corresponding results
    if 'last_id' in request.session:
        last_id = request.session['last_id']
        req = UserRequestRu.objects.get(pk=last_id)
        res = req.costs.all().order_by('arb_fee')

    # creating chart
    plt.style.use('fivethirtyeight')
    plt.rcParams.update({'font.size': 7})

    # data to plot
    ai = [cost.ai.arb_inst.split()[0] for cost in res]
    arbs_fee = np.array([ai.arbs_fee for ai in res])
    admin_fee = np.array([ai.admin_fee for ai in res])

    # creating bar
    ind = [x for x, _ in enumerate(ai)]
    plt.bar(
        ind, admin_fee, width=0.8, label='Административный сбор',
        color='silver', bottom=arbs_fee
    )
    plt.bar(
        ind, arbs_fee, width=0.8, label='Гонорарный сбор',
        color='#CDD5CD',
    )

    # editing ticks, labels, legend and title
    ax = plt.gca()
    ax.get_yaxis().set_tick_params(direction='out', pad=3, labelright=True)
    ax.get_xaxis().set_tick_params(direction='out', pad=2)

    for tick in ax.yaxis.get_majorticklabels():
        tick.set_verticalalignment('center')

    plt.yticks(rotation='90', fontsize=8)
    plt.xticks(ind, ai, rotation='27.5', fontsize=8)

    plt.ylabel('Арбитражный сбор (руб.)', fontsize=10)

    plt.legend(fontsize=10)

    ttl = (
        f'Результаты для\n'
        f'{req.amount} руб. | {req.arbs} арбитр(а) | {req.proc} процедура | '
        f'{req.type} спор'
    )
    plt.title(f"{ttl}", fontsize=10)

    # saving chart as pdf to memory stream
    buf_chart = io.BytesIO()
    plt.savefig(buf_chart, format='pdf', dpi=200)
    plt.close()

    # creating HttpResponse object
    response = HttpResponse(content_type='application/pdf')

    # telling the browser what the file is named
    response['Content-Disposition'] = "attachment; filename=Results.pdf"

    # putting the spreadsheet data into the HttpResponse object
    response.write(buf_chart.getvalue())

    return response


def update_rates_manulally(request):
    get_rates()

    return HttpResponseRedirect(reverse('calc:home'))
