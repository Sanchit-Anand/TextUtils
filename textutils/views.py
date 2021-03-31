import smtplib
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contactus.html')


def about(request):
    return render(request, 'about.html')


def send(request):
    render(request, 'contactus.html')
    firstName = request.POST.get('firstName', 'none')
    lastName = request.POST.get('lastName', 'none')
    email = request.POST.get('email', 'none')
    password = request.POST.get('password', 'none')
    content = request.POST.get('content', 'none')
    requestTitle = request.POST.get('requestTitle', 'none')
    if firstName != '' and lastName != '' and email != '' and password != '' and content != '':
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(email, password)
            server.sendmail(email, 'sanchitanand20072008@gmail.com', content)
            server.close()
            params = {'firstName': firstName, 'lastName': lastName,
                      'email': email, 'content': content, 'requestTitle': requestTitle}
            return render(request, 'sendsuccess.html', params)
        except Exception as e:
            params = {'exception': e, 'firstName': firstName, 'lastName': lastName, 'email': email,
                      'password': password, 'content': content, 'requestTitle': requestTitle}
            return render(request, 'senderror.html', params)
    else:
        return render(request, 'blank.html')


def analyze(request):
    djtext = request.POST.get('text', 'default')
    check = djtext.replace(' ', '')
    # Check checkbox values
    removepunc = request.POST.get('removepunc', 'off')
    fullcaps = request.POST.get('fullcaps', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')

    # Check which checkbox is on
    if check == '':
        return render(request, 'errorwrite.html')

    if removepunc == "on":
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        analyzed = ""
        for char in djtext:
            if char not in punctuations:
                analyzed = analyzed + char

        params = {'purpose': 'Removed Punctuations', 'analyzed_text': analyzed}
        djtext = analyzed
        # return render(request, 'analyze.html', params)

    if(fullcaps == "on"):
        analyzed = ""
        for char in djtext:
            analyzed = analyzed + char.upper()

        params = {'purpose': 'Changed to Uppercase', 'analyzed_text': analyzed}
        djtext = analyzed
        # Analyze the text
        # return render(request, 'analyze.html', params)

    if(extraspaceremover == "on"):
        analyzed = ""
        for index, char in enumerate(djtext):
            if not(djtext[index] == " " and djtext[index+1] == " "):
                analyzed = analyzed + char

        params = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed}
        djtext = analyzed
        # Analyze the text
        # return render(request, 'analyze.html', params)

    if (newlineremover == "on"):
        analyzed = ""
        for char in djtext:
            if char != "\n" and char != "\r":
                analyzed = analyzed + char
        params = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed}

    if(removepunc != "on" and newlineremover != "on" and extraspaceremover != "on" and fullcaps != "on"):
        return render(request, 'errorselect.html')

    return render(request, 'analyze.html', params)
