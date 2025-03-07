---
title: "Cuaderno de problemas"
author: "Serafí Nebot Ginard"
# date: "02/03/2025"
pdf-engine: xelatex
fontfamily: libertinus
# mainfont: Courier
geometry: top=2cm, bottom=1.5cm, left=1.5cm, right=1.5cm
documentclass: article
# numbersections: true
toc: true
---

\pagebreak

# Tema 1

## Problema 1.1

Dos sistemas, A y B, ejecutan el programa SEARCH, pero en el sistema A tiene un tiempo de ejecución de 3 segundos, mientras que en el B son 4 segundos. Si el sistema A cuesta 3.000 € y el sistema B 2.500 € ¿Cuál de los dos sistemas presenta una mejor relación de prestaciones y coste para el programa SEARCH?

## Problema 1.2

Los sistemas del problema 1.1, A y B, cuando ejecutan SEARCH, el sistema A consume una energía de 1000 Ws y el sistema B consume 850 Ws ¿Cuál de los dos sistemas presenta una mejor relación de energía y rendimiento?

## Problema 1.3

Dos sistemas, A y B, ejecutan el programa KICK, pero el sistema A tiene un tiempo de ejecución de 4 segundos, mientras que en el B son 5 segundos. Si el sistema A consume una energía de 1200 Ws y el sistema B consume 950 Ws, se solicitan las siguientes métricas:

* Calcular el EDP de ambos sistemas.
* Calcular la aceleración de un sistema sobre el otro.
* Calcular el incremento de energía consumida de un sistema sobre el otro.
* ¿Cómo se podría establecer un índice coherente que relacionase la aceleración y el incremento de energía consumida, donde uno de los sistemas es el patrón de comparación?

## Problema 1.4

La utilización del procesador Xeon en un servidor es del 85%. Se pide calcular la mejora de rendimiento que se conseguiría, si éste se sustituye por otro modelo nuevo el doble de rápido. 

## Problema 1.5

Se quiere mejorar el rendimiento del servidor RELATIVITY mediante el cambio de su unidad de disco. Esta unidad de disco mejora la velocidad el doble en los accesos de E/S. Sabiendo que las aplicaciones que se ejecutan en ese servidor usan el disco un 50%, si las aplicaciones que se ejecutan en RELATIVITY tardan con el disco antiguo 3 segundos ¿cuánto tiempo tardarán con la unidad de disco nueva? 

## Problema 1.6

En el centro de datos (datacenter) de la Universidad Central del Colorado (UCeCo) se quiere cambiar el sistema de discos RAID por uno 10 veces más rápido con las mismas características funcionales que el actual. ¿Cuánto debería usarse el nuevo sistema para que las aplicaciones típicas de la UCeCo, que se ejecutan en el centro de datos y usan el sistema de discos, aceleren el triple? ¿Y para que el sistema acelere 8 veces?

## Problema 1.7

El servidor HAL con 48 procesadores ejecuta programas con una media de paralelismo del 80%. ¿Cuál es la aceleración calculada con la ley de Gustafson? Si el paralelismo baja al 60% ¿cuál es la aceleración ahora? Si quisiéramos calcular la aceleración con la ley de Amdahl ¿qué valor resultaría? ¿Cuál es el límite de la aceleración con la ley de Amdahl? 

## Problema 1.8

El gestor de la base de datos MyOracle de la empresa hotelera ENJOY recibe transacciones provenientes de su sistema de reservas interno. Cada transacción tiene un tiempo de respuesta de 1,3 segundos. Al monitorizar el uso que los programas de reserva hacen de la base de datos se ha concluido que el 60% del tiempo de respuesta de cada transacción es debido al acceso a E/S, mientras que el resto es debido al procesamiento y la memoria. El proveedor tecnológico DiskisOK le ofrece dos opciones de substitución de la E/S, una es doble de rápida pero cuesta 14.000 € y la otra es el triple de rápida pero cuesta 23.000 €. Se pide:

*  Calcular el tiempo de ambas opciones.
*  Calcular las mejoras de rendimiento sobre el sistema de E/S actual de ambas opciones.
*  Calcular la relación de coste y rendimiento de las nuevas opciones de E/S.
*  Si el sistema de E/S original costó 10.000 €, pero una vez amortizado hasta hoy valdría 8.000 €. ¿Cuánto es el incremento real de la sustitución y su efecto en el rendimiento/coste?
* Como a ENJOY le parecen ambos sistemas de DiskisOK muy caros, sólo quiere cambiar unos discos del sistema de E/S de la marca IOWorld que valen 1000€ y mantener el sistema actual a costa de mejorar solo un 5 % la aceleración ¿Cuál la nueva relación de rendimiento y coste de esta rebaja? 

## Problema 1.9

