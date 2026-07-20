from datetime import datetime
import os
import pandas as pd

# 1. Configuration de la structure des cuisines et des friteuses
PARC_FRITEUSES = {
    "Cuisine Centrale": ["CC-F1", "CC-F2", "CC-F3", "CC-F4"],
    "Cuisine Canastel": ["KC-F1", "KC-F2"],
    "Room Service": ["RS-F1", "RS-F2"],
    "Aqua": ["AQ-F1", "AQ-F2"],
}

FICHIER_SUIVI = "suivi_huiles_friture.xlsx"
SEUIL_CRITIQUE_CP = 25.0  # Seuil réglementaire des composés polaires


def initialiser_fichier():
    """Crée le fichier Excel avec les bonnes colonnes s'il n'existe pas."""
    if not os.path.exists(FICHIER_SUIVI):
        colonnes = [
            "Date",
            "Cuisine",
            "Code Friteuse",
            "Composes Polaires (%)",
            "Etat Visuel",
            "Action Menee",
            "Huile Neuve Ajoutee (L)",
            "Huile Usee Vidangee (L)",
            "Operateur",
            "Statut Huile",
        ]
        df = pd.DataFrame(columns=colonnes)
        df.to_excel(FICHIER_SUIVI, index=False)
        print(f"Fichier '{FICHIER_SUIVI}' initialisé avec succès.")


def enregistrer_controle(donnees):
    """Ajoute une nouvelle ligne de contrôle dans le fichier Excel."""
    df = pd.read_excel(FICHIER_SUIVI)
    # Conversion de la saisie en DataFrame
    nouvelle_ligne = pd.DataFrame([donnees])
    # Ajout au fichier existant
    df = pd.concat([df, nouvelle_ligne], ignore_index=False)
    df.to_excel(FICHIER_SUIVI, index=False)
    print("\n[SUCCÈS] Contrôle enregistré dans le fichier Excel !")


def menu_saisie():
    """Interface utilisateur pour saisir un contrôle quotidien."""
    print("\n--- NOUVEAU CONTRÔLE HUILE DE FRITURE ---")

    # Sélection de la cuisine
    cuisines = list(PARC_FRITEUSES.keys())
    for i, cuisine in enumerate(cuisines, 1):
        print(f"{i}. {cuisine}")

    choix_cuisine = (
        int(input("Sélectionnez la cuisine (numéro) : ")) - 1
    )
    cuisine_selectionnee = cuisines[choix_cuisine]

    # Sélection de la friteuse
    friteuses = PARC_FRITEUSES[cuisine_selectionnee]
    for i, friteuse in enumerate(friteuses, 1):
        print(f"{i}. {friteuse}")

    choix_friteuse = (
        int(input("Sélectionnez la friteuse (numéro) : ")) - 1
    )
    friteuse_selectionnee = friteuses[choix_friteuse]

    # Saisie des mesures
    cp = float(
        input("Taux de composés polaires en % (ex: 14.5) : ")
    )
    visuel = input(
        "État visuel (Correct / Mousse / Sombre) : "
    )
    operateur = input("Nom de l'opérateur : ")

    # Logique automatique selon le taux de composés polaires
    if cp >= SEUIL_CRITIQUE_CP:
        print(
            f"\n⚠ ALERTE : Le taux ({cp}%) dépasse le seuil critique de {SEUIL_CRITIQUE_CP}% !"
        )
        print("-> Action requise : VIDANGE TOTALE IMMÉDIATE.")
        action = "Vidange totale"
        statut = "CRITIQUE (À changer)"
        hu_vidangee = float(
            input("Quantité d'huile usée vidangée en Litres : ")
        )
        hn_ajoutee = float(
            input("Quantité d'huile neuve réintroduite en Litres : ")
        )
    else:
        print(f"\nTaux correct ({cp}%).")
        statut = "Conforme"
        choix_action = input(
            "Action menée ? (Rien / Filtration / Appoint) : "
        )
        action = choix_action
        hn_ajoutee = 0.0
        hu_vidangee = 0.0
        if choix_action.lower() == "appoint":
            hn_ajoutee = float(
                input("Quantité d'huile neuve ajoutée (L) : ")
            )

    # Préparation du dictionnaire de données
    donnees_controle = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Cuisine": cuisine_selectionnee,
        "Code Friteuse": friteuse_selectionnee,
        "Composes Polaires (%)": cp,
        "Etat Visuel": visuel,
        "Action Menee": action,
        "Huile Neuve Ajoutee (L)": hn_ajoutee,
        "Huile Usee Vidangee (L)": hu_vidangee,
        "Operateur": operateur,
        "Statut Huile": statut,
    }

    enregistrer_controle(donnees_controle)


# --- PROGRAMME PRINCIPAL ---
if __name__ == "__main__":
    initialiser_fichier()

    while True:
        print("\n==========================================")
        print("  GESTION DES HUILES - CUISINES CENTRALES ")
        print("==========================================")
        print("1. Saisir un contrôle de friteuse")
        print("2. Voir l'historique des contrôles")
        print("3. Quitter")

        choix = input("Votre choix : ")

        if choix == "1":
            menu_saisie()
        elif choix == "2":
            if os.path.exists(FICHIER_SUIVI):
                df = pd.read_excel(FICHIER_SUIVI)
                if df.empty:
                    print("\nAucun historique disponible pour le moment.")
                else:
                    print("\n--- HISTORIQUE DES ENREGISTREMENTS ---")
                    print(df.tail(10).to_string())  # Affiche les 10 derniers
            else:
                print("\nAucun fichier trouvé.")
        elif choix == "3":
            print("Fermeture du programme.")
            break
        else:
            print("Option invalide, veuillez recommencer.")# huile-de-friture-
pour faire le suivi des huiles des friteuses 
