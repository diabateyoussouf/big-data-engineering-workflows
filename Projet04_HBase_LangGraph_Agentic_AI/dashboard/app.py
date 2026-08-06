import os
import happybase
import pandas as pd
import plotly.express as px
import streamlit as st
from langchain_core.messages import HumanMessage

# Import du graphe LangGraph Agentic AI (Tool Calling & RAG)
from Projet04_HBase_LangGraph_Agentic_AI.agents.rag_graph import build_rag_graph

st.set_page_config(
    page_title="HBase NoSQL Feature Store & LangGraph AI",
    page_icon="⚡",
    layout="wide"
)

HBASE_HOST = "localhost"
HBASE_PORT = 9090
TABLE_NAME = "retail_feature_store"
DATA_PATH = "Projet04_HBase_LangGraph_Agentic_AI/data/purchases.txt"

@st.cache_resource
def load_rag_agent():
    """Charge et met en cache l'instance du graphe LangGraph Agentic AI."""
    return build_rag_graph()

@st.cache_data(ttl=60)
def fetch_hbase_data():
    """Tente de lire la table HBase via HappyBase, sinon bascule sur le fallback local."""
    try:
        connection = happybase.Connection(host=HBASE_HOST, port=HBASE_PORT, timeout=3000)
        connection.open()
        table = connection.table(TABLE_NAME)

        records = []
        for row_key, data in table.scan():
            row_dict = {"city": row_key.decode("utf-8")}
            for col_name, val in data.items():
                row_dict[col_name.decode("utf-8")] = val.decode("utf-8")
            records.append(row_dict)

        connection.close()
        df = pd.DataFrame(records)
        return df, "HBase (Docker Thrift Server)"

    except Exception:
        actual_path = DATA_PATH if os.path.exists(DATA_PATH) else "data/purchases.txt"
        if os.path.exists(actual_path):
            cols = ["date", "time", "city", "category", "amount", "payment"]
            raw_df = pd.read_csv(actual_path, sep="\t", names=cols, header=None)
            raw_df["amount"] = pd.to_numeric(raw_df["amount"], errors="coerce").fillna(0.0)
            
            grouped = raw_df.groupby("city")
            records = []
            for city, group in grouped:
                cat_sum = group.groupby("category")["amount"].sum()
                pmt_counts = group["payment"].value_counts().to_dict()
                records.append({
                    "city": city,
                    "sales:total_revenue": str(round(group["amount"].sum(), 2)),
                    "sales:avg_transaction": str(round(group["amount"].mean(), 2)),
                    "sales:transaction_count": str(len(group)),
                    "categories:top_category": cat_sum.idxmax() if not cat_sum.empty else "N/A",
                    "categories:top_category_revenue": str(round(cat_sum.max(), 2)) if not cat_sum.empty else "0",
                    "payments:card_count": str(pmt_counts.get("Visa", 0) + pmt_counts.get("MasterCard", 0)),
                    "payments:cash_count": str(pmt_counts.get("Cash", 0)),
                    "payments:paypal_count": str(pmt_counts.get("PayPal", 0)),
                })
            return pd.DataFrame(records), "Mode Démo Cloud (Dataset local)"
        return pd.DataFrame(), "Aucune source disponible"

# --- BARRE LATÉRALE PÉDAGOGIQUE ---
with st.sidebar:
    st.title("⚙️ Architecture & Status")
    
    df, source_mode = fetch_hbase_data()
    
    if "HBase" in source_mode:
        st.success(f"🟢 **Connecté à Apache HBase**\n\n*(Port Thrift : {HBASE_PORT})*")
    else:
        st.warning(f"🟡 **{source_mode}**")

    st.markdown("---")
    st.subheader("📚 Qu'est-ce qu'un Feature Store ?")
    st.info(
        "C'est un réservoir de données à **ultra-faible latence** conçu pour servir des indicateurs pré-calculés en temps réel aux applications web et agents IA."
    )
    st.markdown(
        "**Structure de la table HBase :**\n"
        "- **Table :** `retail_feature_store`\n"
        "- **RowKey (Clé) :** `city` (Ex: *Baltimore*)\n"
        "- **Column Families :**\n"
        "  - `sales:` Indicateurs financiers\n"
        "  - `categories:` Tops ventes\n"
        "  - `payments:` Modes de règlement"
    )
    st.markdown("---")
    st.caption("🚀 Projet 04 — Big Data Engineering Workflows")

