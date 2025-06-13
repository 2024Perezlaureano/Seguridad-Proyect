import itertools
import string
import time
from datetime import datetime

class UniversalPasswordCracker:
    def __init__(self):
        self.charset = {
            'minúsculas': string.ascii_lowercase,
            'mayúsculas': string.ascii_uppercase,
            'números': string.digits,
            'símbolos': string.punctuation,
            'espacio': ' ',
            'todos': (string.ascii_letters + string.digits + string.punctuation + ' ')
        }
        
        self.report_file = "password_report.txt"
    
    def generate_combinations(self, length, use_upper=True, use_lower=True, 
                            use_digits=True, use_symbols=True, use_space=False):
        """Genera todas las combinaciones posibles para la longitud dada"""
        selected_chars = ''
        if use_lower:
            selected_chars += string.ascii_lowercase
        if use_upper:
            selected_chars += string.ascii_uppercase
        if use_digits:
            selected_chars += string.digits
        if use_symbols:
            selected_chars += string.punctuation
        if use_space:
            selected_chars += ' '
            
        return itertools.product(selected_chars, repeat=length)
    
    def brute_force_attack(self, target_function, max_length=8, **kwargs):
        """
        Realiza un ataque de fuerza bruta contra una función objetivo
        
        target_function: función que recibe user/pass y devuelve True si es correcto
        max_length: longitud máxima de contraseña a probar
        kwargs: configuración del conjunto de caracteres
        """
        start_time = datetime.now()
        attempts = 0
        found = False
        
        with open(self.report_file, 'w') as report:
            report.write(f"Inicio de ataque: {start_time}\n")
            report.write(f"Configuración: {kwargs}\n\n")
            
            print(f"\n[+] Iniciando ataque de fuerza bruta universal a las {start_time}")
            
            for length in range(1, max_length + 1):
                print(f"\n[+] Probando combinaciones de longitud {length}")
                report.write(f"\nLongitud {length}:\n")
                
                for combo in self.generate_combinations(length, **kwargs):
                    attempts += 1
                    password = ''.join(combo)
                    
                    # Mostrar progreso cada 1000 intentos
                    if attempts % 1000 == 0:
                        print(f"Intento {attempts}: Probando '{password}'", end='\r')
                    
                    # Prueba la contraseña
                    if target_function(password):
                        end_time = datetime.now()
                        elapsed = end_time - start_time
                        
                        print(f"\n[+] ¡Credencial encontrada después de {attempts} intentos!")
                        print(f"[+] Contraseña: {password}")
                        print(f"[+] Tiempo transcurrido: {elapsed}")
                        
                        report.write(f"\n¡ÉXITO!\n")
                        report.write(f"Contraseña encontrada: {password}\n")
                        report.write(f"Intentos: {attempts}\n")
                        report.write(f"Tiempo: {elapsed}\n")
                        
                        found = True
                        return password
                
                report.write(f"Completado: {length} caracteres. Intentos: {attempts}\n")
        
        if not found:
            end_time = datetime.now()
            elapsed = end_time - start_time
            print(f"\n[-] No se encontró la contraseña después de {attempts} intentos")
            print(f"[-] Tiempo transcurrido: {elapsed}")
            
            with open(self.report_file, 'a') as report:
                report.write(f"\nRESULTADO: No se encontró la contraseña\n")
                report.write(f"Intentos totales: {attempts}\n")
                report.write(f"Tiempo total: {elapsed}\n")
        
        return None

# Ejemplo de uso:
if __name__ == "__main__":
    cracker = UniversalPasswordCracker()
    
    # Ejemplo de función objetivo (debes reemplazarla con tu propia lógica)
    def example_target(password):
        # Esta es solo una función de ejemplo
        # Reemplázala con tu propia lógica de verificación
        correct_password = "abc123!"  # Solo para demostración
        return password == correct_password
    
    # Configuración del ataque
    config = {
        'max_length': 8,
        'use_upper': True,
        'use_lower': True,
        'use_digits': True,
        'use_symbols': True,
        'use_space': False
    }
    
    # Ejecutar el ataque
    result = cracker.brute_force_attack(example_target, **config)
    
    if result:
        print(f"\n[+] Contraseña encontrada: {result}")
    else:
        print("\n[-] No se encontró la contraseña")