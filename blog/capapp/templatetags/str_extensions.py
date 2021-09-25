from django import template

register = template.Library()


def capitalize(inputstr):
    return inputstr.capitalize()


def superoutput(inputstr):
    # Главная страница
    # ГлАвНаЯ СтРаНиЦа
    # result = []
    # for i in range(len(inputstr)):
    #     letter = inputstr[i]
    #     if i % 2 == 0:
    #         letter = letter.upper()
    #     result.append(letter)
    # return ''.join(result)

    #
    return ''.join([inputstr[i].upper() if i % 2 == 0 else inputstr[i] for i in range(len(inputstr))])


register.filter('capitalize', capitalize)
register.filter('sup', superoutput)
