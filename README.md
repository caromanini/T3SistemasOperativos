# Protocolo de capa de aplicación para resolver cuestionarios

Integrantes: Camila Hinojosa y Chiara Romanini.

Este proyecto corresponde a un protocolo de capa de aplicación, que permite crear y desarrollar pruebas en línea. A continuación se presentan las distintas funcionalidades:


## Identificación
Una vez que la conexión sea establecida entre el cliente y el servidor (instrucciones en RUN.md), el programa pedirá al usuario identificarse. Para esto, se tiene que ingresar un mail @miuandes.cl. Ej:


```
Enter username (@miuandes.cl): username@miuandes.cl 
```

## Opciones 
Después de que la identificación sea exitosa, el programa mostrará una serie de opciones. Para elegir una de estas, se tiene que ingresar el número de la opción (1, 2 o 3):

```
Options:
1. Create test
2. Take test
3. Exit
```

1. __Create test__: Este comando deja al usuario crear una prueba. El programa pedirá: 
    - El nombre de la prueba
    - El tiempo limite de la prueba, en minutos (Ejemplo: para ingresar 5 minutos hay que escribir 5)
    - La cantidad de preguntas: Después de ingresar la cantidad de preguntas, el programa pedirá:
        - La pregunta
        - Opciones de la pregunta: Se permite ingresar cuatro opciones
        - Respuesta de la pregunta (Ingresar A, B, C o D) 


```
Antes de escribir la opción, también hay que escribir la letra de la opción. 
Ejemplo:
Enter option A for question 1: <A. opcion 1>
```

2. __Take test__: Muestra y deja escoger una de las pruebas disponibles. Para comenzar una de estas, hay que ingresar el número que le corresponde (1, 2, 3, etc.)
  
    - Antes de cada pregunta, se presentará el tiempo restante para responder la prueba completa. 
    - Una vez que se responde una pregunta, no se puede volver atrás.
    - El puntaje total será mostrado una vez que la prueba se termine. 

```
Ejemplo de formato de pregunta: 

Time remaining: 0:01:53
1. Question 1
A. Option A
B. Option B
C. Option C
D. Option D
Your answer: Ingresar A, B, C o D
```

3. __Exit__: Opción que termina la conexión del cliente con el servidor.