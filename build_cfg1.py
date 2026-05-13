import ast
import networkx as nx

# 1. Завантаження коду функції
with open("auth.py", "r") as f:
    code = f.read()

tree = ast.parse(code)
func = tree.body[0]  # Функція authenticate_user

G = nx.DiGraph()

# 2. Визначення вузлів (Блоки рішень та дії)
nodes = {
    "n0": "if not username or not password",
    "n1": "if username not in db",
    "n2": "attempts = db[username].get('attempts', 0)",
    "n3": "if attempts >= 3",
    "n4": "if db[username]['password'] != password",
    "n5": "db[username]['attempts'] = 0",
    "ret_miss": "return 'Missing credentials'",
    "ret_nf": "return 'User not found'",
    "ret_lock": "return 'Account locked'",
    "ret_inv": "return 'Invalid password'",
    "ret_auth": "return 'Authenticated'"
}

for node_id, label in nodes.items():
    G.add_node(node_id, label=label)

# 3. Додавання ребер (Логіка розгалуження)
# n0 (credentials check)
G.add_edge("n0", "ret_miss")  # True
G.add_edge("n0", "n1")        # False

# n1 (user check)
G.add_edge("n1", "ret_nf")    # True
G.add_edge("n1", "n2")        # False

# n2 -> n3 (послідовно)
G.add_edge("n2", "n3")

# n3 (attempts check)
G.add_edge("n3", "ret_lock")  # True
G.add_edge("n3", "n4")        # False

# n4 (password check)
G.add_edge("n4", "ret_inv")   # True
G.add_edge("n4", "n5")        # False

# n5 -> ret_auth (послідовно)
G.add_edge("n5", "ret_auth")

# 4. Пошук усіх шляхів виконання
exit_nodes = ["ret_miss", "ret_nf", "ret_lock", "ret_inv", "ret_auth"]
all_paths = []

for target in exit_nodes:
    paths = list(nx.all_simple_paths(G, source="n0", target=target))
    all_paths.extend(paths)

print("--- Шляхи виконання (all_simple_paths) ---")
for i, path in enumerate(all_paths, 1):
    print(f"Шлях {i}: {path}")

# 5. Коректний розрахунок цикломатичної складності
# Для графів з багатьма виходами: M = E - N + (L + 1)
# Де L - кількість вузлів return (вихідних точок)
E = G.number_of_edges()
N = G.number_of_nodes()
L = len(exit_nodes)
M = E - N + (L + 1)

print(f"\nСтатистика графа:")
print(f"Кількість ребер (E): {E}")
print(f"Кількість вузлів (N): {N}")
print(f"Кількість виходів (L): {L}")
print(f"Цикломатична складність (M): {M}")

# 6. Експорт у DOT для візуалізації
nx.nx_pydot.write_dot(G, "cfg1.dot")