"""
Interfaz de linea de comandos (CLI) para el sistema de gestion de clinica.
"""

from datetime import datetime
import sys
import os

# Anadir el directorio padre al path para poder importar los modulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modelo.clinica import Clinica
from modelo.paciente import Paciente
from modelo.medico import Medico
from modelo.especialidad import Especialidad
from modelo.excepciones import *


class CLI:
    """
    Clase CLI que actua como la interfaz de usuario por consola para interactuar 
    con el sistema de gestion de la clinica.
    """
    
    def __init__(self):
        """Inicializa la interfaz CLI."""
        self.clinica = Clinica()
        self.ejecutando = True
    
    def mostrar_menu(self):
        """Muestra el menu principal."""
        print("\n" + "="*50)
        print(" SISTEMA DE GESTION CLINICA")
        print("="*50)
        print("1) Agregar paciente")
        print("2) Agregar medico")
        print("3) Agendar turno")
        print("4) Agregar especialidad a medico")
        print("5) Emitir receta")
        print("6) Ver historia clinica")
        print("7) Ver todos los turnos")
        print("8) Ver todos los pacientes")
        print("9) Ver todos los medicos")
        print("0) Salir")
        print("="*50)
    
    def ejecutar(self):
        """Ejecuta el bucle principal de la aplicacion."""
        print("¡Bienvenido al Sistema de Gestion de Clinica!")
        
        while self.ejecutando:
            try:
                self.mostrar_menu()
                opcion = input("Seleccione una opcion: ").strip()
                
                if opcion == "1":
                    self.agregar_paciente()
                elif opcion == "2":
                    self.agregar_medico()
                elif opcion == "3":
                    self.agendar_turno()
                elif opcion == "4":
                    self.agregar_especialidad()
                elif opcion == "5":
                    self.emitir_receta()
                elif opcion == "6":
                    self.ver_historia_clinica()
                elif opcion == "7":
                    self.ver_todos_turnos()
                elif opcion == "8":
                    self.ver_todos_pacientes()
                elif opcion == "9":
                    self.ver_todos_medicos()
                elif opcion == "0":
                    self.salir()
                else:
                    print("❌ Opcion invlida. Por favor, seleccione una opcion del 0 al 9.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                self.ejecutando = False
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
    
    def agregar_paciente(self):
        """Solicita los datos y agrega un nuevo paciente."""
        try:
            print("\n--- AGREGAR PACIENTE ---")
            nombre = input("Nombre completo: ").strip()
            dni = input("DNI: ").strip()
            fecha_nacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ").strip()
            
            paciente = Paciente(nombre, dni, fecha_nacimiento)
            self.clinica.agregar_paciente(paciente)
            
            print(f"✅ Paciente agregado exitosamente: {paciente}")
            
        except PacienteDuplicadoException as e:
            print(f"❌ {e}")
        except DatoInvalidoException as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Error al agregar paciente: {e}")
    
    def agregar_medico(self):
        """Solicita los datos y agrega un nuevo medico."""
        try:
            print("\n--- AGREGAR MEDICO ---")
            nombre = input("Nombre completo: ").strip()
            matricula = input("Matricula: ").strip()
            
            medico = Medico(nombre, matricula)
            
            # Agregar especialidades
            print("\nAgregue al menos una especialidad:")
            while True:
                tipo_especialidad = input("Nombre de la especialidad: ").strip()
                if not tipo_especialidad:
                    print("❌ El nombre de la especialidad no puede estar vacio.")
                    continue
                
                print("Días de atencion (separados por comas):")
                print("Ejemplo: lunes, miercoles, viernes")
                dias_input = input("Dias: ").strip()
                
                if not dias_input:
                    print("❌ Debe especificar al menos un dia.")
                    continue
                
                dias = [dia.strip() for dia in dias_input.split(",")]
                
                try:
                    especialidad = Especialidad(tipo_especialidad, dias)
                    medico.agregar_especialidad(especialidad)
                    print(f"✅ Especialidad agregada: {especialidad}")
                    break
                except (DatoInvalidoException, EspecialidadDuplicadaException) as e:
                    print(f"❌ {e}")
            
            self.clinica.agregar_medico(medico)
            print(f"✅ Medico agregado exitosamente: {medico}")
            
        except MedicoDuplicadoException as e:
            print(f"❌ {e}")
        except DatoInvalidoException as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Error al agregar medico: {e}")
    
    def agendar_turno(self):
        """Solicita los datos y agenda un nuevo turno."""
        try:
            print("\n--- AGENDAR TURNO ---")
            dni = input("DNI del paciente: ").strip()
            matricula = input("Matricula del medico: ").strip()
            especialidad = input("Especialidad: ").strip()
            
            print("Fecha y hora del turno:")
            fecha_str = input("Fecha (dd/mm/aaaa): ").strip()
            hora_str = input("Hora (HH:MM): ").strip()
            
            # Parsear fecha y hora
            fecha_hora_str = f"{fecha_str} {hora_str}"
            fecha_hora = datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M")
            
            self.clinica.agendar_turno(dni, matricula, especialidad, fecha_hora)
            print("✅ Turno agendado exitosamente.")
            
        except (PacienteNoEncontradoException, MedicoNoEncontradoException, 
                MedicoNoDisponibleException, TurnoOcupadoException) as e:
            print(f"❌ {e}")
        except ValueError:
            print("❌ Formato de fecha u hora invalido. Use dd/mm/aaaa para fecha y HH:MM para hora.")
        except Exception as e:
            print(f"❌ Error al agendar turno: {e}")
    
    def agregar_especialidad(self):
        """Agrega una especialidad a un medico existente."""
        try:
            print("\n--- AGREGAR ESPECIALIDAD A MEDICO ---")
            matricula = input("Matricula del medico: ").strip()
            
            # Verificar que el medico existe
            medico = self.clinica.obtener_medico_por_matricula(matricula)
            
            tipo_especialidad = input("Nombre de la especialidad: ").strip()
            print("Dias de atencion (separados por comas):")
            print("Ejemplo: lunes, miercoles, viernes")
            dias_input = input("Dias: ").strip()
            
            dias = [dia.strip() for dia in dias_input.split(",")]
            
            especialidad = Especialidad(tipo_especialidad, dias)
            medico.agregar_especialidad(especialidad)
            
            print(f"✅ Especialidad agregada exitosamente: {especialidad}")
            
        except MedicoNoEncontradoException as e:
            print(f"❌ {e}")
        except (DatoInvalidoException, EspecialidadDuplicadaException) as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Error al agregar especialidad: {e}")
    
    def emitir_receta(self):
        """Solicita los datos y emite una nueva receta."""
        try:
            print("\n--- EMITIR RECETA ---")
            dni = input("DNI del paciente: ").strip()
            matricula = input("Matricula del medico: ").strip()
            
            print("Medicamentos (separados por comas):")
            print("Ejemplo: Ibuprofeno 400mg, Paracetamol 500mg")
            medicamentos_input = input("Medicamentos: ").strip()
            
            if not medicamentos_input:
                print("❌ Debe especificar al menos un medicamento.")
                return
            
            medicamentos = [med.strip() for med in medicamentos_input.split(",")]
            
            self.clinica.emitir_receta(dni, matricula, medicamentos)
            print("✅ Receta emitida exitosamente.")
            
        except (PacienteNoEncontradoException, MedicoNoEncontradoException,
                RecetaInvalidaException) as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Error al emitir receta: {e}")
    
    def ver_historia_clinica(self):
        """Muestra la historia clinica de un paciente."""
        try:
            print("\n--- VER HISTORIA CLINICA ---")
            dni = input("DNI del paciente: ").strip()
            
            historia = self.clinica.obtener_historia_clinica(dni)
            print(f"\n{historia}")
            
        except PacienteNoEncontradoException as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Error al obtener historia clinica: {e}")
    
    def ver_todos_turnos(self):
        """Muestra todos los turnos agendados."""
        try:
            print("\n--- TODOS LOS TURNOS ---")
            turnos = self.clinica.obtener_turnos()
            
            if not turnos:
                print("No hay turnos agendados.")
                return
            
            for i, turno in enumerate(turnos, 1):
                print(f"{i}. {turno}")
                
        except Exception as e:
            print(f"❌ Error al obtener turnos: {e}")
    
    def ver_todos_pacientes(self):
        """Muestra todos los pacientes registrados."""
        try:
            print("\n--- TODOS LOS PACIENTES ---")
            pacientes = self.clinica.obtener_pacientes()
            
            if not pacientes:
                print("No hay pacientes registrados.")
                return
            
            for i, paciente in enumerate(pacientes, 1):
                print(f"{i}. {paciente}")
                
        except Exception as e:
            print(f"❌ Error al obtener pacientes: {e}")
    
    def ver_todos_medicos(self):
        """Muestra todos los medicos registrados."""
        try:
            print("\n--- TODOS LOS MEDICOS ---")
            medicos = self.clinica.obtener_medicos()
            
            if not medicos:
                print("No hay medicos registrados.")
                return
            
            for i, medico in enumerate(medicos, 1):
                print(f"{i}. {medico}")
                
        except Exception as e:
            print(f"❌ Error al obtener medicos: {e}")
    
    def salir(self):
        """Termina la ejecucion del programa."""
        print("\n👋 ¡Gracias por usar el Sistema de Gestion de Clinica!")
        self.ejecutando = False


def main():
    """Funcion principal para ejecutar la CLI."""
    cli = CLI()
    cli.ejecutar()


if __name__ == "__main__":
    main ()