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

        st.dataframe(df_filtre.style.map(colorer_statut, subset=["Statut"]), use_container_width=True)
        
        # Bouton de téléchargement du fichier Excel propre
        with open(FICHIER_SUIVI, "rb") as f:
            st.download_button(
                label="📥 Télécharger le registre complet (Excel)",
                data=f,
                file_name=f"registre_huiles_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
