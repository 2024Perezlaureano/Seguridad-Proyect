import itertools
import string
import time
from datetime import datetime
import os
import sys
import platform

class UniversalCredentialCracker:
    def __init__(self):
        self.charsets = {
            'lowercase': string.ascii_lowercase,
            'uppercase': string.ascii_uppercase,
            'digits': string.digits,
            'symbols': string.punctuation,
            'space': ' ',
            'all': (string.ascii_letters + string.digits + string.punctuation + ' ')
        }
        
        # Configuración de rutas multiplataforma
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        self.report_dir = os.path.join(desktop, "Password_Cracker_Reports")
        os.makedirs(self.report_dir, exist_ok=True)
        
        self.current_report = ""
        self.attempts = 0
        self.start_time = None
        self.running = True
    
    def clear_screen(self):
        """Limpia la pantalla de la consola"""
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')
    
    def generate_report_filename(self):
        """Genera un nombre de archivo único para el reporte"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.report_dir, f"attack_report_{timestamp}.txt")
    
    def log_attempt(self, email, password, success=False):
        """Registra un intento en el archivo de reporte"""
        try:
            with open(self.current_report, 'a', encoding='utf-8') as f:
                status = "SUCCESS" if success else "FAILED"
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] [{status}] Email: {email} | Password: {password}\n")
        except Exception as e:
            print(f"\n[!] Error al escribir en el reporte: {str(e)}")
    
    def test_credentials(self, email, password):
        """
        FUNCIÓN DE PRUEBA - REEMPLAZAR CON TU LÓGICA REAL
        
        Ejemplos de implementación real:
        1. Para SSH: usar paramiko.SSHClient()
        2. Para web: usar requests.post(url, auth=(email, password))
        3. Para APIs: usar la autenticación correspondiente
        """
        # EJEMPLO: Credenciales hardcodeadas para prueba
        correct_email = "test@example.com"
        correct_password = "Admin123!"
        
        # Simula un retraso de red
        time.sleep(0.01)
        
        return email == correct_email and password == correct_password
    
    def generate_combinations(self, base_chars, length):
        """Generador de combinaciones de contraseñas"""
        return itertools.product(base_chars, repeat=length)
    
    def estimate_time(self, charset_size, max_length):
        """Estima el tiempo máximo requerido (en segundos)"""
        # Asume 1000 intentos por segundo (ajustar según hardware)
        attempts_per_second = 1000
        total_combinations = sum(charset_size**l for l in range(1, max_length + 1))
        return total_combinations / attempts_per_second
    
    def format_time(self, seconds):
        """Formatea segundos a un string legible"""
        if seconds < 60:
            return f"{seconds:.2f} segundos"
        elif seconds < 3600:
            return f"{seconds/60:.2f} minutos"
        else:
            return f"{seconds/3600:.2f} horas"
    
    def crack_email_password(self, email_pattern=None, max_pass_length=6, 
                           use_upper=True, use_lower=True, use_digits=True, 
                           use_symbols=True, use_space=False):
        """Ejecuta el ataque de fuerza bruta"""
        # Configurar conjunto de caracteres
        chars = ""
        if use_lower: chars += string.ascii_lowercase
        if use_upper: chars += string.ascii_uppercase
        if use_digits: chars += string.digits
        if use_symbols: chars += string.punctuation
        if use_space: chars += " "
        
        charset_size = len(chars)
        estimated_time = self.estimate_time(charset_size, max_pass_length)
        
        # Preparar reporte
        self.current_report = self.generate_report_filename()
        self.start_time = datetime.now()
        self.attempts = 0
        
        with open(self.current_report, 'w', encoding='utf-8') as f:
            config_info = f"""
            CONFIGURACIÓN DEL ATAQUE:
            Fecha y hora: {self.start_time}
            Email objetivo: {email_pattern or 'Generación automática'}
            Longitud máxima de password: {max_pass_length}
            Tamaño del conjunto de caracteres: {charset_size}
            Caracteres incluidos:
              - Mayúsculas: {use_upper}
              - Minúsculas: {use_lower}
              - Dígitos: {use_digits}
              - Símbolos: {use_symbols}
              - Espacios: {use_space}
            
            ESTIMACIÓN:
            Tiempo estimado máximo: {self.format_time(estimated_time)}
            Combinaciones totales: {sum(charset_size**l for l in range(1, max_pass_length + 1)):,}
            """
            f.write(config_info)
            print(config_info)
        
        # Generar emails si no se proporciona uno fijo
        emails_to_try = [email_pattern] if email_pattern else self.generate_possible_emails()
        
        try:
            for email in emails_to_try:
                print(f"\n[+] Probando email: {email}")
                
                for pass_length in range(1, max_pass_length + 1):
                    if not self.running:
                        print("\n[!] Ataque detenido por el usuario")
                        return None
                    
                    print(f"[+] Probando contraseñas de longitud {pass_length}")
                    
                    for password_tuple in self.generate_combinations(chars, pass_length):
                        if not self.running:
                            print("\n[!] Ataque detenido por el usuario")
                            return None
                            
                        password = ''.join(password_tuple)
                        self.attempts += 1
                        
                        # Mostrar progreso
                        if self.attempts % 1000 == 0:
                            elapsed = datetime.now() - self.start_time
                            elapsed_sec = elapsed.total_seconds()
                            speed = self.attempts / elapsed_sec if elapsed_sec > 0 else 0
                            remaining = (estimated_time - elapsed_sec) if estimated_time > elapsed_sec else 0
                            
                            print(f"Intento {self.attempts:,} | Velocidad: {speed:,.0f} intentos/seg | "
                                  f"Tiempo transcurrido: {self.format_time(elapsed_sec)} | "
                                  f"Estimado restante: {self.format_time(remaining)}", end='\r')
                        
                        # Probar credenciales
                        if self.test_credentials(email, password):
                            elapsed = datetime.now() - self.start_time
                            elapsed_sec = elapsed.total_seconds()
                            speed = self.attempts / elapsed_sec if elapsed_sec > 0 else 0
                            
                            success_msg = f"""
                            [+++] CREDENCIALES ENCONTRADAS [+++]
                            Email: {email}
                            Password: {password}
                            Intentos totales: {self.attempts:,}
                            Tiempo transcurrido: {self.format_time(elapsed_sec)}
                            Velocidad promedio: {speed:,.0f} intentos/segundo
                            """
                            print(success_msg)
                            self.log_attempt(email, password, success=True)
                            
                            with open(self.current_report, 'a', encoding='utf-8') as f:
                                f.write("\n" + "="*50 + "\n")
                                f.write(success_msg)
                                f.write("\n" + "="*50 + "\n")
                            
                            return (email, password)
                        
                        self.log_attempt(email, password)
        
        except KeyboardInterrupt:
            print("\n[!] Ataque interrumpido por el usuario")
            self.running = False
            return None
        
        print("\n[-] No se encontraron credenciales válidas")
        return None
    
    def generate_possible_emails(self):
        """Genera posibles combinaciones de emails comunes"""
        domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'protonmail.com']
        usernames = ['admin', 'user', 'test', 'root', 'administrator', 'info', 'contact', 'support']
        
        for user in usernames:
            for domain in domains:
                yield f"{user}@{domain}"

def main_menu():
    cracker = UniversalCredentialCracker()
    cracker.clear_screen()
    
    print("""
    ██████╗ ██████╗ ██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗ 
    ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
    ██████╔╝██████╔╝██║  ██║███████║██║     █████╔╝ █████╗  ██████╔╝
    ██╔══██╗██╔══██╗██║  ██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
    ██████╔╝██║  ██║██████╔╝██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
    ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    """)
    print("Buscador Universal de Credenciales - Versión 2.0")
    print("-----------------------------------------------")
    print("ADVERTENCIA: Solo para uso ético y en sistemas propios")
    print("             El uso no autorizado es ilegal\n")
    
    while True:
        try:
            # Configuración del ataque
            print("\n[CONFIGURACIÓN DEL ATAQUE]")
            email = input("Email específico a probar (dejar vacío para probar comunes): ").strip() or None
            
            while True:
                max_len_input = input("Longitud máxima de password (1-6 recomendado, 8 máximo): ").strip()
                if not max_len_input:
                    max_len = 6
                    break
                if max_len_input.isdigit():
                    max_len = int(max_len_input)
                    if 1 <= max_len <= 8:
                        break
                    print("[!] Por favor ingresa un número entre 1 y 8")
                else:
                    print("[!] Entrada inválida. Ingresa un número.")
            
            print("\n[SELECCIÓN DE CARACTERES]")
            use_upper = input("Incluir mayúsculas (A-Z)? [s/n]: ").lower() == 's'
            use_lower = input("Incluir minúsculas (a-z)? [s/n]: ").lower() == 's'
            use_digits = input("Incluir dígitos (0-9)? [s/n]: ").lower() == 's'
            use_symbols = input("Incluir símbolos (!@#$...)? [s/n]: ").lower() == 's'
            use_space = input("Incluir espacios? [s/n]: ").lower() == 's'
            
            # Mostrar advertencia para configuraciones complejas
            charset_size = (
                (26 if use_upper else 0) + 
                (26 if use_lower else 0) + 
                (10 if use_digits else 0) + 
                (32 if use_symbols else 0) + 
                (1 if use_space else 0)
            )
            estimated = cracker.estimate_time(charset_size, max_len)
            if estimated > 300:  # Más de 5 minutos
                print(f"\n[!] ADVERTENCIA: Esta configuración podría tomar hasta {cracker.format_time(estimated)}")
                confirm = input("¿Deseas continuar? [s/n]: ").lower()
                if confirm != 's':
                    continue
            
            print("\n[+] Iniciando ataque... (Presiona Ctrl+C para detener)")
            result = cracker.crack_email_password(
                email_pattern=email,
                max_pass_length=max_len,
                use_upper=use_upper,
                use_lower=use_lower,
                use_digits=use_digits,
                use_symbols=use_symbols,
                use_space=use_space
            )
            
            if result:
                email, password = result
                print(f"\n[+] Credenciales encontradas: {email}:{password}")
            else:
                print("\n[-] No se encontraron credenciales válidas")
            
            print(f"\nReporte detallado guardado en: {cracker.current_report}")
            
            another = input("\n¿Deseas realizar otro ataque? [s/n]: ").lower()
            if another != 's':
                break
                
            cracker.clear_screen()
            cracker = UniversalCredentialCracker()  # Resetear para nuevo ataque
            
        except KeyboardInterrupt:
            print("\n[!] Operación cancelada por el usuario")
            break
        except Exception as e:
            print(f"\n[!] Error inesperado: {str(e)}")
            time.sleep(2)
            cracker.clear_screen()

if __name__ == "__main__":
    main_menu()