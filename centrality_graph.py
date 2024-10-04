# import json
# import numpy as np
# from scipy.sparse import csr_matrix
# import networkx as nx
#
# # Загрузка данных из JSON файла
# with open('friends_data.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)
#
# # Создание множества уникальных вершин
# a_set = set()
# for key, values in data.items():
#     a_set.add(int(key))
#     for value in values:
#         a_set.add(value)
#
# # Создание индекса для вершин
# vertex_index = {vertex: index for index, vertex in enumerate(sorted(a_set))}
#
# row_indices = []
# col_indices = []
#
# # Заполнение списков индексов для рёбер
# for vertex, connections in data.items():
#     for connection in connections:
#         row_indices.append(vertex_index[int(vertex)])
#         col_indices.append(vertex_index[connection])
#
# # Создание разреженной матрицы смежности
# adjacency_matrix = csr_matrix((np.ones(len(row_indices)), (row_indices, col_indices)), shape=(len(a_set), len(a_set)))
#
# # Создание графа из разреженной матрицы смежности
# G = nx.from_scipy_sparse_array(adjacency_matrix)
#
# # Заданные ID для анализа
# target_ids = [
#     290530655, 1931147, 207227130, 253340861,
#     138042735, 172244589, 168420440, 711398942,
#     65657314, 50933461, 198216820, 268235974
# ]
#
# # Вычисление центральности по посредничеству
# betweenness = nx.betweenness_centrality(G)
# print("Центральность по посредничеству:")
# for node in target_ids:
#     print(f'Узел: {node}, Центральность по посредничеству: {betweenness.get(node, 0)}')
#
# # Вычисление центральности по близости
# closeness = nx.closeness_centrality(G)
# print("\nЦентральность по близости:")
# for node in target_ids:
#     print(f'Узел: {node}, Центральность по близости: {closeness.get(node, 0)}')
#
# # Вычисление центральности по собственному вектору
# eigenvector = nx.eigenvector_centrality(G)
# print("\nЦентральность по собственному вектору:")
# for node in target_ids:
#     print(f'Узел: {node}, Центральность по собственному вектору: {eigenvector.get(node, 0)}')
import json
import cudf
import cugraph

# Загрузка данных из JSON файла
with open('friends_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Подготовка данных для CuGraph
edges = []
for key, values in data.items():
    for value in values:
        edges.append((int(key), value))

# Создание DataFrame для рёбер
edges_df = cudf.DataFrame(edges, columns=['source', 'target'])

# Создание графа из DataFrame
G = cugraph.Graph()
G.from_cudf_edgelist(edges_df)

# Заданные ID для анализа
target_ids = [
    290530655, 1931147, 207227130, 253340861,
    138042735, 172244589, 168420440, 711398942,
    65657314, 50933461, 198216820, 268235974
]

# Вычисление центральности по посредничеству
betweenness = cugraph.betweenness_centrality(G)
print("Центральность по посредничеству:")
for node in target_ids:
    print(f'Узел: {node}, Центральность по посредничеству: {betweenness[betweenness["vertex"] == node]["betweenness_centrality"].values[0] if node in betweenness["vertex"].values else 0}')

# Вычисление центральности по близости
closeness = cugraph.closeness_centrality(G)
print("\nЦентральность по близости:")
for node in target_ids:
    print(f'Узел: {node}, Центральность по близости: {closeness[closeness["vertex"] == node]["closeness_centrality"].values[0] if node in closeness["vertex"].values else 0}')

# Вычисление центральности по собственному вектору
eigenvector = cugraph.eigenvector_centrality(G)
print("\nЦентральность по собственному вектору:")
for node in target_ids:
    print(f'Узел: {node}, Центральность по собственному вектору: {eigenvector[eigenvector["vertex"] == node]["eigenvector_centrality"].values[0] if node in eigenvector["vertex"].values else 0}')