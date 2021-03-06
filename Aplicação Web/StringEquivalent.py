from flask import render_template, request, flash, Markup
from collections import Iterable
from MyForms import Form
import pandas as pd
import datetime as dt
from datetime import datetime
from dateutil.parser import parse


url4 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/app/data/vacinometro-sp.csv'


def flatten(list):
    for item in list:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item


def regex_match(word, match):
    transchar = ''
    converted_word = ''
    list = []
    for char in word:
        if char in match.keys():
            transchar = match.get(char)
            list.append(transchar)
        else:
            transchar = char
            list.append(transchar)
    if list is not None:
        converted_word = ''.join(list)
    else:
        converted_word = word
    return converted_word


def regex_change(word, accent):
    converted_word = ''
    try:
        converted_word = accent[word]
    except KeyError:
        converted_word = word
    return converted_word


def regex_match_list(list, match):
    words = []
    for word in list:
        transchar = ''
        converted_word = ''
        chars = []
        for char in word:
            if char in match.keys():
                transchar = match.get(char)
                chars.append(transchar)

            else:
                transchar = char
                chars.append(transchar)

        if chars is not None:
            converted_word = ''.join(chars)
            words.append(converted_word)
        else:
            converted_word = word
            words.append(converted_word)
    return words


def regex_change_list(lista, accent):
    changes = []
    for word in lista:
        converted_word = ''
        word = word.title()
        if word in accent.keys():
            converted_word = accent[word]
            changes.append(converted_word)
        else:
            converted_word = word
            changes.append(converted_word)
    change = list(flatten(changes))
    return change


def city_filter_srag(df, city_request):
    form = Form()
    mini = '2020-01-01'
    maxi = datetime.now().strftime('%Y-%m-%d')
    dict_match = {'??': 'A', '??': 'A', '??': 'A', '??': 'A', '??': 'a', '??': 'a', '??': 'a', '??': 'a',
                  '??': 'E', '??': 'E', '???': 'E', '??': 'E', '??': 'e', '??': 'e', '???': 'e', '??': 'e',
                  '??': 'I', '??': 'I', '??': 'I', '??': 'i', '??': 'i', '??': 'i', '??': 'O', '??': 'O',
                  '??': 'O', '??': 'O', '??': 'o', '??': 'o', '??': 'o', '??': 'o', '??': 'U', '??': 'U',
                  '??': 'U', '??': 'u', '??': 'u', '??': 'u', '??': 'C', '??': 'c'}
    searches = []
    names = []
    if request.method == 'POST':
        if request.form['municipio_field'] != '':
            search = str(request.form.get('municipio_field'))
            searches = search.split(', ')
        else:
            df = df.query(
                "Munic??pio == 'S??o Jos?? dos Campos' | Munic??pio == 'Taubat??' | Munic??pio == 'Jacare??' | Munic??pio == "
                "'Lorena' | Munic??pio == 'Pindamonhangaba' | Munic??pio == 'Caraguatatuba' | Munic??pio == "
                "'Guaratinguet??' | Munic??pio == 'Ca??apava' | Munic??pio == 'Ubatuba' | Munic??pio == 'S??o Sebasti??o'")
            flash(Markup(f'<h1 class="cidades"> Dados das dez maiores cidades do Vale do Para??ba. Para acessar outras '
                         f'cidades, fa??a uma pesquisa personalizada.</h1>'))
            return df
    else:
        try:
            search = city_request[-1]
            searches = search.split(', ')
            if city_request[-1] == 'dumby':
                df = df.query(
                    "Munic??pio == 'S??o Jos?? dos Campos' | Munic??pio == 'Taubat??' | Munic??pio == 'Jacare??' | Munic??pio "
                    "== 'Lorena' | Munic??pio == 'Pindamonhangaba' | Munic??pio == 'Caraguatatuba' | "
                    "Munic??pio == 'Guaratinguet??' | Munic??pio == 'Ca??apava' | Munic??pio == 'Ubatuba' | Munic??pio == "
                    "'S??o Sebasti??o'")
                flash(Markup(f'<h1 class="cidades"> Dados das dez maiores cidades do Vale do Para??ba. Para acessar '
                             f'outras cidades, fa??a uma pesquisa personalizada.</h1>'))
                return df
        except IndexError:
            df = df.query(
                "Munic??pio == 'S??o Jos?? dos Campos' | Munic??pio == 'Taubat??' | Munic??pio == 'Jacare??' | Munic??pio == "
                "'Lorena' | Munic??pio == 'Pindamonhangaba' | Munic??pio == 'Caraguatatuba' | Munic??pio == "
                "'Guaratinguet??' | Munic??pio == 'Ca??apava' | Munic??pio == 'Ubatuba' | Munic??pio == 'S??o Sebasti??o'")
            flash(Markup(f'<h1 class="cidades"> Dados das dez maiores cidades do Vale do Para??ba. Para acessar '
                         f'outras cidades, fa??a uma pesquisa personalizada.</h1>'))
            return df
    filter = regex_match_list(searches, dict_match)
    dfs = {}
    for item in filter:
        result = df[df.Munic??pio.str.contains(item, case=False)]
        if result.empty is False:
            dfs[item] = result
            names.append(item.title())
        else:
            flash(Markup(f'<h1 class="cidades-erro">N??o h?? dados referentes ?? "{item}"</h1>'))
            del item
    names = list(dict.fromkeys(names))
    names = ', '.join(names)
    if len(dfs) >= 2:
        df = pd.concat(dfs.values())
        duplicates = df.duplicated(keep='first')
        df = df[~duplicates]
        flash(Markup(f'<h1 class="cidades">Resultados referentes ?? busca "{names}"</h1>'))
        return df
    elif len(dfs) == 1:
        for v in dfs.values():
            df = v
        flash(Markup(f'<h1 class="cidades">Resultados referentes ?? busca "{names}"</h1>'))
        return df
    else:
        flash(Markup('<h1 class="cidades-erro-total">N??o h?? resultados referentes ?? busca por munic??pio</h1>'))
        return render_template('municipios.html', form=form, min=mini, max=maxi)


