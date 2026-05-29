class BaseCurrencyAdapter:
    """
    Interfaz base para adaptadores de moneda — DIP (Inversión de Dependencias).
    Si mañana se cambia de API, solo se crea otra clase concreta.
    El resto del código no cambia.
    """
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        raise NotImplementedError("Las subclases deben implementar get_exchange_rate()")