# --- EN-TÊTE ET PRESENTATION ---
st.title("⚡ Apache HBase NoSQL Feature Store & Agentic AI")
st.caption("Plateforme de restitution d'indicateurs métiers distribués & Agent Autonome LangGraph.")

# --- BLOC D'EXPLICATION POUR LE VISITEUR ---
with st.expander("💡 **Comprendre cette application en 1 minute (Guide du visiteur)**", expanded=False):
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        st.markdown(
            "#### 🎯 Le Cas d'Usage Métier\n"
            "Cette interface analyse **200 000 transactions réelles** réparties sur 103 villes. "
            "Les données brutes ont été agrégées pour calculer le Chiffre d'Affaires, "
            "la catégorie dominante et les habitudes de paiement par région."
        )
    with col_exp2:
        st.markdown(
            "#### 🛠️ Pourquoi utiliser Apache HBase (NoSQL) ?\n"
            "Contrairement à une base relationnelle (SQL) qui devient lente avec des millions de lignes, "
            "**HBase (orienté colonnes)** permet d'extraire l'ensemble des métriques d'une ville "
            "en **moins de 2 millisecondes** grâce à sa clé d'accès directe (*RowKey*)."
        )

st.markdown("---")

if df.empty:
    st.error("❌ Aucune donnée disponible. Vérifiez le conteneur HBase ou le fichier data/purchases.txt.")
    st.stop()

# Nettoyage et typage numérique
num_cols = [
    "sales:total_revenue", "sales:avg_transaction", "sales:transaction_count",
    "categories:top_category_revenue", "payments:card_count", "payments:cash_count", "payments:paypal_count"
]
for col in num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# --- VALEURS CLÉS GLOBALES ---
st.subheader("📌 Indicateurs Clés Globaux (Feature Store Summary)")
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Villes Référencées (RowKeys)",
    value=f"{len(df):,}",
    help="Nombre de clés uniques (RowKeys) enregistrées dans le cluster HBase."
)
col2.metric(
    label="Chiffre d'Affaires Total",
    value=f"{df['sales:total_revenue'].sum():,.2f} €",
    help="Somme cumulée de la famille de colonnes sales:total_revenue sur toutes les villes."
)
col3.metric(
    label="Transactions Traitées",
    value=f"{int(df['sales:transaction_count'].sum()):,}",
    help="Nombre total de transactions analysées à partir du jeu de données réel."
)
col4.metric(
    label="Panier Moyen Global",
    value=f"{df['sales:avg_transaction'].mean():,.2f} €",
    help="Moyenne des paniers moyens par ville (famille de colonnes sales:avg_transaction)."
)

st.markdown("<br>", unsafe_allow_html=True)

# --- ONGLETS D'EXPLORATION INTERACTIFS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Performances par Ville", 
    "💳 Modes de Paiement", 
    "🔎 Inspecteur NoSQL (RowKey Lookup)",
    "🤖 Agent IA (LangGraph Tool Calling)"
])

with tab1:
    st.markdown("### 📊 Analyse des Revenus & Domination par Catégorie")
    st.caption("Visualisation des métriques extraites des familles de colonnes `sales:` et `categories:`")
    
    c_left, c_right = st.columns(2)
    with c_left:
        top_cities = df.nlargest(10, "sales:total_revenue")
        fig_rev = px.bar(
            top_cities, 
            x="sales:total_revenue", 
            y="city", 
            orientation="h",
            title="<b>Top 10 Villes par Chiffre d'Affaires (€)</b>",
            labels={"sales:total_revenue": "Chiffre d'Affaires (€)", "city": "Ville (RowKey HBase)"},
            color="sales:total_revenue", 
            color_continuous_scale="Viridis"
        )
        fig_rev.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_rev, use_container_width=True)

    with c_right:
        top_cats = df["categories:top_category"].value_counts().reset_index()
        top_cats.columns = ["Catégorie", "Nombre de Villes"]
        fig_cat = px.pie(
            top_cats, 
            names="Catégorie", 
            values="Nombre de Villes",
            title="<b>Répartition des Catégories №1 par Ville</b>",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_cat, use_container_width=True)

