import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
from datetime import datetime
import base64
from io import BytesIO

# Configuration de la page avec la charte FIAE
st.set_page_config(
    page_title="FIAE - Module 1 : Priorisation des Prestations",
    page_icon="🎯",
    layout="wide"
)

# CSS personnalisé selon la charte graphique FIAE
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Variables couleurs FIAE */
    :root {
        --bleu-sombre: #071827;
        --gris-metallique: #819394;
        --bleu-gris: #374A52;
        --gris-clair: #C3CBC8;
        --lime-green: #32CD32;
        --blanc-casse: #EAEDE4;
    }
    
    /* Style global */
    .stApp {
        font-family: 'Roboto', sans-serif;
        background-color: var(--blanc-casse);
    }
    
    /* Headers */
    h1 {
        color: var(--bleu-sombre) !important;
        font-size: 32px !important;
        font-weight: 500;
        border-bottom: 3px solid var(--lime-green);
        padding-bottom: 10px;
        margin-bottom: 30px;
    }
    
    h2 {
        color: var(--bleu-gris) !important;
        font-size: 24px !important;
        font-weight: 500;
    }
    
    h3 {
        color: var(--bleu-gris) !important;
        font-size: 20px !important;
    }
    
    /* Boutons */
    .stButton > button {
        background-color: var(--lime-green) !important;
        color: var(--bleu-sombre) !important;
        font-weight: 500;
        border: none;
        padding: 10px 24px;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #28a428 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Sliders */
    .stSlider > div > div {
        background-color: var(--gris-metallique);
    }
    
    .stSlider > div > div > div {
        background-color: var(--lime-green) !important;
    }
    
    /* Cards personnalisées */
    .prestation-card {
        background: white;
        border-left: 4px solid var(--lime-green);
        padding: 20px;
        margin: 15px 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, var(--bleu-gris) 0%, var(--bleu-sombre) 100%);
        color: white;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        margin: 10px 0;
    }
    
    .recommendation-box {
        background: linear-gradient(135deg, #32CD3210 0%, #32CD3220 100%);
        border: 2px solid var(--lime-green);
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
    }
    
    /* Progress indicators */
    .progress-step {
        display: inline-block;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background-color: var(--gris-metallique);
        color: white;
        text-align: center;
        line-height: 30px;
        margin: 0 10px;
    }
    
    .progress-step.active {
        background-color: var(--lime-green);
        color: var(--bleu-sombre);
    }
</style>
""", unsafe_allow_html=True)

# Initialisation de la session state
if 'prestations' not in st.session_state:
    st.session_state.prestations = []
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'first_time' not in st.session_state:
    st.session_state.first_time = True

# Header avec logo simulé
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #374A52 0%, #071827 100%); 
                padding: 20px; border-radius: 8px; text-align: center;">
        <h2 style="color: #32CD32 !important; margin: 0;">FIAE</h2>
        <small style="color: #C3CBC8;">Formation IA Entreprises</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.title("Module 1 : Priorisation des Prestations")
    st.markdown("**Objectif** : Identifier et prioriser vos prestations pour optimiser votre ROI avec l'IA")

# Progress bar
st.markdown("""
<div style="text-align: center; margin: 20px 0;">
    <span class="progress-step active">1</span>
    <span style="color: #819394;">━━━</span>
    <span class="progress-step">2</span>
    <span style="color: #819394;">━━━</span>
    <span class="progress-step">3</span>
</div>
""", unsafe_allow_html=True)

# Tabs pour organiser l'interface
tab1, tab2, tab3 = st.tabs(["📝 Saisie des Prestations", "📊 Analyse & Priorisation", "📥 Export"])

with tab1:
    st.markdown("### Étape 1 : Listez vos prestations principales")
    
    # Zone d'ajout de prestation
    with st.expander("➕ Ajouter une nouvelle prestation", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nom_prestation = st.text_input("Nom de la prestation", placeholder="Ex: Formation IA collective")
            recurrence = st.selectbox(
                "Récurrence",
                ["Quotidien", "Hebdomadaire", "Mensuel", "Annuel", "Variable"],
                help="À quelle fréquence réalisez-vous cette prestation ?"
            )
        
        with col2:
            st.markdown("#### Évaluations (0 = faible, 10 = élevé)")
            chronophage = st.slider("Aspect chronophage", 0, 10, 5, 
                                   help="Combien de temps cette prestation consomme-t-elle ?")
            rentabilite = st.slider("Rentabilité", 0, 10, 5,
                                   help="Quelle est la rentabilité de cette prestation ?")
            satisfaction = st.slider("Satisfaction client", 0, 10, 5,
                                    help="À quel point vos clients apprécient cette prestation ?")
        
        if st.button("Ajouter cette prestation", use_container_width=True):
            if nom_prestation:
                # Calcul du score avec pondération
                recurrence_score = {"Quotidien": 10, "Hebdomadaire": 7, "Mensuel": 4, "Annuel": 2, "Variable": 3}
                score = (recurrence_score[recurrence] * 3 + chronophage * 2 + rentabilite * 2 + satisfaction * 1) / 8
                
                nouvelle_prestation = {
                    "nom": nom_prestation,
                    "recurrence": recurrence,
                    "chronophage": chronophage,
                    "rentabilite": rentabilite,
                    "satisfaction": satisfaction,
                    "score": round(score, 2),
                    "priorite": "À définir"
                }
                
                st.session_state.prestations.append(nouvelle_prestation)
                st.success(f"✅ Prestation '{nom_prestation}' ajoutée avec succès!")
                st.rerun()
            else:
                st.error("Veuillez entrer un nom de prestation")
    
    # Affichage des prestations existantes
    if st.session_state.prestations:
        st.markdown("### 📋 Vos prestations enregistrées")
        
        for i, prestation in enumerate(st.session_state.prestations):
            with st.container():
                st.markdown(f"""
                <div class="prestation-card">
                    <h4 style="color: #071827; margin-bottom: 10px;">{prestation['nom']}</h4>
                    <div style="display: flex; justify-content: space-between; color: #374A52;">
                        <span>📅 {prestation['recurrence']}</span>
                        <span>⏱️ Chrono: {prestation['chronophage']}/10</span>
                        <span>💰 Rentabilité: {prestation['rentabilite']}/10</span>
                        <span>😊 Satisfaction: {prestation['satisfaction']}/10</span>
                        <span style="color: #32CD32; font-weight: bold;">Score: {prestation['score']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🗑️ Supprimer", key=f"del_{i}"):
                    st.session_state.prestations.pop(i)
                    st.rerun()

with tab2:
    if st.session_state.prestations:
        st.markdown("### 🎯 Analyse de vos prestations")
        
        # Calcul des recommandations
        df = pd.DataFrame(st.session_state.prestations)
        
        # Matrice Effort vs Impact
        fig = go.Figure()
        
        for _, row in df.iterrows():
            effort = row['chronophage']
            impact = (row['rentabilite'] + row['satisfaction']) / 2
            
            # Détermination de la couleur selon le quadrant
            if effort <= 5 and impact >= 5:
                color = '#32CD32'  # Quick wins
                quadrant = "Quick Win"
            elif effort > 5 and impact >= 5:
                color = '#071827'  # Projets majeurs
                quadrant = "Projet Majeur"
            elif effort <= 5 and impact < 5:
                color = '#819394'  # Fill-ins
                quadrant = "À reconsidérer"
            else:
                color = '#374A52'  # Temps perdus
                quadrant = "À optimiser"
            
            fig.add_trace(go.Scatter(
                x=[effort],
                y=[impact],
                mode='markers+text',
                name=row['nom'],
                text=[row['nom']],
                textposition="top center",
                marker=dict(size=20, color=color),
                hovertemplate=f"<b>{row['nom']}</b><br>Effort: {effort}<br>Impact: {impact}<br>Quadrant: {quadrant}<extra></extra>"
            ))
        
        fig.update_layout(
            title="Matrice Effort vs Impact",
            xaxis_title="Effort (Aspect chronophage)",
            yaxis_title="Impact (Rentabilité + Satisfaction)",
            height=500,
            showlegend=False,
            plot_bgcolor='#EAEDE4',
            xaxis=dict(range=[0, 10], gridcolor='#C3CBC8'),
            yaxis=dict(range=[0, 10], gridcolor='#C3CBC8'),
            shapes=[
                dict(type="line", x0=5, y0=0, x1=5, y1=10, line=dict(color="#819394", width=2, dash="dash")),
                dict(type="line", x0=0, y0=5, x1=10, y1=5, line=dict(color="#819394", width=2, dash="dash"))
            ],
            annotations=[
                dict(x=2.5, y=7.5, text="Quick Wins", showarrow=False, font=dict(color="#32CD32", size=14, family="Roboto")),
                dict(x=7.5, y=7.5, text="Projets Majeurs", showarrow=False, font=dict(color="#071827", size=14, family="Roboto")),
                dict(x=2.5, y=2.5, text="À reconsidérer", showarrow=False, font=dict(color="#819394", size=14, family="Roboto")),
                dict(x=7.5, y=2.5, text="À optimiser", showarrow=False, font=dict(color="#374A52", size=14, family="Roboto"))
            ]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommandations personnalisées
        st.markdown("### 🤖 Recommandations IA")
        
        # Tri par score pour recommandations
        df_sorted = df.sort_values('score', ascending=False)
        
        # Déterminer si c'est la première fois
        if st.session_state.first_time:
            # Recommander une prestation facile mais représentative
            prestations_faciles = df[df['chronophage'] <= 5].sort_values('score', ascending=False)
            if not prestations_faciles.empty:
                recommandation = prestations_faciles.iloc[0]
                st.markdown(f"""
                <div class="recommendation-box">
                    <h3 style="color: #071827;">🎯 Recommandation pour débuter</h3>
                    <p><strong>Commencez par : {recommandation['nom']}</strong></p>
                    <p>Cette prestation est idéale pour votre première cartographie car :</p>
                    <ul>
                        <li>Effort modéré (chronophage : {recommandation['chronophage']}/10)</li>
                        <li>Impact significatif (rentabilité : {recommandation['rentabilite']}/10)</li>
                        <li>Processus représentatif de vos activités</li>
                    </ul>
                    <p style="color: #32CD32; font-weight: bold;">
                        💡 Conseil : Maîtrisez d'abord cette cartographie simple avant de vous attaquer aux processus complexes.
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Recommander la prestation avec le meilleur score
            top_prestation = df_sorted.iloc[0]
            st.markdown(f"""
            <div class="recommendation-box">
                <h3 style="color: #071827;">🏆 Prestation prioritaire</h3>
                <p><strong>Focalisez-vous sur : {top_prestation['nom']}</strong></p>
                <p>Score global : {top_prestation['score']}/10</p>
                <p>Cette prestation offre le meilleur potentiel de ROI avec l'automatisation IA.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Métriques globales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: white !important;">Total Prestations</h3>
                <h1 style="color: #32CD32 !important;">{}</h1>
            </div>
            """.format(len(df)), unsafe_allow_html=True)
        
        with col2:
            avg_chrono = df['chronophage'].mean()
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: white !important;">Charge Moyenne</h3>
                <h1 style="color: #32CD32 !important;">{:.1f}/10</h1>
            </div>
            """.format(avg_chrono), unsafe_allow_html=True)
        
        with col3:
            avg_rentabilite = df['rentabilite'].mean()
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: white !important;">Rentabilité Moy.</h3>
                <h1 style="color: #32CD32 !important;">{:.1f}/10</h1>
            </div>
            """.format(avg_rentabilite), unsafe_allow_html=True)
        
        with col4:
            quick_wins = len(df[(df['chronophage'] <= 5) & (df['rentabilite'] >= 5)])
            st.markdown("""
            <div class="metric-card">
                <h3 style="color: white !important;">Quick Wins</h3>
                <h1 style="color: #32CD32 !important;">{}</h1>
            </div>
            """.format(quick_wins), unsafe_allow_html=True)
    else:
        st.info("👈 Commencez par ajouter vos prestations dans l'onglet 'Saisie des Prestations'")

with tab3:
    if st.session_state.prestations:
        st.markdown("### 📥 Export des données")
        
        df_export = pd.DataFrame(st.session_state.prestations)
        
        # Export CSV
        csv = df_export.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📄 Télécharger en CSV",
            data=csv,
            file_name=f"FIAE_prestations_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
        
        # Export JSON pour l'étape suivante
        json_data = json.dumps(st.session_state.prestations, ensure_ascii=False, indent=2)
        st.download_button(
            label="🔗 Export JSON (pour Module 2)",
            data=json_data,
            file_name=f"FIAE_prestations_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )
        
        # Aperçu des données
        st.markdown("### 👁️ Aperçu des données")
        st.dataframe(df_export, use_container_width=True)
        
        # Bouton pour passer au module suivant
        st.markdown("---")
        if st.button("Continuer vers le Module 2 →", use_container_width=True):
            st.info("Le Module 2 (Détail des processus) sera bientôt disponible. Vos données ont été sauvegardées.")
    else:
        st.info("Aucune prestation à exporter. Ajoutez d'abord des prestations.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #819394; padding: 20px;">
    <p>FIAE - Formation IA Entreprises | Module 1 v1.0</p>
    <p style="font-size: 12px;">Méthode In Astra - Optimisation par l'IA</p>
</div>
""", unsafe_allow_html=True)