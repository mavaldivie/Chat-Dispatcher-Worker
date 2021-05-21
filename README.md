# Respuesta Tarea 4 (Patron dispatcher-worker)
## Marcos Adrian Valdivie Rodriguez C412

La implementación proporcionada consiste en dos clases, server y client, las cuales llevan los pasos lógicos para el trabajo desde el servidor y el cliente respectivamente. 
El programa está desarrollado para que funcione en una distribución en forma de estrella, en la que todos los clientes se comunican a través del servidor. Para esto se usaron sockets TCP en el cliente y el servidor para manejar el tráfico de mensajes.

El servidor abre un socket al iniciarse, y se relaciona a la dirección pasada en el constructor desde la cual escuchará por conexiones entrantes. Cuando un cliente intenta establecer conexión con el server este creará un nuevo hilo el cual se ocupará de manejar dicha conexión. Dentro de ese hilo se acomodarán las variables necesarias para el trabajo con el cliente y se crearán dos hilos más que serán los encargados de manejar los mensajes que se reciban y se envien a ese cliente.

Los mensajes se enviarán especificando el número de orden del mensaje, y si es de ACK o no. El ACK se hace para dar constancia al servidor que el cliente recibió correctamente el mensaje que le tocaba y el número de orden para asegurar que todos los clientes reciban los mensajes en el mismo orden. El número del mensaje correspondiente al último ACK de un cliente dado se guarda en un diccionario llamado expACK, se utiliza un semaphore para controlar el acceso concurrente a este contenedor a la hora de modificarlo.

El cliente abre un socket de tipo TCP y crea un hilo desde el cual se recibirán todos los mensajes entrantes y se escribirán en la consola. Para enviar un mensaje se debe llamar al método send pasándole como parámetro el mensaje.

Con respecto a la solución implementada anteriormente se puede destacar el uso de dos hilos en el servidor para manejar los mensajes entrantes y salientes desde un mismo cliente, ya que en la anterior se usaba un mismo hilo para enviar todos los mensajes a todos los clientes, lo que podía ocasionar demoras para recibir el mensaje por el cliente. Además se puede destacar el uso del semáforo para manejar concurrentemente los recursos de la clase, lo que ocasionaba comportamientos indebidos en la anterior solución.

***
Para ejecutar el programa es necesario correr el script correspondiente con Python pasándole el parámetro --address en el caso del servidor y --address y --name en el caso del cliente. Ejemplo:
Para correr el servidor, se iniciará un proceso que escuchará conexiones enviadas a la dirección pasada por parámetro

```bash
$ python3 server.py --address 127.0.0.1:8081   
```

Para correr el cliente, se iniciará un proceso que se conectará a la dirección pasada como parámetro y se comunicará con los demás clientes a través de la misma, el parámetro name se usa para colocar un identificador en todos los mensajes enviados por el proceso. Los mensajes se enviarán y podrán ser observados desde la consola con que se ejecuta el comando.

```bash
$ python3 client.py --address 127.0.0.1:8081 --name cliente
```

***
Para el desarrollo del programa se usaron los módulos threading, random, argparse y zmq de python.
