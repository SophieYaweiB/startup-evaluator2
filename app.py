import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Test d'idée Startup", layout="wide")
st.title("🚀 Teste ton Idée de Startup")

st.markdown("""
Cette application t’aide à évaluer ton idée selon 5 grands axes :
- **Marché**
- **Produit**
- **Traction**
- **Exécution**
- **Alignement personnel**

Chaque critère est noté de **0 à 2** :
- 0 = Non / Pas du tout prêt
- 1 = Moyennement / À valider
- 2 = Oui / Validé ou fort
""")

# --------- CRITÈRES ----------
criteria = [
    # Marché
    ("🧲 Besoin clair du marché", "Est-ce un problème réel et fréquent pour un segment identifié ?"),
    ("📈 Taille du marché", "Le marché est-il suffisamment grand ou en croissance ?"),
    ("🏹 Accessibilité", "Peux-tu atteindre tes clients facilement ?"),

    # Produit
    ("🛠️ MVP rapide possible", "Peux-tu lancer une version testable en moins de 30 jours ?"),
    ("💡 Proposition de valeur claire", "Ta solution est-elle différenciante ?"),

    # Traction
    ("📊 Premiers retours utilisateurs", "As-tu eu des retours concrets de vrais utilisateurs ?"),
    ("💬 Intérêt / engagements", "As-tu une liste d'attente, des RDVs, ou un début de communauté ?"),

    # Exécution
    ("🧠 Compétences clés internes", "Les compétences nécessaires sont-elles disponibles ?"),
    ("🧪 Capacité à tester rapidement", "Peux-tu faire des tests terrain en 7-15 jours ?"),

    # Alignement
    ("🔥 Motivation personnelle", "Es-tu personnellement motivée et alignée avec le problème ?"),
    ("💖 Affinité avec les utilisateurs", "Tu connais bien leur quotidien / frustrations ?"),
]

# --------- SLIDERS ----------
scores = {}
cols = st.columns(2)
for i, (title, description) in enumerate(criteria):
    col = cols[i % 2]
    with col:
        with st.expander(title):
            st.markdown(f"_{description}_")
            scores[title] = st.slider("Score", 0, 2, 1, key=title)

# --------- ANALYSE ----------
st.markdown("## 📊 Résultats")

total_score = sum(scores.values())
max_score = len(scores) * 2
percent = total_score / max_score

st.markdown(f"### Score global : **{total_score} / {max_score}** ({int(percent * 100)}%)")

if percent >= 0.8:
    st.success("💚 Fort potentiel ! Prête à être lancée ou présentée.")
elif percent >= 0.6:
    st.info("🟡 Bonne base. Tu peux consolider quelques points avant de te lancer.")
elif percent >= 0.4:
    st.warning("🟠 L'idée mérite plus de validation.")
else:
    st.error("🔴 Trop d'incertitudes. Travaille certains fondamentaux.")

# --------- VISUALISATION ----------
st.markdown("## 📈 Visualisation radar")

sections = {
    "Marché": criteria[0:3],
    "Produit": criteria[3:5],
    "Traction": criteria[5:7],
    "Exécution": criteria[7:9],
    "Alignement": criteria[9:11]
}

section_scores = {}
for sec, crits in sections.items():
    s = sum(scores[c[0]] for c in crits)
    section_scores[sec] = s / (2 * len(crits))

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=list(section_scores.values()) + [list(section_scores.values())[0]],
    theta=list(section_scores.keys()) + [list(section_scores.keys())[0]],
    fill='toself',
    name='Évaluation'
))
fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)

# --------- BOUTON RESET ----------
if st.button("🔄 Nouvelle idée / Réinitialiser"):
    st.experimental_rerun()
