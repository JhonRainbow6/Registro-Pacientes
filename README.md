# ARQUITECTURA DE CAPAS



## Capa de Presentacion (Interfaz)

- Menú de opciones (print("\n=== SISTEMA DE REGISTRO DE PACIENTES ===")).

- Capturar de selección del usuario (opcion = input("\nSeleccione una opcion: ")).

- Solicitud de datos necesarios para cada operación (cedula = input("Cédula: ")).

- Mostrar los resultados de las operaciones al usuario (como la información de un paciente o mensajes de confirmación/error).




## Capa de Negocio (Logica)

- Orquestación de operaciones: Métodos como registrar_paciente(), actualizar_paciente() y eliminar_paciente() coordinan las validaciones y el acceso a los datos.

- Validación de datos: Métodos privados como _validar_email(), _validar_telefono() y _validar_fecha() se aseguran de que los datos cumplan con el formato y las reglas requeridas antes de ser procesados.

- Reglas de negocio: No permitir el registro de un paciente con una cédula duplicada (if cedula in self.pacientes:).

- Gestión de la colección de pacientes: Mantiene el estado de la lista de pacientes en memoria (self.pacientes: Dict [str, Paciente]).




## Capa de Acceso a Datos (Persistencia)

- Carga de datos: cargar_datos() lee el archivo pacientes.json y convierte la información en objetos 'Paciente' que la aplicación puede utilizar.

- Guardado de datos: guardar_datos() toma los objetos 'Paciente' de la memoria y los convierte a un formato JSON para escribirlos en el archivo.

- Manejo de la fuente de datos: Gestion de excepciones si el archivo de datos no existe.
