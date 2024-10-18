#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 19:05:55 2019

@author: juangabriel
"""

import pandas as pd
from apyori import apriori
import matplotlib.pyplot as plt
import seaborn as sns
import csv

# Cargar el dataset
dataset = pd.read_csv('Market_Basket_Optimisation.csv', header=None)

# Convertir el dataset a una lista de transacciones
transactions = []
for i in range(len(dataset)):
    transaction = [str(item) for item in dataset.values[i] if str(item) != 'nan']
    transactions.append(transaction)

# Aplicar el algoritmo Apriori
rules = apriori(transactions, 
                min_support=0.003, 
                min_confidence=0.2,
                min_lift=3, 
                min_length=2)

# Convertir los resultados a una lista
results = list(rules)

# Inicializar listas para almacenar las reglas y métricas
rules_list = []

for rule in results:
    for stat in rule.ordered_statistics:
        if stat.confidence >= 0.2 and stat.lift >= 3:
            rules_list.append({
                'Base': ', '.join(stat.items_base),
                'Add': ', '.join(stat.items_add),
                'Support': rule.support,
                'Confidence': stat.confidence,
                'Lift': stat.lift
            })

# Crear un DataFrame de las reglas
rules_df = pd.DataFrame(rules_list)

# Ordenar el DataFrame por Lift en orden descendente
rules_sorted = rules_df.sort_values(by='Lift', ascending=False)

# Seleccionar las 12 reglas con mayor Lift
top_12_rules = rules_sorted.head(12)

# Imprimir las 12 reglas en la terminal (Método a: Tabla Completa)
print("Las 12 reglas más importantes basadas en Lift:\n")
print(top_12_rules.to_string(index=False))

print("\n" + "="*40 + "\n")

# Imprimir las 12 reglas en la terminal (Método b: Detallado)
print("Las 12 reglas más importantes basadas en Lift (Formato Detallado):\n")

for index, row in top_12_rules.iterrows():
    print(f"Regla: {row['Base']} -> {row['Add']}")
    print(f"Soporte: {row['Support']:.4f}")
    print(f"Confianza: {row['Confidence']:.2f}")
    print(f"Lift: {row['Lift']:.2f}")
    print("-----------------------------------")

# Visualización de las reglas en un gráfico de barras
sns.set(style="whitegrid")

# Crear etiquetas para las reglas
top_12_rules['Rule'] = top_12_rules['Base'] + " -> " + top_12_rules['Add']

# Crear el gráfico de barras
plt.figure(figsize=(12, 8))
sns.barplot(x='Lift', y='Rule', data=top_12_rules, palette='viridis')

plt.title('Top 12 Reglas de Asociación por Lift', fontsize=16)
plt.xlabel('Lift', fontsize=14)
plt.ylabel('Reglas de Asociación', fontsize=14)
plt.tight_layout()
plt.show()
