import os
import pandas as pd
import happybase
from typing import TypedDict, List, Annotated

from langchain_core.tools import tool
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION HBASE ET RAG ---
HBASE_HOST = "localhost"
HBASE_PORT = 9090
TABLE_NAME = "retail_feature_store"
DATA_PATH = "Projet04_HBase_LangGraph_Agentic_AI/data/purchases.txt"

# --- HELPER D'ACCÈS AUX DONNÉES HBASE / FALLBACK ---
def _fetch_hbase_dataframe() -> pd.DataFrame:
    """Interroge la table HBase ou lit le jeu de données local si HBase est indisponible."""
    try:
        connection = happybase.Connection(host=HBASE_HOST, port=HBASE_PORT, timeout=2000)
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
        for c in ["sales:total_revenue", "sales:avg_transaction", "sales:transaction_count"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        return df

    except Exception:
        if os.path.exists(DATA_PATH):
            cols = ["date", "time", "city", "category", "amount", "payment"]
            raw_df = pd.read_csv(DATA_PATH, sep="\t", names=cols, header=None)
            raw_df["amount"] = pd.to_numeric(raw_df["amount"], errors="coerce").fillna(0.0)
            
            records = []
            for city, group in raw_df.groupby("city"):
                cat_sum = group.groupby("category")["amount"].sum()
                records.append({
                    "city": city,
                    "sales:total_revenue": group["amount"].sum(),
                    "sales:avg_transaction": group["amount"].mean(),
                    "sales:transaction_count": len(group),
                    "categories:top_category": cat_sum.idxmax() if not cat_sum.empty else "N/A"
                })
            return pd.DataFrame(records)
        return pd.DataFrame()

# ==========================================
# 1. DÉFINITION DES OUTILS DE REQUÊTE HBASE (TOOLS)
# ==========================================
@tool
def query_top_performing_cities(top_n: int = 5) -> str:
    """À utiliser lorsque l'utilisateur demande quelles villes ou quels magasins ont effectué le plus de ventes, de chiffre d'affaires (CA) ou de transactions.

    Args:
        top_n: Le nombre de villes du classement à retourner (par défaut 5).
    """
    df = _fetch_hbase_dataframe()
    if df.empty:
        return "Aucune donnée n'a pu être récupérée depuis HBase ou le dataset local."
    
    top_df = df.nlargest(top_n, "sales:total_revenue")
    results = []
    for rank, (_, row) in enumerate(top_df.iterrows(), 1):
        results.append(
            f"{rank}. Ville (RowKey): {row['city']} | CA Total: {row['sales:total_revenue']:,.2f} € | "
            f"Panier Moyen: {row['sales:avg_transaction']:,.2f} € | Transactions: {row['sales:transaction_count']}"
        )
    return "\n".join(results)

@tool
def query_city_specific_metrics(city_name: str) -> str:
    """À utiliser pour obtenir les statistiques NoSQL détaillées (CA, panier moyen, catégorie phare) d'une ville spécifique.

    Args:
        city_name: Le nom de la ville en anglais (ex: 'Baltimore', 'Miami', 'Chicago', 'Houston').
    """
    df = _fetch_hbase_dataframe()
    if df.empty:
        return "Aucune donnée n'a pu être récupérée depuis HBase."
    
    match = df[df["city"].str.lower() == city_name.strip().lower()]
    if match.empty:
        return f"La ville '{city_name}' n'existe pas dans le Feature Store HBase."
    
    row = match.iloc[0]
    return (
        f"--- MÉTRIQUES HBASE POUR LA VILLE : {row['city']} ---\n"
        f"- Chiffre d'Affaires Total (sales:total_revenue) : {float(row.get('sales:total_revenue', 0)):,.2f} €\n"
        f"- Panier Moyen (sales:avg_transaction) : {float(row.get('sales:avg_transaction', 0)):,.2f} €\n"
        f"- Volume de Transactions (sales:transaction_count) : {row.get('sales:transaction_count')} ventes\n"
        f"- Catégorie Dominante (categories:top_category) : {row.get('categories:top_category')}"
    )

@tool
def query_rag_knowledge_base(query: str) -> str:
    """À utiliser pour répondre aux questions générales sur l'architecture, le fonctionnement du Feature Store ou les concepts du projet."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    persist_dir = "./chroma_db"
    
    if os.path.exists(persist_dir) and os.listdir(persist_dir):
        vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
        docs = vectorstore.as_retriever(search_kwargs={"k": 2}).invoke(query)
        if docs:
            return "\n\n".join([d.page_content for d in docs])
    return "Aucune documentation RAG pertinente n'a été trouvée dans la base vectorielle."

tools = [query_top_performing_cities, query_city_specific_metrics, query_rag_knowledge_base]

# ==========================================
# 2. DÉFINITION DE L'ÉTAT ET DU LLM
# ==========================================
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    generation: str
    documents: List[str]

llm = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0.1,
    api_key=os.getenv("MISTRAL_API_KEY")
).bind_tools(tools)

# ==========================================
# 3. NŒUDS DE L'AGENT LANGGRAPH
# ==========================================
def agent_node(state: AgentState) -> dict:
    messages = state["messages"]
    system_instruction = SystemMessage(content=(
        "Tu es l'Agent IA officiel du Feature Store Retail HBase.\n"
        "Pour répondre aux questions métiers sur les chiffres, classements et ventes par ville, "
        "tu DOIS impérativement appeler les outils dédiés (query_top_performing_cities ou query_city_specific_metrics).\n"
        "Ne réponds jamais 'Je ne sais pas' sans avoir exécuté une requête NoSQL via tes outils."
    ))
    
    full_messages = [system_instruction] + messages
    response = llm.invoke(full_messages)
    return {"messages": [response]}

# ==========================================
# 4. CONSTRUCTION DU GRAPHE D'AGENT
# ==========================================
def build_rag_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(tools))

    workflow.set_entry_point("agent")
    
    workflow.add_conditional_edges("agent", tools_condition)
    workflow.add_edge("tools", "agent")

    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)