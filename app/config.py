from dotenv import load_dotenv, os
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

    MSSQL_SERVER   = os.getenv("MSSQL_SERVER", "DAVID")
    MSSQL_PORT     = int(os.getenv("MSSQL_PORT", "1433"))
    MSSQL_DATABASE = os.getenv("MSSQL_DATABASE", "JoyeriaDelCentroDB")
    MSSQL_USER     = os.getenv("MSSQL_USER", "sa")
    MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD", "")
    MSSQL_DRIVER   = os.getenv("MSSQL_DRIVER", "ODBC Driver 17 for SQL Server")

    @property
    def ODBC_STRING(self) -> str:
        """
        Cadena ODBC para pyodbc.
        - En local (Windows): ODBC 17/18 de Microsoft → usa SERVER=host,port
        - En Render (Linux):  FreeTDS (tdsodbc)      → usa SERVER=host y PORT=port
        """
        driver = self.MSSQL_DRIVER.strip()

        # ---- Rama para FreeTDS (Render) ----
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

        # ---- Rama por defecto (Microsoft ODBC 17/18) ----
        return (
            "DRIVER={" + driver + "};"
            f"SERVER={self.MSSQL_SERVER},{self.MSSQL_PORT};"
            f"DATABASE={self.MSSQL_DATABASE};"
            f"UID={self.MSSQL_USER};"
            f"PWD={self.MSSQL_PASSWORD};"
            "Encrypt=Yes;"
            "TrustServerCertificate=Yes;"
            "Connection Timeout=30;"
        )

config = Config()
