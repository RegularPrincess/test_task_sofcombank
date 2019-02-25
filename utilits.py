import logging

HEADERS = {
        'cookie': "__cfduid=d2a004b46d6a080f9ee10ef63590c11671551009023",
        'origin': "https://egrp365.ru",
        'dnt': "1",
        'accept': "application/json, text/plain, */*",
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundaryEoImAhCyHxM9O82C",
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/72.0.3626.96 Safari/537.36'
}


def create_form_data(fields_dict):
    item = u"------WebKitFormBoundaryEoImAhCyHxM9O82C\r\nContent-Disposition: form-data; name=\"{}\"\r\n\r\n{}\r\n"
    end = u"------WebKitFormBoundaryEoImAhCyHxM9O82C--"
    body = ''
    for key, value in fields_dict.items():
        body += item.format(key, value)
    body += end
    body.encode('utf-8')
    body = body.replace('None', '')
    logging.info('Auto created body: ' + body)
    return body
