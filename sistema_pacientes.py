import json
import re
from datetime import datetime, date
from typing import Dict, List, Optional

class Paciente:
    def __init__(self, cedula: str, nombre: str, apellido: str, telefono: str,
                 email: str, fecha_nacimiento: str):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email
        self.fecha_nacimiento: date = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
        self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict:
        return {
            'cedula': self.cedula,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'telefono': self.telefono,
            'email': self.email,
            'fecha_nacimiento': self.fecha_nacimiento.strftime("%Y-%m-%d"),
            'fecha_registro': self.fecha_registro
        }

class SistemaRegistroPacientes:
    """Gestiona la colección de pacientes y la persistencia de datos."""
    def __init__(self, archivo_datos: str = "pacientes.json"):
        self.archivo_datos = archivo_datos
        self.pacientes: Dict[str, Paciente] = {}
        self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos de los pacientes desde un archivo JSON."""
        try:
            with open(self.archivo_datos, 'r', encoding='utf-8') as file:
                datos = json.load(file)
                for cedula, info in datos.items():
                    paciente = Paciente(
                        info['cedula'], info['nombre'], info['apellido'],
                        info['telefono'], info['email'], info['fecha_nacimiento']
                    )
                    paciente.fecha_registro = info['fecha_registro']
                    self.pacientes[cedula] = paciente
        except FileNotFoundError:
            print("Datos no encontrados. Creando uno nuevo.")
    
    def guardar_datos(self):
        """Guarda los datos de los pacientes en un archivo JSON."""
        datos = {cedula: paciente.to_dict() for cedula, paciente in self.pacientes.items()}
        with open(self.archivo_datos, 'w', encoding='utf-8') as file:
            json.dump(datos, file, indent=2, ensure_ascii=False)
    
    def _validar_email(self, email: str) -> bool:
        """
        Valida el formato de una dirección de correo electrónico.

        Args:
            email (str): El correo electrónico a validar.

        Returns:
            bool: True si el formato es válido, False en caso contrario.
        """
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    def _validar_telefono(self, telefono: str) -> bool:
        """Valida que el teléfono contenga solo dígitos."""
        return telefono.isdigit()

    def _validar_fecha(self, fecha_str: str) -> bool:
        """Valida el formato de la fecha (YYYY-MM-DD)."""
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def registrar_paciente(self, cedula: str, nombre: str, apellido: str,
                          telefono: str, email: str, fecha_nacimiento: str) -> bool:

        """Registra un nuevo paciente"""
        if cedula in self.pacientes:
            print(f"Error: Ya existe un paciente con cedula {cedula}")
            return False
        
        if not self._validar_telefono(telefono):
            print("Error: El formato del teléfono no es válido. Use solo números.")
            return False

        if not self._validar_email(email):
            print("Error: El formato del email no es válido.")
            return False

        if not self._validar_fecha(fecha_nacimiento):
            print("Error: El formato de la fecha de nacimiento debe ser YYYY-MM-DD.")
            return False

        paciente = Paciente(cedula, nombre, apellido, telefono, email,
                          fecha_nacimiento )
        self.pacientes[cedula] = paciente
        self.guardar_datos()
        print(f"Paciente {nombre} {apellido} registrado exitosamente.")
        return True
    
    def buscar_paciente(self, cedula: str) -> Optional[Paciente]:
        """Busca un paciente por cedula"""
        return self.pacientes.get(cedula)
    
    def listar_pacientes(self) -> List[Paciente]:
        """Lista todos los pacientes"""
        return list(self.pacientes.values())
    
    def actualizar_paciente(self, cedula: str, **kwargs) -> bool:
        """Actualiza los datos de un paciente"""
        if cedula not in self.pacientes:
            print(f"Error: No se encontro paciente con cedula {cedula}")
            return False
        
        paciente = self.pacientes[cedula]
        for campo, valor in kwargs.items():
            if campo == 'telefono' and not self._validar_telefono(valor):
                print("Error: El formato del teléfono no es válido. Use solo números.")
                return False
            if campo == 'email' and not self._validar_email(valor):
                print("Error: El formato del email no es válido.")
                return False
            if hasattr(paciente, campo):
                setattr(paciente, campo, valor)
        
        self.guardar_datos()
        print(f"Paciente con cedula {cedula} actualizado exitosamente.")
        return True
    
    def eliminar_paciente(self, cedula: str) -> bool:
        """Elimina un paciente"""
        if cedula not in self.pacientes:
            print(f"Error: No se encontro paciente con cedula {cedula}")
            return False
        
        del self.pacientes[cedula]
        self.guardar_datos()
        print(f"Paciente con cedula {cedula} eliminado exitosamente.")
        return True

def menu_principal():
    sistema = SistemaRegistroPacientes()
    
    while True:
        print("\n=== SISTEMA DE REGISTRO DE PACIENTES ===")
        print("1. Registrar nuevo paciente")
        print("2. Buscar paciente")
        print("3. Listar todos los pacientes")
        print("4. Actualizar paciente")
        print("5. Eliminar paciente")
        print("6. Salir")
        print("\n========================================")
        
        opcion = input("\nSeleccione una opcion: ")
        
        if opcion == "1":
            print("\n--- Registro de Nuevo Paciente ---")
            cedula = input("Cédula: ")
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            telefono = input("Teléfono: ")
            email = input("Email: ")
            fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")

            sistema.registrar_paciente(cedula, nombre, apellido, telefono, email, fecha_nacimiento)

        elif opcion == "2":
            cedula = input("\nIngrese la cédula del paciente: ")
            paciente = sistema.buscar_paciente(cedula)
            if paciente:
                print(f"\n--- Información del Paciente ---")
                print(f"Cédula: {paciente.cedula}")
                print(f"Nombre: {paciente.nombre} {paciente.apellido}")
                print(f"Teléfono: {paciente.telefono}")
                print(f"Email: {paciente.email}")
                print(f"Fecha de nacimiento: {paciente.fecha_nacimiento.strftime('%Y-%m-%d')}")
                print(f"Fecha de registro: {paciente.fecha_registro}")
            else:
                print("Paciente no encontrado.")
        
        elif opcion == "3":
            pacientes = sistema.listar_pacientes()
            if pacientes:
                print(f"\n--- Lista de Pacientes ({len(pacientes)} registrados) ---")
                for paciente in pacientes:
                    print(f"{paciente.cedula} - {paciente.nombre} {paciente.apellido}")
            else:
                print("No hay pacientes registrados.")
        
        elif opcion == "4":
            cedula = input("\nIngrese la cedula del paciente a actualizar: ")
            if sistema.buscar_paciente(cedula):
                print("Campos a actualizar (presione Enter para omitir):")
                campos = {}
                
                nuevo_telefono = input("Nuevo telefono: ")
                if nuevo_telefono: campos['telefono'] = nuevo_telefono
                
                nuevo_email = input("Nuevo email: ")
                if nuevo_email: campos['email'] = nuevo_email

                if campos:
                    sistema.actualizar_paciente(cedula, **campos)
                else:
                    print("No se realizaron cambios.")
            else:
                print("Paciente no encontrado.")
        
        elif opcion == "5":
            cedula = input("\nIngrese la cedula del paciente a eliminar: ")
            confirmacion = input(f"¿Está seguro de eliminar el paciente con cedula {cedula}? (s/n): ")
            if confirmacion.lower() == 's':
                sistema.eliminar_paciente(cedula)
        
        elif opcion == "6":
            print("Hasta luego!")
            break
        
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu_principal()