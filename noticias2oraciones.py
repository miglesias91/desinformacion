import spacy
from datatable import dt, f

noticias = dt.fread('data/notis_20210803.csv')

nlp = spacy.load('es_core_news_md')

i = 0
textos = noticias[:, 'texto'].to_list()[0]

df = dt.Frame(id_noticia=[], diario=[], seccion=[], fecha=[], oracion=[],
              sustantivos=[], adjetivos=[], verbos=[],
              personas=[], organizaciones=[], lugares=[])

total = str(len(textos))
for texto in textos:

    print(str(i) + ' de ' + total)

    oraciones = list(nlp(texto).sents)

    for oracion in oraciones:

        if len(oracion.text.strip()) is 0:
            continue

        diario = noticias[i,0]
        seccion = noticias[i,1]
        fecha = noticias[i,2][:10]
        titulo = noticias[i,3]

        sustantivos = ','.join([t.lemma_.lower() + '-' + str(t.idx) for t in oracion if t.pos_ == 'NOUN'])
        adjetivos = ','.join([t.lemma_.lower() + '-' + str(t.idx)  for t in oracion if t.pos_ == 'ADJ'])
        verbos = ','.join([t.lemma_.lower() + '-' + str(t.idx)  for t in oracion if t.pos_ == 'VERB'])

        personas = ','.join([e.text + '-' + str(e.start_char) for e in oracion.ents if e.label_ == 'PER'])
        organizaciones = ','.join([e.text + '-' + str(e.start_char)  for e in oracion.ents if e.label_ == 'ORG'])
        lugares = ','.join([e.text + '-' + str(e.start_char)  for e in oracion.ents if e.label_ == 'LOC'])
        # fechas = ','.join([e.text for e in oracion.ents if e.label_ == 'DATE'])
        # geopoliticos = ','.join([e.text for e in oracion.ents if e.label_ == 'GPE'])
        # eventos = ','.join([e.text for e in oracion.ents if e.label_ == 'EVENT'])

        fila = dt.Frame({"id_noticia": [i], "diario": [diario], "seccion": [seccion], "fecha" : [fecha], "oracion" : [oracion.text.strip()],
                         "sustantivos" : [sustantivos], "adjetivos" : [adjetivos], "verbos" : [verbos],
                         "personas" : [personas], "organizaciones" : [organizaciones], "lugares" : [lugares]})

        df.rbind(fila)

    i += 1

df.to_csv('data/oraciones_20210803.csv')

