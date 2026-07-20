import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuration de la page
st.set_page_config(page_title="Suivi des Huiles de Friture", layout="wide")

# Configuration du parc de friteuses
PARC_FRITEUSES = {
    "Cuisine Centrale": ["CC-F1", "CC-F2", "CC-F3", "CC-F4"],
    "Cuisine Canastel": ["KC-F1", "KC-F2"],
    "Room Service": ["RS-F1", "RS-F2"],
    "Aqua": ["AQ-F1", "AQ-F2"]
}

FICHIER_SUIVI = "suivi_huiles_friture.xlsx"
SEUIL_CRITIQUE_CP = 25.0

# Initialisation du fichier Excel de stockage
if not os.path.exists(FICHIER_SUIVI):
    colonnes = [
        "Date", "Cuisine", "Code Friteuse", "Composes Polaires (%)", 
        "Etat Visuel", "Action Menee", "Huile Neuve Ajoutee (L)", 
        "Huile Usee Vidangee (L)", "Operateur", "Statut"
    ]
    pd.DataFrame(columns=colonnes).to_excel(FICHIER_SUIVI, index=False)

# Titre de l'application
st.title("🧪 Gestion & Suivi des Huiles de Friture")
st.markdown("---")

# Création de deux onglets : Saisie et Historique
tab1, tab2 = st.tabs(["📋 Saisie un Contrôle", "📊 Historique & Données"])

# --- ONGLET 1 : FORMULAIRE DE SAISIE ---
with tab1:
    st.header("Nouvel enregistrement")
    
    with st.form("form_controle", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            cuisine = st.selectbox("Sélectionnez la cuisine", list(PARC_FRITEUSES.keys()))
            # Filtre dynamique des friteuses selon la cuisine choisie
            friteuse = st.selectbox("Sélectionnez la friteuse", PARC_FRITEUSES[cuisine])
            operateur = st.text_input("Nom de l'opérateur / Cuisinier")
            visuel = st.selectbox("État visuel de l'huile", ["Correct", "Mousse", "Sombre / Épaisse"])
            
        with col2:
            cp = st.number_input("Taux de composés polaires (%)", min_value=0.0, max_value=100.0, step=0.1, value=10.0)
            
            # Logique dynamique basée sur le taux de composés polaires
            if cp >= SEUIL_CRITIQUE_CP:
                st.error(f"⚠️ Alerte : {cp}% dépasse le seuil critique ({SEUIL_CRITIQUE_CP}%). VIDANGE OBLIGATOIRE !")
                action = "Vidange totale"
                hu_vidangee = st.number_input("Quantité d'huile usée vidangée (Litres)", min_value=0.0, step=1.0)
                hn_ajoutee = st.number_input("Quantité d'huile neuve réintroduite (Litres)", min_value=0.0, step=1.0)
                statut = "CRITIQUE (Vidangée)"
            else:
                st.success(f"✅ Taux conforme ({cp}%).")
                action = st.selectbox("Action menée", ["Rien (Conforme)", "Filtration", "Appoint (Ajout d'huile)"])
                hu_vidangee = 0.0
                if action == "Appoint (Ajout d'huile)":
                    hn_ajoutee = st.number_input("Quantité d'huile neuve ajoutée (Litres)", min_value=0.0, step=1.0)
                else:
                    hn_ajoutee = 0.0
                statut = "Conforme"

        # Bouton de soumission du formulaire
        soumis = st.form_submit_button("Enregistrer le contrôle")
        
        if soumis:
            if not operateur.strip():
                st.warning("Veuillez renseigner le nom de l'opérateur avant de valider.")
            else:
                # Préparation des données
                nouvelle_entree = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Cuisine": cuisine,
                    "Code Friteuse": friteuse,
                    "Composes Polaires (%)": cp,
                    "Etat Visuel": visuel,
                    "Action Menee": action,
                    "Huile Neuve Ajoutee (L)": hn_ajoutee,
                    "Huile Usee Vidangee (L)": hu_vidangee,
                    "Operateur": operateur,
                    "Statut": statut
                }
                
                # Sauvegarde dans Excel
                df_existant = pd.read_excel(FICHIER_SUIVI)
                df_nouveau = pd.concat([df_existant, pd.DataFrame([nouvelle_entree])], ignore_index=True)
                df_nouveau.to_excel(FICHIER_SUIVI, index=False)
                st.balloons()
                st.success(f"Le contrôle pour la friteuse {friteuse} a bien été enregistré !")

# --- ONGLET 2 : HISTORIQUE ET VISUALISATION ---
with tab2:
    st.header("Historique des contrôles")
    
    # Rechargement des données
    df_suivi = pd.read_excel(FICHIER_SUIVI)
    
    if df_suivi.empty:
        st.info("Aucun enregistrement trouvé pour le moment.")
    else:
        # Filtres rapides
        filtre_cuisine = st.multiselect("Filtrer par cuisine", options=df_suivi["Cuisine"].unique(), default=df_suivi["Cuisine"].unique())
        df_filtre = df_suivi[df_suivi["Cuisine"].isin(filtre_cuisine)]
        
        # Coloration du tableau pour repérer les alertes
        def colorer_statut(val):
            color = 'background-color: #ffcccc; color: black' if 'CRITIQUE' in str(val) else 'background-color: #ccffcc; color: black'
            return color

        st.dataframe(df_filtre.style.applymap(colorer_statut, subset=["Statut"]), use_container_width=True)
        
        # Bouton de téléchargement du fichier Excel propre
        with open(FICHIER_SUIVI, "rb") as f:
            st.download_button(
                label="📥 Télécharger le registre complet (Excel)",
                data=f,
                file_name=f"registre_huiles_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
