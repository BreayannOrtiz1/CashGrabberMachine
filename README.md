# Proyecto de Control de Dispositivo con Máquina de Estados

Este proyecto implementa una máquina de estados para controlar un dispositivo con un sistema de cuenta regresiva, turbina, extractor y luz. A continuación se detalla la funcionalidad del código.

---

## 1. Variables Globales

- **`countdownValue`**: Valor de cuenta regresiva por defecto, establecido en 31.
- **`running`**: Indicador booleano para saber si la cuenta regresiva está activa.
- **`sleep_time`**: Tiempo de espera (en milisegundos) entre cambios de estado.
- **`debugTime`**: Valor de tiempo usado para propósitos de depuración.

---

## 2. Asignación de Pines

- **`displayUnidadesPins`**: Pines para el display de unidades.
- **`displayDecenasPins`**: Pines para el display de decenas.
- **`displayDecenasPins_ctl`**: Pin de control para el display de decenas.
- **`pinsObjectsU` y `pinsObjectsD`**: Listas para almacenar objetos de los pines del display de unidades y decenas, respectivamente.
- **`pinsObjectsD_ctl`**: Lista para almacenar el objeto del pin de control para el display de decenas.
- **`pinTurbine`, `pinExtractor`, y `pinLigth`**: Pines para la turbina, extractor y luz, respectivamente.
- **`pinDoorSen` y `pinButton`**: Pines para el sensor de puerta y el botón, respectivamente.

---

## 3. Funciones

- **`setupDisplayU(pins)`**: Configura los pines para el display de unidades y almacena los objetos de los pines en la lista `pinsObjectsU`.
- **`setupDisplayD(pins)`**: Configura los pines para el display de decenas (incluyendo el pin de control) y almacena los objetos de los pines en las listas `pinsObjectsD` y `pinsObjectsD_ctl`.
- **`setupOutput(pin)`**: Configura un pin como salida y devuelve el objeto del pin.
- **`setupInput(btn_pin)`**: Configura un pin como entrada con resistencia pull-up y devuelve el objeto del pin.
- **`displayNumber(displayTensPins, displayUnitsPins, number)`**: Muestra el número dado en los displays de unidades y decenas.

---

## 4. Máquina de Estados

La clase `StateMachine` gestiona los estados operativos del dispositivo.

- **`__init__(self)`**: Inicializa la máquina de estados con el estado inicial `START`.
- **`run(self)`**: Ejecuta la máquina de estados llamando a la función del estado actual.
- **`state0(self)`** (Estado `START`): Configura displays, salidas e inputs.
- **`state1(self)`** (Estado `SETTINGENV`): Muestra el valor de la cuenta regresiva y establece el estado inicial de la turbina, extractor y luz.
- **`state2(self)`** (Estado `WAITING`): Verifica los valores de los sensores de botón y puerta; si se cumplen las condiciones, transiciona al estado `PLAYING`.
- **`state3(self)`** (Estado `PLAYING`): Actualiza la cuenta regresiva en el display, decrementa el valor y vuelve al estado `SETTINGENV` si la cuenta llega a 0 o el sensor de puerta se activa.

---

## 5. Configuración de Pines

El código recorre los pines del 0 al 39 e intenta configurarlos como salidas. Imprime un mensaje indicando si cada pin fue configurado correctamente o no. Luego imprime los valores de los pines en la lista `displayUnidadesPins` (probablemente una referencia a `displayUnidadesPins`).

---

## Resumen

Este proyecto implementa un sistema de control basado en una máquina de estados para un dispositivo que utiliza displays de cuenta regresiva, turbina, extractor y luz. La máquina de estados administra los estados operativos del dispositivo, como la configuración del entorno, la espera de entrada del usuario y la ejecución de la cuenta regresiva. También se incluyen funciones para configurar el display, entradas y salidas, y para mostrar el valor de la cuenta regresiva en el display.

---

¡Esperamos que este código te sea útil en tu proyecto de control de dispositivos!
