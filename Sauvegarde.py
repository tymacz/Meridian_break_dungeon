import json
import os
from Personnages import Personnage
from Roles import Thief, Mage
from Items import Potion, Arme, Materiel


class SaveManager:
    FICHIER_SAUVEGARDE = "savegame.json"

    @staticmethod
    def sauvegarder(personnage: Personnage):
        with open(SaveManager.FICHIER_SAUVEGARDE, "w", encoding="utf-8") as f:
            # json.dump convertit le dictionnaire en texte formaté
            json.dump(personnage.to_dict(), f, indent=4, ensure_ascii=False)
        print("💾 Partie sauvegardée avec succès !")

    @staticmethod
    def charger() -> Personnage:
        if not os.path.exists(SaveManager.FICHIER_SAUVEGARDE):
            print("❌ Aucune sauvegarde trouvée.")
            return None

        with open(SaveManager.FICHIER_SAUVEGARDE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 1. Reconstruire le Rôle
        role_data = data["role"]
        if role_data["type"] == "Thief":
            role = Thief()
        else:
            role = Mage()

        # Restaurer les stats exactes du rôle sauvegardé (en cas de level up)
        role.pv = role_data["pv"]
        role.attack = role_data["attack"]
        role.defense = role_data["defense"]

        # 2. Reconstruire le Personnage
        personnage = Personnage(name=data["name"], role=role)
        personnage.level = data["level"]
        personnage.exp = data["exp"]
        personnage.money = data["money"]

        # 3. Reconstruire l'Inventaire via la Factory
        for item_data in data["inventaire"]:
            if item_data["type"] == "Potion":
                item = Potion(
                    nom=item_data["nom"],
                    poids=item_data["poids"],
                    valeur=item_data["valeur"],
                    soin=item_data["soin"],
                )
            elif item_data["type"] == "Arme":
                item = Arme(
                    nom=item_data["nom"],
                    poids=item_data["poids"],
                    valeur=item_data["valeur"],
                    degats_bonus=item_data["degats_bonus"],
                )
            else:
                item = Materiel(
                    nom=item_data["nom"],
                    poids=item_data["poids"],
                    valeur=item_data["valeur"],
                )

            personnage.inventaire.ajouter(item)

        print(
            f"✅ Partie chargée : Bon retour, {personnage.name} (Niveau {personnage.level}) !"
        )
        return personnage
