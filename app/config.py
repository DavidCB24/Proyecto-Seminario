import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

    MSSQL_SERVER = os.getenv("MSSQL_SERVER", "DAVID")
    MSSQL_PORT = int(os.getenv("MSSQL_PORT", "1433"))
    MSSQL_DATABASE = os.getenv("MSSQL_DATABASE", "JoyeriaDelCentroDB")
    MSSQL_USER = os.getenv("MSSQL_USER", "sa")
    MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD", "")
    MSSQL_DRIVER = os.getenv("MSSQL_DRIVER", "ODBC Driver 17 for SQL Server")

    @property
    def ODBC_STRING(self) -> str:
        """
        Cadena ODBC para pyodbc.
        Encrypt=Yes + TrustServerCertificate=Yes para entorno local.
        En producción usa certificados válidos (quita TrustServerCertificate).
        """
        return (
            "DRIVER={" + self.MSSQL_DRIVER + "};"
            f"SERVER={self.MSSQL_SERVER},{self.MSSQL_PORT};"
            f"DATABASE={self.MSSQL_DATABASE};"
            f"UID={self.MSSQL_USER};"
            f"PWD={self.MSSQL_PASSWORD};"
            "Encrypt=Yes;"
            "TrustServerCertificate=Yes;"
            "Connection Timeout=30;"
        )

config = Config()