El 80% de las tareas de un programa se pueden paralelizar en distintos procesadores. Si el programa se ejecuta en 5 segundos, se pide calcular:

* La aceleración que experimenta el tiempo de ejecución del programa en un multiprocesador de 32 procesadores aplicando la ley de Amdahl y la ley de Gustafson.
* El tiempo que tardaría en ejecutarse con ese paralelismo con ambas leyes. 

## Problema 1.10

El tiempo de respuesta de una transacción web es de 2,5 segundos y el 70% de ese tiempo se usa para acceder al disco local del servidor web. Si el coste del disco es 300 €, ¿cuánto debe mejorar la velocidad del disco para que el tiempo de respuesta de una transacción sea la mitad? Si el precio del disco nuevo es de 600€ ¿se podría decir que compensa adquirirlo considerando el rendimiento esperado y el coste? 


## Problema 1.11

Se quiere mejorar el rendimiento del servidor RELATIVITY2 mediante el cambio de su unidad de disco. Esta unidad de disco mejora la velocidad en los accesos de E/S el triple. Calcula el tiempo que se mejora sabiendo que las aplicaciones que se ejecutan en ese servidor tras la mejora, ahora usan el disco un 50% del tiempo. Si las aplicaciones que se ejecutan en RELATIVITY2 tardaban con el disco antiguo 3,5 segundos, ¿cuánto tiempo tardarán con la unidad de disco nueva? ¿Cuál es la aceleración global del servidor RELATIVITY2? 


# Tema 2

## Problema 2.1

Considérese un sistema informático en el que la activación de un monitor software implica la ejecución de un total de 150.000 instrucciones máquina. Si el procesador del sistema tiene una velocidad de ejecución de 750 MIPS (milion of instructions per second), se pide:

1. Calcular el valor que ha de tener el periodo de muestreo si se quiere una sobrecarga (overhead) del 5%.

2. Calcular el número de muestras que se tomarán en un periodo de medida de dos horas.

## Problema 2.2

Un sistema informático que trabaja en el sistema operativo Linux tiene instalado el monitor de actividad sar (system activity reporter). Este monitor se activa cada 20 minutos y tarda 450 milisegundos en ejecutarse por cada activación. En cada una de las activaciones se recoge información del sistema, se construye un registro de datos con esta información, y se añade al fichero histórico saDD del día DD correspondiente. Se pide:

1. Calcular la sobrecarga (overhead) que genera este programa sobre el sistema informático.
2. Determinar el tamaño del directorio /var/log/sa a lo largo de dos semanas si el registro de datos generado por cada activación ocupa 3KB.
3. Si el volumen máximo del directorio /var/log/sa es de 150 MB, ¿cuántos ficheros históricos saDD se pueden almacenar?
4. En dos años, ¿se desbordaría el tamaño del directorio? ¿Cuánta capacidad nos faltaría?

# Tema 3

## Problema 3.1

El rendimiento de un sistema informático bajo la ejecución del benchmark Linpack varía de acuerdo a las diferentes configuraciones del mismo. Para tres tamaños de carga (40000, 60000 y 80000 ecuaciones diferenciales), la generación de resultados del benchmark se distribuye de acuerdo con los siguientes GFLOPS:

| Carga | Porcentaje de Carga | GFLOPS |
|-------|---------------------|--------|
| 40000 | 25%                 | 2      |
| 60000 | 25%                 | 4.5    |
| 80000 | 50%                 | 6      |

Calcúlese el valor medio de los GFLOPS obtenidos por el benchmark.

---

Al ser GFLOPS, Calculemos la media armónica:

$$
\overline{GFLOPS} = \frac{1}{\sum\limits_{i=1}^{n}\frac{w_i}{x_i}} =
\frac{1}{\frac{0.25}{2}+\frac{0.25}{4.5}+\frac{0.5}{6}} = 3.789473 \textrm{ GFLOPS}
$$

dónde $x_i$ es el valor en GFLOPS y $w_i$ el peso (en este caso, el porcentaje de la carga) de tal forma que $\sum\limits_{i = 1}^{n}w_i = 1$

---

## Problema 3.2

Un estudio llevado a cabo mediante un monitor de ejecución de programas ha permitido cuantificar el tiempo medio de ejecución de las instrucciones que emplea un benchmark. Este benchmark se ha ejecutado en dos procesadores de la familia Intel, i5 y i7, con el mismo juego de instrucciones y se ha obtenido el siguiente resultado:

| Tipo de instrucción | Frecuencia de uso | Tiempo en i5 | Tiempo en i7 |
|---------------------|-------------------|--------------|--------------|
| Memoria             | 10%               | 6.5 ns       | 6,1 ns       |
| Comparación         | 35%               | 1,4 ns       | 0,7 ns       |
| Salto               | 5%                | 8,6 ns       | 7,9 ns       |
| Otras               | 50%               | 2,7 ns       | 1,9 ns       |

