import os, re, json

jsons = os.listdir('data/septiembre')

topico = ['[Dd]ólar blue', '[Tt]ipo de cambio', '[Dd]ólar MEP', 'MEP', '[Cc]ontado con liquidación', 'CCL', '[Bb]recha', '[Dd]ólar ahorro']
regex_topico = '|'.join(topico)
salida = open('data/noticias_sobre_dolar.csv', 'wt')
salida.write('url,diario,seccion,fecha\n')

for path in jsons:
    print('path: ' + path)
    dia = open('data/septiembre/' + path, 'rt')
    for linea in dia.readlines():
        noticia = json.loads(linea)
        titulo_y_texto = noticia['titulo'] + '.' + noticia['texto']
        matcheos = re.findall(regex_topico, titulo_y_texto)
        if len(matcheos) > 3:
            fila = "\"" + noticia['url'] + "\"" + ',' + noticia['diario'] + ',' + noticia['seccion'] + ',' + noticia['fecha']['$date'][:10] + '\n'
            salida.write(fila)
    dia.close()

salida.close()