def city_filter_all(df, city_request):
    form = Form()
    mini = '2020-01-01'
    maxi = datetime.now().strftime('%Y-%m-%d')
    dict_match = {'??': 'A', '??': 'A', '??': 'A', '??': 'A', '??': 'a', '??': 'a', '??': 'a', '??': 'a',
                  '??': 'E', '??': 'E', '???': 'E', '??': 'E', '??': 'e', '??': 'e', '???': 'e', '??': 'e',
                  '??': 'I', '??': 'I', '??': 'I', '??': 'i', '??': 'i', '??': 'i', '??': 'O', '??': 'O',
                  '??': 'O', '??': 'O', '??': 'o', '??': 'o', '??': 'o', '??': 'o', '??': 'U', '??': 'U',
                  '??': 'U', '??': 'u', '??': 'u', '??': 'u', '??': 'C', '??': 'c'}
    searches = []
    names = []
    vac = pd.read_csv(url4, usecols=['Munic??pio'], dtype={'Munic??pio': 'category'})
    vac = vac.values.tolist()
    vac = list(flatten(vac))
    vac = list(dict.fromkeys(vac))
    dict_accent = {}
    for x in vac:
        transx = regex_match(x, dict_match)
        dict_accent[transx] = x
    if request.method == 'POST':
        if request.form['municipio_field'] != '':
            search = str(request.form.get('municipio_field'))
            searches = search.split(', ')
        else:
            df = df.query("Munic??pio == 'S??o Jos?? dos Campos' | Munic??pio == 'Taubat??' | Munic??pio == 'Jacare??' | "
                          "Munic??pio == 'Lorena' | Munic??pio == 'Pindamonhangaba' | Munic??pio == "
                          "'Caraguatatuba' | Munic??pio == 'Guaratinguet??' | Munic??pio == 'Ca??apava' | Munic??pio == "
                          "'Ubatuba' | Munic??pio == 'S??o Sebasti??o'")
            flash(Markup(f'<h1 class="cidades"> Dados das dez maiores cidades do Vale do Para??ba. Para acessar '
                         f'outras cidades, fa??a uma pesquisa personalizada.</h1>'))
            return df
    else:
        try:
            search = city_request[-1]
            searches = search.split(', ')
            if city_request[-1] == 'dumby':
                df = df.query(
                    "Munic??pio == 'S??o Jos?? dos Campos' | Munic??pio == 'Taubat??' | Munic??pio == 'Jacare??' | Munic??pio "
                    "== 'Lorena' | Munic??pio == 'Pindamonhangaba' | Munic??pio == 'Caraguatatuba' | "
                    "Munic??pio == 'Guaratinguet??' | Munic??pio == 'Ca??apava' | Munic??pio == 'Ubatuba' | Munic??pio == "
                    "'S??o Sebasti??o'")
                flash(Markup(f'<h1 class="cidades"> Dados das dez maiores cidades do Vale do Para??ba. Para acessar '
                             f'outras cidades, fa??a uma pesquisa personalizada.</h1>'))
                return df
        except IndexError:
            df = df.query(
                "Munic??pio == 'S??o Jos?? dos Campos' | Munic??pio == 'Taubat??' | Munic??pio == 'Jacare??' | Munic??pio == "
                "'Lorena' | Munic??pio == 'Pindamonhangaba' | Munic??pio == 'Caraguatatuba' | Munic??pio == "
                "'Guaratinguet??' | Munic??pio == 'Ca??apava' | Munic??pio == 'Ubatuba' | Munic??pio == 'S??o Sebasti??o'")
            flash(Markup(f'<h1 class="cidades"> Dados das dez maiores cidades do Vale do Para??ba. Para acessar '
                         f'outras cidades, fa??a uma pesquisa personalizada.</h1>'))
            return df
    filter = regex_match_list(searches, dict_match)
    filter = regex_change_list(filter, dict_accent)
    dfs = {}
    filter = list(dict.fromkeys(filter))
    for item in filter:
        result = df[df.Munic??pio.str.contains(item, case=False)]
        if result.empty is False:
            dfs[item] = result
            names.append(item.title())
        else:
            flash(Markup(f'<h1 class="cidades-erro">N??o h?? dados referentes ?? "{item}"</h1>'))
            del item
    names = list(dict.fromkeys(names))
    names = ', '.join(names)
    if len(dfs) >= 2:
        df = pd.concat(dfs.values())
        flash(Markup(f'<h1 class="cidades">Resultados referentes ?? busca "{names}"</h1>'))
        return df
    elif len(dfs) == 1:
        for v in dfs.values():
            df = v
        flash(Markup(f'<h1 class="cidades">Resultados referentes ?? busca "{names}"</h1>'))
        return df
    else:
        flash(Markup('<h1 class="cidades-erro-total">N??o h?? resultados referentes ?? busca por munic??pio</h1>'))
        return render_template('municipios.html', form=form, min=mini, max=maxi)


