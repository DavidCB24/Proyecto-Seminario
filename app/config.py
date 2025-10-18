import os
from dotenv import load_dotenv
load_dotenv()

def _default_driver():
    # Si no estás en Windows, por defecto usa FreeTDS (útil para Render/Linux)
    return "ODBC Driver 17 for SQL Server" if os.name == "nt" else "FreeTDS"

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

    MSSQL_SERVER   = os.getenv("MSSQL_SERVER", "DAVID")
    MSSQL_PORT     = int(os.getenv("MSSQL_PORT", "1433"))
    MSSQL_DATABASE = os.getenv("MSSQL_DATABASE", "JoyeriaDelCentroDB")
    MSSQL_USER     = os.getenv("MSSQL_USER", "sa")
    MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD", "")
    MSSQL_DRIVER   = os.getenv("MSSQL_DRIVER", _default_driver()).strip()

    @property
    def ODBC_STRING(self) -> str:
        """
        Cadena ODBC para pyodbc.
        - En local (Windows): ODBC 17/18 de Microsoft → usa SERVER=host,port
        - En Render (Linux):  FreeTDS (tdsodbc)      → usa SERVER=host y PORT=port
        """
        driver = self.MSSQL_DRIVER

        # ---- Rama para FreeTDS (Render/Linux) ----
        if driver.lower() in ("freetds", "tdsodbc"):
            return (
                "DRIVER={FreeTDS};"
                f"SERVER={self.MSSQL_SERVER};"
                f"PORT={self.MSSQL_PORT};"
                f"DATABASE={self.MSSQL_DATABASE};"
                f"UID={self.MSSQL_USER};"
                f"PWD={self.MSSQL_PASSWORD};"
                "TDS_Version=7.4;"          # SQL Server/Azure
                "Encrypt=Yes;"              # Azure requiere TLS
                "TrustServerCertificate=Yes;"
                "ClientCharset=UTF-8;"
                "Connection Timeout=30;"
            )

        # ---- Rama Microsoft ODBC (Windows) ----
        return (
            f"DRIVER={{{driver}}};"
            f"SERVER={self.MSSQL_SERVER},{self.MSSQL_PORT};"
            f"DATABASE={self.MSSQL_DATABASE};"
            f"UID={self.MSSQL_USER};"
            f"PWD={self.MSSQL_PASSWORD};"
            "Encrypt=Yes;"
            "TrustServerCertificate=Yes;"
            "Connection Timeout=30;"
        )

config = Config()

# (Opcional) imprime en logs qué driver quedó seleccionado, útil para Render
print(f"[config] MSSQL_DRIVER='{config.MSSQL_DRIVER}'  (os.name={os.name})")
