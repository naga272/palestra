import sys
import re


'''
struttura
db = {
    <tabella1>: [
        # lista dict (rappresenta ogni tupla)
        {
            <proprieta1>: <value>,
            <proprieta2>: <value>,
            <proprieta3>: <value>,
        },
        {
            <proprieta1>: <value>,
            <proprieta2>: <value>,
            <proprieta3>: <value>,
        }
    ],
    <tabella2>: [
        {
            <proprieta1>: <value>,
            <proprieta2>: <value>,
            <proprieta3>: <value>,
        }
    ],
    ...
}

La hash table principale spiegherebbe anche perche'
genera errore in caso di tabelle con lo stesso nome
'''


db = {
    "Citta": []
}


struct_name = r"[a-zA-Z_][\w_]*"


def get_table_name(query: str):
    pattern = rf"insert\s+into\s+({struct_name})\s*\(([^)]+)\)"

    match = re.search(pattern, query, re.IGNORECASE)
    if not match:
        print("error insert key")
        sys.exit(1)

    table = match.group(1)
    columns = [c.strip() for c in match.group(2).split(",")]
    return table, columns


def get_values(query):
    values_pattern = r"values\s*\(([^)]+)\)"
    val_match = re.search(values_pattern, query, re.IGNORECASE)

    if not val_match:
        print("error match values")

    raw_values = [
        v.strip() for v in val_match.group(1).split(",")
    ]

    values = [v.strip("'\"") for v in raw_values]

    return values


def main() -> int:
    query = open("./file.sql", "r").read()

    name_table, list_param = get_table_name(query)
    valori = get_values(query)

    if name_table not in db.keys():
        print(f"error! tabella {name_table} inesistente")

    db[name_table] = []

    for i, element in enumerate(list_param):
        db[name_table].append({
            str(element): valori[i]
        })

    # stampo lo stato finale
    print(db)
    return 0


if __name__ == "__main__":
    res = main()
    print("programma terminato con valore", res)
    sys.exit(res)
