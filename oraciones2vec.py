import multiprocessing
from gensim.models import Word2Vec

import datatable
from datatable import dt, f

import dibujos

oraciones = datatable.fread('data/oraciones_20210803.csv')

filtro = ('clarin', 'politica')

i = 0
oraciones_tokenizadas = []
for id_noticia, diario, seccion, fecha, oracion, sustantivos, adjetivos, verbos, personas, organizaciones, lugares in oraciones.to_tuples():
    tokens_con_posicion = []

    if diario != filtro[0] or seccion != filtro[1]:
        continue
    # if ',' in verbos:
    #     tokens.extend(verbos.split(','))

    if len(sustantivos):
        con_pos = [s for s in sustantivos.split(',') if '-' in s] # chequeo q tengan '-'
        tokens_con_posicion.extend(con_pos)

    if len(adjetivos):
        con_pos = [a for a in adjetivos.split(',') if '-' in a] # chequeo q tengan '-'
        tokens_con_posicion.extend(con_pos)

    if len(personas):
        con_pos = [p for p in personas.split(',') if '-' in p] # chequeo q tengan '-'
        tokens_con_posicion.extend(con_pos)

    if len(organizaciones):
        con_pos = [o for o in organizaciones.split(',') if '-' in o] # chequeo q tengan '-'
        tokens_con_posicion.extend(con_pos)

    if len(lugares):
        con_pos = [l for l in lugares.split(',') if '-' in l] # chequeo q tengan '-'
        tokens_con_posicion.extend(con_pos)


    if tokens_con_posicion:
        tokens_con_posicion = [t for t in tokens_con_posicion if t.split('-')[-1].isdigit()] # filtro los que no tienen posición
        try:
            tokens_con_posicion.sort(key=lambda x : int(x.split('-')[-1])) # ordeno según posición
        except RuntimeError:
            print('Error en la linea: ' + str(i))

        tokens = [t.split('-')[0] for t in tokens_con_posicion]
        oraciones_tokenizadas.append(tokens)
    i += 1

cores = multiprocessing.cpu_count()
w2v = Word2Vec(
    min_count=2, # ignora palabras cuya frecuencia es menor a esta
    window=5, # tamanio de la ventana de contexto
    size=300, # dimension del embedding
    sample=6e-5, # umbral para downsamplear palabras muy frecuentes
    alpha=0.03, # tasa de aprendizaje inicial (entrenamiento de la red neuronal)
    min_alpha=0.0007, # tasa de aprendizaje minima
    negative=20, # penalidad de palabras muy frecuentes o poco informativas
    workers=cores
)

w2v.build_vocab(oraciones_tokenizadas, progress_per=10000)

w2v.train(oraciones_tokenizadas, total_examples=w2v.corpus_count, epochs=30, report_delay=1)

w2v.init_sims(replace=True) # precomputa distancias (más rápido)

w2v.wv.most_similar(positive=['Quinta de Olivos'])

palabra = 'test'
while palabra != '':
    palabra = input('Dibujar palabras cercanas de: ')
    if palabra == '':
        continue
    try:
        dibujos.tsnescatterplot(w2v, palabra)
    except KeyError:
        print(palabra + ' no está en el vocabulario.')