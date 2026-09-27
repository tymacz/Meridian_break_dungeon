class EventBus:
    _abonnes = {}

    @classmethod
    def s_abonner(cls, type_evenement: str, callback):
        """Ajoute une fonction à exécuter quand un événement précis survient."""
        if type_evenement not in cls._abonnes:
            cls._abonnes[type_evenement] = []
        cls._abonnes[type_evenement].append(callback)

    @classmethod
    def emettre(cls, type_evenement: str, donnees: dict = None):
        """Déclenche toutes les fonctions abonnées à cet événement."""
        if donnees is None:
            donnees = {}

        if type_evenement in cls._abonnes:
            for callback in cls._abonnes[type_evenement]:
                callback(donnees)
