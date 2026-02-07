import csv
from difflib import SequenceMatcher
from collections import defaultdict

# Nome do arquivo de entrada
arquivo_entrada = 'nomes_unicos.csv'

# Função para calcular similaridade
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Ler os nomes
nomes = []
with open(arquivo_entrada, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Pular cabeçalho
    for row in reader:
        nomes.append(row[0])

# Encontrar possíveis duplicatas (similaridade > 0.8)
possiveis_duplicatas = []
for i in range(len(nomes)):
    for j in range(i+1, len(nomes)):
        if similar(nomes[i], nomes[j]) > 0.8:
            possiveis_duplicatas.append((nomes[i], nomes[j]))

# Imprimir possíveis duplicatas
if possiveis_duplicatas:
    print("Possíveis duplicatas encontradas:")
    for par in possiveis_duplicatas:
        print(f"{par[0]} <-> {par[1]}")
else:
    print("Nenhuma duplicata aproximada encontrada.")

# Agora, corrigir as duplicatas agrupando nomes similares
# Criar grafo de similaridade
graph = defaultdict(list)
for a, b in possiveis_duplicatas:
    graph[a].append(b)
    graph[b].append(a)

# Encontrar componentes conectados (grupos de nomes similares)
visited = set()
components = []
for name in nomes:
    if name not in visited:
        component = []
        stack = [name]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                component.append(current)
                stack.extend(graph[current])
        components.append(component)

# Para cada componente, escolher o nome com mais palavras (mais completo)
cleaned_names = []
corrections = []
for comp in components:
    if len(comp) == 1:
        cleaned_names.append(comp[0])
    else:
        # Escolher o nome com mais palavras
        best = max(comp, key=lambda x: len(x.split()))
        cleaned_names.append(best)
        corrections.append((comp, best))

# Imprimir correções feitas
if corrections:
    print("\nCorreções aplicadas:")
    for comp, best in corrections:
        print(f"Grupo: {comp} -> Mantido: {best}")

# Salvar nomes corrigidos em um novo arquivo
with open('nomes_corrigidos.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Nome'])
    for name in cleaned_names:
        writer.writerow([name])

print(f"\nNomes únicos salvos em 'nomes_corrigidos.csv'. Total: {len(cleaned_names)}")