def painel_filter(df, city_request):
    dict_match = {'??': 'A', '??': 'A', '??': 'A', '??': 'A', '??': 'a', '??': 'a', '??': 'a', '??': 'a',
                  '??': 'E', '??': 'E', '???': 'E', '??': 'E', '??': 'e', '??': 'e', '???': 'e', '??': 'e',
                  '??': 'I', '??': 'I', '??': 'I', '??': 'i', '??': 'i', '??': 'i', '??': 'O', '??': 'O',
                  '??': 'O', '??': 'O', '??': 'o', '??': 'o', '??': 'o', '??': 'o', '??': 'U', '??': 'U',
                  '??': 'U', '??': 'u', '??': 'u', '??': 'u', '??': 'C', '??': 'c'}
    searches = []
    names = []
    vac = pd.read_csv(url4, usecols=['Munic??pio'], dtype={'Munic??pio': 'category'})
    vac = vac.values.tolist()
    vac = list(flatten(vac))
    vac = list(dict.fromkeys(vac))
    dict_accent = {}
    for x in vac:
        transx = regex_match(x, dict_match)
        dict_accent[transx] = x
    if request.method == 'POST':
        if request.form['municipio_field'] != '':
            search = str(request.form.get('municipio_field'))
            searches = search.split(', ')
        else:
            df = df.query(
                "Munic??pio == 'S??o Jos?? dos Campos' | Munic??pio == 'Taubat??' | Munic??pio == 'Jacare??' | Munic??pio == "
                "'Lorena' | Munic??pio == 'Pindamonhangaba' | Munic??pio == 'Caraguatatuba' | Munic??pio == "
                "'Guaratinguet??' | Munic??pio == 'Ca??apava' | Munic??pio == 'Ubatuba' | Munic??pio == 'S??o Sebasti??o'")
            return df
    else:
        try:
            search = city_request[-1]
            searches = search.split(', ')
            if city_request[-1] == 'dumby':
                df = df.query(
                    "Munic??pio == 'S??o Jos?? dos Campos' | Munic??pio == 'Taubat??' | Munic??pio == 'Jacare??' | Munic??pio "
                    "== 'Lorena' | Munic??pio == 'Pindamonhangaba' | Munic??pio == 'Caraguatatuba' | "
                    "Munic??pio == 'Guaratinguet??' | Munic??pio == 'Ca??apava' | Munic??pio == 'Ubatuba' | Munic??pio == "
                    "'S??o Sebasti??o'")
                return df
        except IndexError:
            df = df.query(
                "Munic??pio == 'S??o Jos?? dos Campos' | Munic??pio == 'Taubat??' | Munic??pio == 'Jacare??' | Munic??pio == "
                "'Lorena' | Munic??pio == 'Pindamonhangaba' | Munic??pio == 'Caraguatatuba' | Munic??pio == "
                "'Guaratinguet??' | Munic??pio == 'Ca??apava' | Munic??pio == 'Ubatuba' | Munic??pio == 'S??o Sebasti??o'")
            return df
    filter = regex_match_list(searches, dict_match)
    filter = regex_change_list(filter, dict_accent)
    dfs = {}
    filter = list(dict.fromkeys(filter))
    for item in filter:
        result = df[df.Munic??pio.str.contains(item, case=False)]
        if result.empty is False:
            dfs[item] = result
            names.append(item.title())
        else:
            del item
    names = list(dict.fromkeys(names))
    names = ', '.join(names)
    if len(dfs) >= 2:
        df = pd.concat(dfs.values())
        return df
    elif len(dfs) == 1:
        for v in dfs.values():
            df = v
        return df
    else:
        return df