with tab2:
    st.markdown("### 💳 Analyse des Volumes de Paiement")
    st.caption("Données extraites de la famille de colonnes `payments:` (`card_count`, `cash_count`, `paypal_count`)")
    
    total_cards = df["payments:card_count"].sum()
    total_cash = df["payments:cash_count"].sum()
    total_paypal = df["payments:paypal_count"].sum()
    
    pmt_df = pd.DataFrame({
        "Moyen de Paiement": ["Carte Bancaire (Visa/MC)", "Espèces (Cash)", "PayPal"],
        "Nombre de Transactions": [total_cards, total_cash, total_paypal]
    })
    
    fig_pmt = px.bar(
        pmt_df, 
        x="Moyen de Paiement", 
        y="Nombre de Transactions", 
        color="Moyen de Paiement",
        title="<b>Répartition Globale des Moyens de Règlement</b>",
        text_auto=True,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_pmt, use_container_width=True)

with tab3:
    st.markdown("### 🔎 Inspection Directe d'une Clé de Ligne NoSQL (RowKey)")
    st.info("Sélectionnez une ville pour simuler une requête instantanée (`Get RowKey`) et observer l'organisation des **Column Families** sous forme clé-valeur.")
    
    selected_city = st.selectbox("🎯 Choisir une ville à interroger (RowKey) :", sorted(df["city"].unique()))
    
    city_data = df[df["city"] == selected_city].iloc[0].to_dict()
    
    st.markdown(f"#### Données HBase associées à la clé : `{selected_city}`")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.success("##### 🏬 Famille `sales:`")
        st.write(f"- **total_revenue :** `{float(city_data.get('sales:total_revenue', 0)):,} €`")
        st.write(f"- **avg_transaction :** `{float(city_data.get('sales:avg_transaction', 0)):,} €`")
        st.write(f"- **transaction_count :** `{city_data.get('sales:transaction_count')} tx`")

    with col_f2:
        st.info("##### 🏷️ Famille `categories:`")
        st.write(f"- **top_category :** `{city_data.get('categories:top_category')}`")
        st.write(f"- **top_category_revenue :** `{float(city_data.get('categories:top_category_revenue', 0)):,} €`")

    with col_f3:
        st.warning("##### 💳 Famille `payments:`")
        st.write(f"- **card_count :** `{city_data.get('payments:card_count')} tx`")
        st.write(f"- **cash_count :** `{city_data.get('payments:cash_count')} tx`")
        st.write(f"- **paypal_count :** `{city_data.get('payments:paypal_count')} tx`")

# --- ONGLET 4 : INTEGRATION LANGGRAPH AGENTIC AI (TOOL CALLING) ---
with tab4:
    st.markdown("### 🤖 Agent IA Autonome Orchestré par LangGraph (Tool Calling & RAG)")
    st.caption("L'agent analyse votre question et choisit dynamiquement d'exécuter un outil HBase ou de consulter la base RAG.")

    mistral_key_input = st.text_input("🔑 Clé API Mistral AI (optionnel si définie dans .env) :", type="password")
    if mistral_key_input:
        os.environ["MISTRAL_API_KEY"] = mistral_key_input

    if "rag_messages" not in st.session_state:
        st.session_state.rag_messages = [
            {"role": "assistant", "content": "Bonjour ! Je suis votre Agent IA Feature Store. Posez-moi une question sur les performances des villes (HBase) ou sur la documentation du projet."}
        ]
    if "session_thread_id" not in st.session_state:
        st.session_state.session_thread_id = "streamlit_session_1"

    for msg in st.session_state.rag_messages:
        st.chat_message(msg["role"]).write(msg["content"])

    user_query = st.chat_input("Ex: Quel magasin ou quelle ville a effectué le plus de ventes ?")
    
    if user_query:
        st.session_state.rag_messages.append({"role": "user", "content": user_query})
        st.chat_message("user").write(user_query)

        with st.spinner("🧠 Agent IA : Décision de l'outil & Requête HBase / ChromaDB..."):
            try:
                agent_app = load_rag_agent()
                config = {"configurable": {"thread_id": st.session_state.session_thread_id}}

                # Transmettre le message au format attendu par le graphe LangGraph avec Tool Calling
                inputs = {"messages": [HumanMessage(content=user_query)]}
                result = agent_app.invoke(inputs, config=config)

                # Extraction de la réponse générée par l'agent
                last_message = result["messages"][-1]
                answer = last_message.content

                st.session_state.rag_messages.append({"role": "assistant", "content": answer})
                st.chat_message("assistant").write(answer)

            except Exception as err:
                st.error(f"❌ Erreur lors de l'exécution de l'agent LangGraph : {str(err)}")