Se pide:

1. Calcular el tiempo medio de ejecución de una instrucción en cada procesador y utilizarlos para cuantificar la mejora conseguida por el procesador más rápido.

Para calcular el timepo medio de cada instrucción se hace la media aritmética ponderada de cada tipo de instrucción.

Tiempo en i5:

$$
T_{i5} = 6.5\cdot 0.1 + 1.4\cdot0.35 + 8.6\cdot0.05 + 2.7\cdot0.5 = 2.92 \textrm{ ns}
$$

Tiempo en i7:

$$
T_{i7} = 6.1\cdot0.1 + 0.7\cdot0.35 + 7.9\cdot0.05 + 1.9\cdot0.5 = 2.2 \textrm{ ns}
$$

2. Determinar el nuevo tiempo medio de ejecución de una instrucción en el procesador Intel i5 si un nuevo diseño consigue que todas las instrucciones se ejecuten un 15% más rápidamente. 

$$
\frac{T_{i5}}{T_{mej}} = \frac{2.92}{1.15} = 2.539130 \textrm{ ns}
$$

## Problema 3.3

Considérese un programa de cálculo numérico que se ejecuta en 83 segundos y hace las operaciones de coma flotante que se indican a continuación, así como las operaciones normalizadas equivalentes.

| Operación | Cantidad      | Operaciones normalizadas |
|-----------|---------------|--------------------------|
| ADD       | $78\cdot10^9$ | 1                        |
| SQRT      | $29\cdot10^9$ | 3                        |
| COS       | $13\cdot10^9$ | 8                        |
| EXP       | $42\cdot10^9$ | 12                       |

¿Cuál es el rendimiento conseguido por el sistema con este programa de cálculo atendiendo a los GFLOPS? ¿Y si se mide en GFLOPS normalizados? 

## Problema 3.4

Un servidor dispone de un procesador con un reloj que trabaja a 3,2 GHz. Este procesador estructura su juego de instrucciones en tres categorías: simples, normales y complejas. El número medio de ciclos por instrucción (CPI) para cada categoría se indica en la siguiente tabla.

| Tipo     | CPI  | Versión 1                    | Versión 2                    |
|----------|------|------------------------------|------------------------------|
| Simple   | 1    | $9\cdot10^6$ instrucciones   | $11\cdot10^6$ instrucciones  |
| Normal   | 3    | $1.5\cdot10^6$ instrucciones | $2.5\cdot10^6$ instrucciones |
| Compleja | 5    | $2\cdot10^6$ instrucciones   | $1.5\cdot10^6$ instrucciones |

El servidor anterior se está utilizando para comparar el rendimiento de dos versiones de un compilador, V1 y V2. El número de instrucciones de cada categoría ejecutadas por un programa de prueba compilado con ambas versiones se indica también en la tabla anterior. Se pide calcular, para las dos versiones del compilador, el CPI medio y los MIPS conseguidos por el programa. 

Versión 1:

$$
\frac{1\cdot9\cdot10^6 + 3\cdot1.5\cdot10^6 + 5\cdot2\cdot10^6}{9\cdot10^6 + 1.5\cdot10^6 + 2\cdot10^6} = 1.9
$$

## Problema 3.5

Un programa ejecuta un total de $186\cdot10^8$ instrucciones. De ellas, el 75% se ejecutan en 3 ciclos de reloj, mientras que el resto lo hace en 5 ciclos de reloj. Tras haber medido el tiempo de ejecución de dicho programa a través del monitor time se ha obtenido la siguiente información:

```
real 0m57s
user 0m23s
sys 0m1.2s
```

Se pide calcular el número medio de ciclos por instrucción (CPI) obtenidos por el programa, la frecuencia del procesador y los MIPS.

## Problema 3.6

En la siguiente tabla se muestran los tiempos de ejecución (en segundos) de seis configuraciones diferentes del benchmark Linpack en tres sistemas distintos, A, B y C. Se pide comparar el rendimiento de estos tres sistemas utilizando la media aritmética y la media geométrica de los tiempos de ejecución. ¿El orden de rendimiento obtenido con las dos medias coincide? ¿Los valores normalizados de la media (con ambas medias) del tiempo de ejecución a cada una de las tres máquinas guarda la proporcionalidad con el valor suma de tiempos de ejecución?

| Programa  | Sistema A | Sistema B | Sistema C |
|-----------|-----------|-----------|-----------|
| Linpack 1 | 128       | 534       | 512.1     |
| Linpack 2 | 68.7      | 56        | 26        |
| Linpack 3 | 352       | 478       | 698       |
| Linpack 4 | 82.4      | 96        | 91        |
| Linpack 5 | 893.1     | 3654      | 4789      |
| Linpack 6 | 178.5     | 167       | 324       |
