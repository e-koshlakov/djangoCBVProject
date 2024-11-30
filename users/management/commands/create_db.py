from django.core.management.base import BaseCommand
import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

class Command(BaseCommand):
    help = 'Create the database'

    def handle(self, *args, **options):
        ODBC_DRIVER = os.getenv('ODBC_DRIVER')
        SERVER = os.getenv('SERVER')
        USER = os.getenv('DUSER')
        PASSWORD = os.getenv('PASSWORD')
        PAD_DATABASE = os.getenv('PAD_DATABASE')
        DATABASE = 'DjangoCBVProjectDB'

        ConnectionString = f'''DRIVER={{{ODBC_DRIVER}}};
        SERVER={SERVER};
        DATABASE={PAD_DATABASE};
        UID={USER};
        PWD={PASSWORD};
        TrustServerCertificate=yes;
        Encrypt=no'''

        try:
            conn = pyodbc.connect(ConnectionString)
            conn.autocommit = True
            conn.execute(fr"CREATE DATABASE {DATABASE};")
        except pyodbc.ProgrammingError as ex:
            print(ex)
        else:
            print("База данных успешно создана")