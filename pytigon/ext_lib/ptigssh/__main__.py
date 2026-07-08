import sys
import select
import tty
import termios
import getpass
import paramiko
import signal
import os

def get_terminal_size():
    """Pobiera aktualną szerokość i wysokość lokalnego okna konsoli"""
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except OSError:
        return 80, 24  # Wartości domyślne w razie błędu

def run_interactive_shell(chan):
    """Funkcja obsługująca interaktywny terminal w Linuksie"""
    oldtty = termios.tcgetattr(sys.stdin)
    
    # Reakcja na zmianę rozmiaru okna (SIGWINCH)
    def resize_handler(signum, frame):
        try:
            col, row = get_terminal_size()
            chan.resize_pty(width=col, height=row)
        except Exception:
            pass

    # Rejestracja przechwytywania sygnału zmiany rozmiaru okna
    signal.signal(signal.SIGWINCH, resize_handler)

    try:
        # Przełączenie lokalnego terminala w tryb RAW
        tty.setraw(sys.stdin.fileno())
        chan.setblocking(0)

        while True:
            # Sprawdzanie czy są nowe dane na serwerze lub z klawiatury
            r, w, e = select.select([chan, sys.stdin], [], [])
            
            # Serwer przysłał dane -> wyświetl je
            if chan in r:
                try:
                    x = chan.recv(1024).decode('utf-8', errors='ignore')
                    if len(x) == 0:
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except Exception:
                    break
                    
            # Użytkownik kliknął klawisz(e) -> wyślij do serwera jako cały pakiet
            if sys.stdin in r:
                # Czytamy nie 1 bajt, ale wszystko co aktualnie czeka w buforze wejściowym (np. całą strzałkę)
                x = os.read(sys.stdin.fileno(), 4096)
                if len(x) == 0:
                    break
                chan.send(x)


    finally:
        # Przywrócenie normalnego działania terminala w Linuksie
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
        # Wyczyszczenie handlera sygnału
        signal.signal(signal.SIGWINCH, signal.SIG_DFL)

# --- Pobieranie danych od użytkownika ---
hostname = input("Podaj adres serwera (IP/Host): ")
username = input("Podaj nazwę użytkownika: ")
password = getpass.getpass("Podaj hasło (znaki będą ukryte): ")

# --- Połączenie Paramiko ---
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"\nŁączenie z {hostname}...")
    client.connect(hostname=hostname, username=username, password=password, timeout=10)
    
    # Pobranie aktualnego rozmiaru okna przed startem powłoki
    current_col, current_row = get_terminal_size()
    
    # Otwarcie kanału z przekazaniem poprawnego typu terminala oraz jego dokładnych wymiarów
    chan = client.invoke_shell(
        term='xterm-256color',
        width=current_col,
        height=current_row
    )
    
    print("*** Połączono! Uruchamiam interaktywną konsolę SSH... ***\n")
    run_interactive_shell(chan)
    
    chan.close()

except Exception as e:
    print(f"\nBłąd połączenia: {e}")

finally:
    client.close()
    print("\n*** Połączenie zamknięte ***")
