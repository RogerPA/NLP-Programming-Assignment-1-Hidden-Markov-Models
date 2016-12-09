GUIA DE USO

Parte 1:

1. Reemplazar las palabras poco frecuentes con se creara el archivo gene_rare.train:
    
    python replace_rare_words.py

2. Generar el conteo con el archivo genereado:
    
    python count_freqs.py gene_rare.train > gene.counts

3. Etiquetar las palabras del dev:
    
    python simple_gen_tagger.py gene.counts gene.dev > gene_dev.p1.out

4. Comprobar:
    
    python eval_gene_tagger.py gene.key gene_dev.p1.out

    Outputs:
    Found 2669 GENEs. Expected 642 GENEs; Correct: 424.

            precision  recall      F1-Score
    GENE:   0.158861   0.660436    0.256116

5. Etiquetar las palabras del test:
    
    python simple_gen_tagger.py gene.counts gene.test > gene_test.p1.out

Parte 2:
1. Reemplazar las palabras poco frecuentes con se creara el archivo gene_rare.train:
    
    python replace_rare_words.py

2. Generar el conteo con el archivo genereado:
    
    python count_freqs.py gene_rare.train > gene.counts

3. Etiquetar las palabras del dev.
Modificar los archivos de entrada y salida lineas 165, 166 y 167
(file_name_counts = "gene.counts"
file_name_test = "gene.dev"
file_name_output = "gene_dev.p2.out")
y descomentar la linea 55 ( words_filter = [] ):
    
    python viterbi_gen_tagger.py

4. Comprobar:
    
    python eval_gene_tagger.py gene.key gene_dev.p2.out

    Outputs:

    Found 373 GENEs. Expected 642 GENEs; Correct: 202.

            precision  recall      F1-Score
    GENE:   0.541555   0.314642    0.398030

5. Etiquetar las palabras del test.
Modificar los archivos de entrada y salida lineas 165, 166 y 167
(file_name_counts = "gene.counts"
file_name_test = "gene.test"
file_name_output = "gene_test.p2.out")
y descomentar la linea 55 ( words_filter = [] ):
    
    python simple_gen_tagger.py gene.counts gene.test > gene_test.p2.out


Parte 3:

1. Reemplazar las palabras poco frecuentes con informacion con se creara el archivo gene_info_rare.train:
    
    python replace_rare_words.py

2. Generar el conteo con el archivo genereado:
    
    python count_freqs.py gene_info_rare.train > gene.counts

3. Etiquetar las palabras del dev.
Modificar los archivos de entrada y salida lineas 165, 166 y 167
(file_name_counts = "gene.counts"
file_name_test = "gene.dev"
file_name_output = "gene_dev.p3.out")
y comentar la linea 55 ( #words_filter = [] ):
    
    python viterbi_gen_tagger.py

4. Comprobar:
    
    python eval_gene_tagger.py gene.key gene_dev.p2.out

    Outputs:

    Found 415 GENEs. Expected 642 GENEs; Correct: 222.

            precision  recall      F1-Score
    GENE:   0.534940   0.345794    0.420057

5. Etiquetar las palabras del test.
Modificar los archivos de entrada y salida lineas 165, 166 y 167
(file_name_counts = "gene.counts"
file_name_test = "gene.test"
file_name_output = "gene_test.p3.out")
y comentar la linea 55 ( #words_filter = [] ):
    
    python simple_gen_tagger.py gene.counts gene.test > gene_test.p2.out