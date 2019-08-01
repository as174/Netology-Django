from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_show_test = Counter()
counter_click_test = Counter()
counter_click = Counter()

def index(request):
    landing_type = request.GET.get('from-landing')
    if landing_type == 'test':
        counter_click_test['qty'] += 1
    elif landing_type == 'original':
        counter_click['qty'] += 1
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    return render_to_response('index.html')


def landing(request):
    landing_type = request.GET.get('ab-test-arg')
    if landing_type == 'test':
        response = 'landing_alternate.html'
        counter_show_test['qty'] += 1
    else:
        response = 'landing.html'
        counter_show['qty'] += 1
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    return render_to_response(response)


def stats(request):
    try:
        test_conversion = round(counter_click_test['qty'] / counter_show_test['qty'], 2)
    except ZeroDivisionError:
        test_conversion = 0

    try:
        original_conversion = round(counter_click['qty'] / counter_show['qty'], 2)
    except ZeroDivisionError:
        original_conversion = 0
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    return render_to_response('stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
