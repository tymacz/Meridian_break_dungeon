from Evenements import EventBus


class VueConsole:
    def __init__(self):
        # On abonne la vue aux différents événements du jeu
        EventBus.s_abonner("attaque_physique", self.afficher_attaque_physique)
        EventBus.s_abonner("attaque_magique", self.afficher_attaque_magique)
        EventBus.s_abonner("changement_pv", self.afficher_changement_pv)

    def afficher_attaque_physique(self, donnees: dict):
        print(
            f"🗡️ {donnees['attaquant']} poignarde {donnees['cible']} pour {donnees['degats']} dégâts !"
        )

    def afficher_attaque_magique(self, donnees: dict):
        print(
            f"🔥 {donnees['attaquant']} lance une boule de feu sur {donnees['cible']} pour {donnees['degats']} dégâts !"
        )

    def afficher_changement_pv(self, donnees: dict):
        print(f"   -> Il reste {donnees['pv_restants']} PV à {donnees['cible']}.")
