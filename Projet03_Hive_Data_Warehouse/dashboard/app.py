import streamlit as st
import duckdb
import plotly.express as px
import pandas as pd
import time
import os

# --- Configuration de la page ---
st.set_page_config(
    page_title="HiveQL Data Warehouse & Business Intelligence",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Styling CSS Avancé ---
st.markdown("""
<style>
    /* Cartes de métriques KPI */
    .metric-card {
        background: linear-gradient(135deg, #1E222D 0%, #171A21 100%);
        border: 1px solid #2B313E;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #00D4FF;
        margin-top: 4px;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #A0AABF;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #1A1D24;
        border-radius: 8px;
        padding-left: 20px;
        padding-right: 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF9900 !important;
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialisation du moteur SQL (DuckDB / HiveQL) ---
@st.cache_resource
def init_hive_engine():
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "purchases.txt"),
        os.path.join(os.path.dirname(__file__), "..", "data", "purchases.txt"),
        "data/purchases.txt"
    ]
    
    data_file = next((p for p in possible_paths if os.path.exists(p)), None)
            
    if not data_file:
        st.error("❌ Fichier `purchases.txt` introuvable dans le dossier `data/`.")
        st.stop()

    con = duckdb.connect(database=':memory:', read_only=False)
    
    # Structure de la table externe Hive
    con.execute(f"""
        CREATE TABLE purchases_raw AS 
        SELECT 
            column0 AS sale_date,
            column1 AS sale_time,
            column2 AS store_name,
            column3 AS category,
            CAST(column4 AS DOUBLE) AS cost,
            column5 AS payment
        FROM read_csv('{data_file}', delim='\t', header=False)
        WHERE column4 IS NOT NULL AND column4 > 0;
    """)
    return con

con = init_hive_engine()

# --- En-tête ---
st.title("🐝 Apache HiveQL Data Warehouse & Business Intelligence")
st.caption("Plateforme décisionnelle & Studio de requêtage distribué basés sur la syntaxe HiveQL.")

# --- Navigation ---
tab_dash, tab_studio, tab_schema = st.tabs([
    "📊 Executive Dashboard", 
    "💻 Studio SQL & Console HiveQL", 
    "🗄️ Métadonnées Data Warehouse"
])

# =============================================================================
# TAB 1 : DASHBOARD EXECUTIVE & ANALYTICS
# =============================================================================
with tab_dash:
    st.sidebar.header("🎛️ Filtres Analytics")
    
    # Liste dynamique des magasins
    all_stores = [r[0] for r in con.execute("SELECT DISTINCT store_name FROM purchases_raw ORDER BY store_name").fetchall()]
    selected_stores = st.sidebar.multiselect("Magasins (Filtrage global) :", all_stores, default=all_stores[:10])
    
    top_stores_limit = st.sidebar.slider("Nombre de Magasins à comparer :", 5, 25, 10)
    top_categories_limit = st.sidebar.slider("Top N Catégories (Window Function) :", 1, 5, 3)

    # Clause WHERE dynamique
    store_filter = f"WHERE store_name IN ({','.join([f'\'{s}\'' for s in selected_stores])})" if selected_stores else "WHERE 1=1"

    # KPI Calculation
    kpi_df = con.execute(f"""
        SELECT 
            ROUND(SUM(cost), 2) AS total_revenue,
            COUNT(1) AS total_tx,
            ROUND(AVG(cost), 2) AS avg_basket,
            COUNT(DISTINCT store_name) AS active_stores
        FROM purchases_raw
        {store_filter}
    """).df()

    # Cartes KPI (4 Colonnes)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Chiffre d'Affaires</div>
                <div class="metric-value">{kpi_df['total_revenue'].iloc[0]:,.2f} €</div>
            </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Volume Transactions</div>
                <div class="metric-value">{kpi_df['total_tx'].iloc[0]:,}</div>
            </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Panier Moyen</div>
                <div class="metric-value">{kpi_df['avg_basket'].iloc[0]:,.2f} €</div>
            </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Magasins Sélectionnés</div>
                <div class="metric-value">{kpi_df['active_stores'].iloc[0]}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # RANGÉE 1 : ÉVOLUTION TEMPORELLE & MODES DE PAIEMENT
    # -------------------------------------------------------------------------
    row1_left, row1_right = st.columns([6, 4])

    with row1_left:
        st.subheader("📈 Évolution Chronologique des Ventes (HiveQL `GROUP BY sale_date`)")
        df_trend = con.execute(f"""
            SELECT 
                sale_date AS Date, 
                ROUND(SUM(cost), 2) AS Sales
            FROM purchases_raw
            {store_filter}
            GROUP BY sale_date
            ORDER BY sale_date ASC
        """).df()

        fig_trend = px.line(
            df_trend, x="Date", y="Sales", 
            markers=True, 
            title="Tendance Journalière du Chiffre d'Affaires",
            line_shape="linear"
        )
        fig_trend.update_traces(line_color="#00D4FF", line_width=3)
        st.plotly_chart(fig_trend, use_container_width=True)

    with row1_right:
        st.subheader("💳 Répartition des Modes de Paiement")
        df_payment = con.execute(f"""
            SELECT 
                payment AS Payment_Method, 
                ROUND(SUM(cost), 2) AS Sales
            FROM purchases_raw
            {store_filter}
            GROUP BY payment
            ORDER BY Sales DESC
        """).df()

        fig_payment = px.pie(
            df_payment, values="Sales", names="Payment_Method", 
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_payment.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_payment, use_container_width=True)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # RANGÉE 2 : TOP MAGASINS & WINDOW FUNCTIONS
    # -------------------------------------------------------------------------
    row2_left, row2_right = st.columns(2)

    with row2_left:
        st.subheader(f"📊 Top {top_stores_limit} Magasins par CA")
        df_store = con.execute(f"""
            SELECT store_name AS Magasin, ROUND(SUM(cost), 2) AS Ventes
            FROM purchases_raw
            {store_filter}
            GROUP BY store_name
            ORDER BY Ventes DESC
            LIMIT {top_stores_limit}
        """).df()
        
        fig_store = px.bar(
            df_store, x="Ventes", y="Magasin", orientation='h',
            color="Ventes", color_continuous_scale="Viridis",
            title=f"Classement des Magasins"
        )
        fig_store.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False)
        st.plotly_chart(fig_store, use_container_width=True)

    with row2_right:
        st.subheader(f"🏆 Top {top_categories_limit} Catégories par Magasin (`ROW_NUMBER`)")
        df_window = con.execute(f"""
            WITH ranked_categories AS (
                SELECT 
                    store_name,
                    category,
                    ROUND(SUM(cost), 2) AS category_sales,
                    ROW_NUMBER() OVER (PARTITION BY store_name ORDER BY SUM(cost) DESC) AS rank
                FROM purchases_raw
                {store_filter}
                GROUP BY store_name, category
            )
            SELECT store_name AS Magasin, category AS Categorie, category_sales AS Ventes
            FROM ranked_categories
            WHERE rank <= {top_categories_limit}
            ORDER BY store_name, rank
        """).df()

        fig_window = px.bar(
            df_window, x="Magasin", y="Ventes", color="Categorie",
            barmode="group", title="Partitionnement HiveQL par Magasin"
        )
        st.plotly_chart(fig_window, use_container_width=True)


# =============================================================================
# TAB 2 : STUDIO SQL INTERACTIF
# =============================================================================
with tab_studio:
    st.subheader("💻 Console HiveQL & SQL Query Runner")
    st.markdown("Exécutez, modifiez ou testez vos propres requêtes HiveQL complexes en temps réel.")

    # Catalogue complet de requêtes modèle
    PREDEFINED_QUERIES = {
        "1. Évolution Temporelle du CA par Date (Chrono-Analytics)": """-- Analyse de la tendance temporelle du CA
SELECT 
    sale_date,
    COUNT(1) AS total_transactions,
    ROUND(SUM(cost), 2) AS daily_revenue,
    ROUND(AVG(cost), 2) AS daily_avg_basket
FROM purchases_raw
GROUP BY sale_date
ORDER BY sale_date ASC;""",

        "2. Top 3 Catégories par Magasin (Hive Window Function ROW_NUMBER)": """-- Window Function : Classement des catégories par magasin
WITH ranked_sales AS (
    SELECT 
        store_name,
        category,
        ROUND(SUM(cost), 2) AS total_category_sales,
        ROW_NUMBER() OVER (PARTITION BY store_name ORDER BY SUM(cost) DESC) AS rank
    FROM purchases_raw
    GROUP BY store_name, category
)
SELECT store_name, category, total_category_sales, rank
FROM ranked_sales
WHERE rank <= 3
ORDER BY store_name ASC, rank ASC;""",

        "3. Performance par Mode de Paiement (GROUP BY & HAVING)": """-- Répartition et filtres sur les volumes de paiements élevés
SELECT 
    payment,
    category,
    COUNT(1) AS transaction_count,
    ROUND(SUM(cost), 2) AS total_amount
FROM purchases_raw
GROUP BY payment, category
HAVING SUM(cost) > 10000
ORDER BY total_amount DESC;""",

        "4. Top 10 Magasins Générant le Plus de Chiffre d'Affaires": """-- Top 10 Magasins
SELECT 
    store_name,
    COUNT(1) AS total_transactions,
    ROUND(SUM(cost), 2) AS total_sales
FROM purchases_raw
GROUP BY store_name
ORDER BY total_sales DESC
LIMIT 10;""",

        "✍️ Éditeur Libre (Saisir sa propre requête SQL)": """-- Écrivez votre requête HiveQL personnalisée
SELECT 
    category, 
    ROUND(SUM(cost), 2) AS total_sales,
    ROUND(AVG(cost), 2) AS avg_price
FROM purchases_raw
GROUP BY category
ORDER BY total_sales DESC;"""
    }

    selected_option = st.selectbox("📌 Choisir un modèle de requête HiveQL :", list(PREDEFINED_QUERIES.keys()))
    
    query_input = st.text_area(
        "Éditeur HiveQL :", 
        value=PREDEFINED_QUERIES[selected_option], 
        height=210
    )

    if st.button("▶️ Exécuter la requête HiveQL", type="primary"):
        start_time = time.time()
        try:
            res_df = con.execute(query_input).df()
            exec_time = time.time() - start_time
            
            st.success(f"✅ Requête exécutée en **{exec_time:.3f} secondes** ({len(res_df)} lignes retournées).")
            
            st.dataframe(res_df, use_container_width=True)

            csv = res_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger les résultats en CSV",
                data=csv,
                file_name="hiveql_results.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"❌ Erreur d'exécution HiveQL : {e}")


# =============================================================================
# TAB 3 : METADONNÉES DU DATA WAREHOUSE
# =============================================================================
with tab_schema:
    st.subheader("🗄️ Structure & Métadonnées de la table Hive (`purchases_raw`)")
    
    col_meta1, col_meta2 = st.columns(2)
    with col_meta1:
        st.markdown("**Schéma de la table Hive :**")
        schema_df = con.execute("DESCRIBE purchases_raw").df()
        st.table(schema_df)
    
    with col_meta2:
        st.markdown("**Aperçu des 10 premières lignes brutes :**")
        preview_df = con.execute("SELECT * FROM purchases_raw LIMIT 10").df()
        st.dataframe(preview_df, use_container_width=True)