# Anotações

- Act2Vec e montar os traces "na mão" ou utilizar Trace2Vec
- Como testar? Devo criar um processo com labels para atestar resultados? 
(apesar de que os processos são verificaveis para saber se são anomalos)
- Comportamento estranho ao pegar os vetores do Trace2Vec (ou, efetivamente, de um Doc2Vec).
Ao treinar, ele splita o dataset no meio entre anomalos e normais
- OCSVM provavelmente não está dando bons resultados.
Metade dos anomalos gerados ficaram para cada classe
- Supervisionado mostra um comportamento interessante.
Acerta com muita precisão anomalias que envolvem skip ou insert, e não acerta nada com permutação de atividades.
O resultado é esperado, na verdade, com o jeito que estão sendo feitos os vetores, não se importando com a ordem das atividades e só somando.
(2019-02-08)

## Próximos passos
- [x] ~~Testar o word2vec na mão, é só isso que fizeram no act2vec.~~
- [x] ~~Não utilizar XES, importar os csvs que eu fiz.~~
- [] Criar uma base de teste? Nào foi feito, talvez não seja feito
- [] Testar mais parâmetros do Word2Vec, talvez usar o Doc2Vec
- [] Testar mais parâmetros da OCSVM, mas acho que os dados não estão bem separados
- [x] Testar supervisionado e comparar os resultados
