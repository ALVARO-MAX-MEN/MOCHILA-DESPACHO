# MOCHILA-DESPACHO

Solucion al **problema de la mochila 0/1** aplicado a la optimizacion de seleccion de productos para despacho logistico, resuelto mediante **programacion dinamica** (enfoque bottom-up).

## Descripcion

Dado un conjunto de productos con peso y valor, y un vehiculo con capacidad maxima de carga, el algoritmo determina el subconjunto de productos que maximiza el valor total transportado sin exceder la capacidad.

## Contenido

 `knapsack_mochila_EF_dp.py`: implementacion de tres estrategias (programacion dinamica, fuerza bruta y algoritmo voraz), caso de prueba y analisis empirico de tiempos de ejecucion.

## Resultado principal

Con un caso de prueba de 5 lotes de productos y capacidad de 50 kg, la programacion dinamica obtuvo el valor optimo de **S/. 220** (seleccionando Lote B y Lote C), igual al resultado de fuerza bruta y superior al 88.6% alcanzado por el algoritmo voraz.

## Como ejecutar

```bash
python knapsack_mochila_EF_dp.py
```

Requiere Python 3 y la libreria matplotlib
o tambien puedes copiar y pegar en Colaboratory
## Autores
Johann Sifuentes Alvaro;
Andres Garcia Valverde;
Fabian Maguiña Nuñez; 
Carlos Pinedo Vasquez;
Christopher Reyes Rojas;

Curso: Analisis de Algoritmos y Estrategias de Programacion — UPN 2026-1
