import datetime
import os
from django.shortcuts import render

def file_list(request, date=None):
    template_name = 'index.html'

    context = {
        'files': [],
        'date': date
    }


    if (date != None):
        context['date'] = datetime.datetime.strptime(date, '%Y-%m-%d')

    files = os.listdir('files')
    for file in files:
        path = ('files/' + f'{file}')
        os.stat_result = os.stat(path)
        ctime_ts = os.stat_result.st_ctime
        mtime_ts = os.stat_result.st_mtime
        ctime = datetime.datetime.fromtimestamp(ctime_ts).date()
        mtime = datetime.datetime.fromtimestamp(mtime_ts).date()
        file_dict = {'name': file, 'ctime': ctime, 'mtime': mtime}
        ctime_date = ctime.strftime('%Y-%m-%d')
        if (ctime_date == date) or (date == None):
            context['files'].append(file_dict)



    return render(request, template_name, context)


def file_content(request, name):
    if name in os.listdir('files'):
        file_name = os.path.join('files', name)
        with open(file_name, 'r') as f:
            content = f.read()

    return render(
        request,
        'file_content.html',
        context={'file_name': name, 'file_content': content}
        )

