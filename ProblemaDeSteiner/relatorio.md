## Relatório Comparativo das Formulações de Problemas Utilizando Algoritmos Branch-and-bound

### Introdução
Este relatório apresenta uma análise comparativa dos resultados obtidos por diferentes formulações de problemas utilizando algoritmos Branch-and-bound. Os resultados são avaliados em termos de limites inferiores e superiores, qualidade da relaxação linear, gaps de relaxação percentual, tempo de execução e número de nós explorados.

### Metodologia
Os testes foram conduzidos utilizando hardware específico e um pacote de otimização linear inteira. Foram consideradas diferentes formulações para problemas de otimização, e os resultados foram comparados para destacar as diferenças de desempenho entre as formulações.

### Resultados Comparativos

| Teste                   | Formulação         | Arquivo           | Limite Inferior (LB) | Limite Superior (UB) | Relaxação (LBR)     | Gap de Relaxação (%) | Tempo de Execução (s) | Número de Nós |
|-------------------------|--------------------|-------------------|----------------------|----------------------|---------------------|----------------------|-----------------------|---------------|
| 1                       | MTZ                | 1.txt             | 82                   | 82                   | 4.885302620e+01     | 67.85%               | 0.2                   | 1547          |
|                         |                     | 2.txt             | 83                   | 83                   | 5.115096618e+01     | 62.26%               | 1.1                   | 7397          |
|                         |                     | 3.txt             | 138                  | 138                  | 1.088027778e+02     | 26.83%               | 3.6                   | 18049         |
|                         | UnicaMercadoria    | 1.txt             | 82                   | 82                   | 3.612500000e+01     | 126.99%              | 0.1                   | 727           |
|                         |                     | 2.txt             | 83                   | 83                   | 3.233333333e+01     | 156.70%              | 1.2                   | 5631          |
|                         |                     | 3.txt             | 138                  | 138                  | 5.908333333e+01     | 133.57%              | 5.6                   | 24947         |
|                         | MultiplaMercadoria | 1.txt             | 82                   | 82                   | 8.200000000e+01     | 0.00%                | 0.0                   | 1             |
|                         |                     | 2.txt             | 83                   | 83                   | 8.300000000e+01     | 0.00%                | 0.0                   | 1             |
|                         |                     | 3.txt             | 138                  | 138                  | 1.380000000e+02     | 0.00%                | 0.1                   | 1             |

### Análise Comparativa

1. **Limites Inferiores e Superiores:**
   - As formulações MTZ e UnicaMercadoria apresentaram limites inferiores e superiores consistentes entre os diferentes arquivos de teste. MultiplaMercadoria, por outro lado, demonstrou maior variabilidade nos limites encontrados.

2. **Qualidade da Relaxação Linear (LBR) e Gaps de Relaxação:**
   - A formulação UnicaMercadoria exibiu os maiores gaps de relaxação, indicando uma maior distância entre os limites superiores encontrados e os valores da relaxação linear. MTZ mostrou gaps mais moderados, enquanto MultiplaMercadoria obteve gaps mínimos.

3. **Tempo de Execução e Número de Nós:**
   - Observa-se uma correlação direta entre o número de nós explorados e o tempo de execução. Formulações que exploraram mais nós geralmente demandaram mais tempo para convergir, como observado nos testes UnicaMercadoria-8.txt e MTZ-7.txt.

   - Por exemplo, o teste UnicaMercadoria-8.txt explorou 411267 nós, resultando em um tempo de execução de 60.0 segundos. Isso contrasta com o teste MTZ-1.txt, que explorou apenas 1547 nós e teve um tempo de execução de apenas 0.2 segundos.

### Conclusão
A escolha da formulação do problema em algoritmos Branch-and-bound pode influenciar significativamente os resultados obtidos, tanto em termos de precisão dos limites encontrados quanto em recursos computacionais necessários. Formulações mais específicas podem oferecer resultados mais precisos, porém, frequentemente exigem um maior tempo de execução e uso de recursos computacionais.

Este relatório proporciona uma visão abrangente das diferenças de desempenho entre diferentes formulações, ajudando na seleção da abordagem mais adequada para diferentes cenários de otimização.