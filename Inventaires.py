from Items import Item

class Inventaire:
    def __init__(self, capacite_max: float):
        self.capacite_max = capacite_max
        self.items: list[Item] = (
            []
        )

    @property
    def poids_actuel(self) -> float:
        return sum(item.poids for item in self.items)

    def ajouter(self, item: Item) -> bool:
        if self.poids_actuel + item.poids > self.capacite_max:
            print(f"❌ Impossible de ramasser {item.nom} : inventaire trop lourd !")
            return False

        self.items.append(item)
        print(f"🎒 {item.nom} ajouté à l'inventaire.")
        return True

    def retirer(self, item: Item):
        if item in self.items:
            self.items.remove(item)

    def afficher(self):
        print(f"\n=== Inventaire ({self.poids_actuel}/{self.capacite_max} kg) ===")
        if not self.items:
            print("  L'inventaire est vide.")
        for i, item in enumerate(self.items):
            print(
                f"  [{i}] {item.nom} (Valeur: {item.valeur} 🪙, Poids: {item.poids} kg)"
            )
        print("========================\n")
