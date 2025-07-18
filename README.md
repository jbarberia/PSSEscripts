# PSSEscripts
Conjunto de scripts para realizar estudios eléctricos en PSSE


# Uso
Preferentemente se creará un batch file o Makefile para poder correr diferentes scripts en paralelo.


# Organización de los scripts
Los scripts que inician con el prefijo sld_ son utilizados para operar dentro de la GUI del PSSE.
Los scripts que inician con reporte_ son utilizados para generar la salida en un .xlsx o .png dependiendo que se requiera.

# Simulaciones dinamicas

Para automatizar las simulaciones dinámicas se debe pasar un script que inicialize la base y referencia la salida de los canales del archivo .outx a una variable no definida llamada outfile.

Es una buena practica verificar y frenar el proceso si se genera una condicion sospechosa en la simulacion.
