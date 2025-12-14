"""
Insights dashboard page for the Legal AI Platform
"""
import streamlit as st
import pandas as pd
import numpy as np
import datetime
from typing import Dict, List, Any

from utils.visualization import (
    create_risk_trend_chart,
    create_document_comparison_chart,
    create_risk_distribution
)

def show_insights_page():
    """Display the insights dashboard page"""
    
    # Main heading
    st.markdown('<h1 class="main-header">Legal Insights Dashboard</h1>', unsafe_allow_html=True)
    
    # Check if any documents have been analyzed
    if not hasattr(st.session_state, 'analyzed_docs') or not st.session_state.analyzed_docs:
        st.info("No documents have been analyzed yet. Please upload and analyze documents first.")
        
        # Quick navigation to document analysis
        if st.button("Go to Document Analysis"):
            st.session_state.page = 'Document Analysis'
            st.rerun()
        
        return
    
    # Dashboard overview
    st.markdown("""
    This dashboard provides analytics and insights about your legal documents.
    Compare documents, track risk trends, and identify common patterns.
    """)
    
    # Create tabs for different insights
    tabs = st.tabs(["Overview", "Risk Analysis", "Document Comparison", "Trends"])
    
    # Overview tab
    with tabs[0]:
        show_overview_tab()
    
    # Risk Analysis tab
    with tabs[1]:
        show_risk_analysis_tab()
    
    # Document Comparison tab
    with tabs[2]:
        show_document_comparison_tab()
    
    # Trends tab
    with tabs[3]:
        show_trends_tab()

def show_overview_tab():
    """Display the overview tab"""
    
    # Dashboard statistics
    st.markdown("### Document Portfolio Overview")
    
    # Get document statistics
    num_docs = len(st.session_state.analyzed_docs)
    
    # Calculate average risk and other metrics
    avg_risk = np.mean([doc.get("risk_score", 0) for doc in st.session_state.analyzed_docs.values()])
    
    # Count risk levels
    risk_levels = {"low": 0, "medium": 0, "high": 0}
    for doc in st.session_state.analyzed_docs.values():
        risk_level = doc.get("risk_level", "low")
        risk_levels[risk_level] = risk_levels.get(risk_level, 0) + 1
    
    # Count document types
    doc_types = {}
    for doc in st.session_state.analyzed_docs.values():
        doc_type = doc.get("file_type", "").upper()[1:]  # Remove dot and capitalize
        doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
    
    # Display statistics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Documents", num_docs)
    
    with col2:
        st.metric("Average Risk Score", f"{avg_risk:.2f}")
    
    with col3:
        # Show risk distribution as text
        st.markdown("**Risk Distribution**")
        st.markdown(f"🟢 Low: {risk_levels.get('low', 0)}")
        st.markdown(f"🟠 Medium: {risk_levels.get('medium', 0)}")
        st.markdown(f"🔴 High: {risk_levels.get('high', 0)}")
    
    with col4:
        # Show document types
        st.markdown("**Document Types**")
        for doc_type, count in doc_types.items():
            st.markdown(f"{doc_type}: {count}")
    
    # Recent documents
    st.markdown("---")
    st.markdown("### Recent Documents")
    
    # Create a table of recent documents
    docs_data = []
    for doc_id, doc in st.session_state.analyzed_docs.items():
        # Create a simple timestamp from document ID (first 8 chars of UUID as hex timestamp)
        timestamp = int(doc_id.split("-")[0], 16) % (10**10)
        date = datetime.datetime.fromtimestamp(timestamp)
        
        docs_data.append({
            "Document ID": doc_id,
            "Filename": doc.get("filename", "Unknown"),
            "Date Added": date.strftime("%Y-%m-%d"),
            "Risk Score": f"{doc.get('risk_score', 0):.2f}",
            "Risk Level": doc.get("risk_level", "Unknown").capitalize()
        })
    
    # Sort by date (newest first)
    docs_data.sort(key=lambda x: x["Date Added"], reverse=True)
    
    # Display as dataframe
    df = pd.DataFrame(docs_data)
    st.dataframe(df, use_container_width=True)
    
    # Most common risk types across all documents
    st.markdown("---")
    st.markdown("### Common Risk Types")
    
    # Collect risk types from all documents
    risk_counts = {}
    for doc in st.session_state.analyzed_docs.values():
        risky_clauses = doc.get("risky_clauses", [])
        for clause in risky_clauses:
            risk_type = clause.get("risk_type", "unknown")
            risk_counts[risk_type] = risk_counts.get(risk_type, 0) + 1
    
    # Display risk types as a horizontal bar chart
    if risk_counts:
        # Convert to dataframe
        risk_df = pd.DataFrame({
            "Risk Type": list(risk_counts.keys()),
            "Count": list(risk_counts.values())
        })
        
        # Sort by count
        risk_df = risk_df.sort_values("Count", ascending=False)
        
        # Display as bar chart
        st.bar_chart(risk_df.set_index("Risk Type"))
    else:
        st.info("No risk data available yet.")

def show_risk_analysis_tab():
    """Display the risk analysis tab"""
    
    st.markdown("### Document Risk Analysis")
    
    # Get all risky clauses from all documents
    all_risky_clauses = []
    for doc_id, doc in st.session_state.analyzed_docs.items():
        risky_clauses = doc.get("risky_clauses", [])
        
        # Add document ID and filename to each clause
        for clause in risky_clauses:
            clause["doc_id"] = doc_id
            clause["filename"] = doc.get("filename", "Unknown")
        
        all_risky_clauses.extend(risky_clauses)
    
    # If no risky clauses found
    if not all_risky_clauses:
        st.info("No risky clauses found in any documents.")
        return
    
    # Display risk distribution
    risk_dist_fig = create_risk_distribution(all_risky_clauses)
    st.plotly_chart(risk_dist_fig, use_container_width=True)
    
    # Display most risky documents
    st.markdown("### Most Risky Documents")
    
    # Create a table of documents sorted by risk score
    docs_data = []
    for doc_id, doc in st.session_state.analyzed_docs.items():
        docs_data.append({
            "Document ID": doc_id,
            "Filename": doc.get("filename", "Unknown"),
            "Risk Score": doc.get("risk_score", 0),
            "Risk Level": doc.get("risk_level", "Unknown").capitalize(),
            "Risky Clauses": len(doc.get("risky_clauses", []))
        })
    
    # Sort by risk score (highest first)
    docs_data.sort(key=lambda x: x["Risk Score"], reverse=True)
    
    # Display as dataframe
    df = pd.DataFrame(docs_data)
    st.dataframe(df, use_container_width=True)
    
    # Display most common risky clauses
    st.markdown("### Common Risky Clauses")
    
    # Group clauses by text
    clause_texts = {}
    for clause in all_risky_clauses:
        text = clause.get("text", "")
        if text:
            # Use only first 100 chars as key to group similar clauses
            text_key = text[:100]
            if text_key in clause_texts:
                clause_texts[text_key]["count"] += 1
                clause_texts[text_key]["docs"].add(clause.get("filename", "Unknown"))
            else:
                clause_texts[text_key] = {
                    "text": text,
                    "count": 1,
                    "risk_type": clause.get("risk_type", "unknown"),
                    "docs": {clause.get("filename", "Unknown")}
                }
    
    # Convert to list and sort by count
    clause_list = [
        {
            "text": info["text"],
            "count": info["count"],
            "risk_type": info["risk_type"],
            "docs": ", ".join(list(info["docs"])[:3]) + (f" and {len(info['docs']) - 3} more" if len(info["docs"]) > 3 else "")
        }
        for text_key, info in clause_texts.items()
    ]
    clause_list.sort(key=lambda x: x["count"], reverse=True)
    
    # Display top risky clauses
    for i, clause in enumerate(clause_list[:10]):  # Show top 10
        with st.expander(f"{clause['risk_type'].replace('_', ' ').title()} (Found in {clause['count']} documents)"):
            st.markdown(f"**Documents:** {clause['docs']}")
            st.markdown(f"**Text:** {clause['text']}")

def show_document_comparison_tab():
    """Display the document comparison tab"""
    
    st.markdown("### Document Comparison")
    st.markdown("Compare multiple documents to identify similarities and differences.")
    
    # Document selection
    st.markdown("#### Select Documents to Compare")
    
    # Get document options
    doc_options = {doc.get("filename", f"Document {doc_id}"): doc_id 
                  for doc_id, doc in st.session_state.analyzed_docs.items()}
    
    # Multi-select for documents
    selected_doc_names = st.multiselect(
        "Select documents",
        options=list(doc_options.keys()),
        default=list(doc_options.keys())[:min(2, len(doc_options))]
    )
    
    # Get selected document IDs
    selected_doc_ids = [doc_options[name] for name in selected_doc_names]
    
    # Show comparison if at least two documents selected
    if len(selected_doc_ids) >= 2:
        # Get selected documents data
        selected_docs = {doc_id: st.session_state.analyzed_docs[doc_id] 
                        for doc_id in selected_doc_ids}
        
        # Create radar chart comparison
        st.markdown("#### Document Comparison Chart")
        comparison_fig = create_document_comparison_chart(selected_docs)
        st.plotly_chart(comparison_fig, use_container_width=True)
        
        # Create table comparison
        st.markdown("#### Document Metrics Comparison")
        
        # Create comparison dataframe
        comparison_data = []
        for doc_id, doc in selected_docs.items():
            comparison_data.append({
                "Document": doc.get("filename", f"Document {doc_id}"),
                "Risk Score": f"{doc.get('risk_score', 0):.2f}",
                "Risk Level": doc.get("risk_level", "low").capitalize(),
                "Length (chars)": doc.get("metadata", {}).get("length", 0),
                "Sentences": doc.get("metadata", {}).get("num_sentences", 0),
                "Clauses": doc.get("metadata", {}).get("num_clauses", 0),
                "Risky Clauses": len(doc.get("risky_clauses", []))
            })
        
        # Display as dataframe
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
        
        # Common risky clauses
        st.markdown("#### Common Risk Types")
        
        # Count risk types in each document
        doc_risk_counts = {}
        for doc_id, doc in selected_docs.items():
            doc_name = doc.get("filename", f"Document {doc_id}")
            doc_risk_counts[doc_name] = {}
            
            for clause in doc.get("risky_clauses", []):
                risk_type = clause.get("risk_type", "unknown")
                doc_risk_counts[doc_name][risk_type] = doc_risk_counts[doc_name].get(risk_type, 0) + 1
        
        # Get all risk types
        all_risk_types = set()
        for doc_name, risk_counts in doc_risk_counts.items():
            all_risk_types.update(risk_counts.keys())
        
        # Create comparison dataframe
        risk_comparison_data = []
        for risk_type in sorted(all_risk_types):
            row_data = {"Risk Type": risk_type.replace("_", " ").title()}
            
            for doc_name in doc_risk_counts.keys():
                row_data[doc_name] = doc_risk_counts[doc_name].get(risk_type, 0)
            
            risk_comparison_data.append(row_data)
        
        # Display as dataframe
        if risk_comparison_data:
            risk_comparison_df = pd.DataFrame(risk_comparison_data)
            st.dataframe(risk_comparison_df, use_container_width=True)
        else:
            st.info("No risk data available for comparison.")
    
    else:
        st.info("Please select at least two documents to compare.")

def show_trends_tab():
    """Display the trends tab"""
    
    st.markdown("### Document Trends Over Time")
    st.markdown("Track how document risks and metrics change over time.")
    
    # Create mock historical data for demonstration
    # In a real implementation, this would come from a database
    
    # Create a simple timestamp from document ID (first 8 chars of UUID as hex timestamp)
    risk_history = []
    for doc_id, doc in st.session_state.analyzed_docs.items():
        # Create a date from document ID
        timestamp = int(doc_id.split("-")[0], 16) % (10**10)
        date = datetime.datetime.fromtimestamp(timestamp)
        
        risk_history.append({
            "document_id": doc_id,
            "filename": doc.get("filename", "Unknown"),
            "date": date,
            "risk_score": doc.get("risk_score", 0),
            "document_type": doc.get("file_type", "").upper()[1:]
        })
    
    # Create risk trend chart
    risk_trend_fig = create_risk_trend_chart(risk_history)
    st.plotly_chart(risk_trend_fig, use_container_width=True)
    
    # Document metrics over time
    st.markdown("### Document Metrics Over Time")
    
    # Create metrics history
    metrics_history = []
    for doc_id, doc in st.session_state.analyzed_docs.items():
        # Create a date from document ID
        timestamp = int(doc_id.split("-")[0], 16) % (10**10)
        date = datetime.datetime.fromtimestamp(timestamp)
        
        # Get document metrics
        metadata = doc.get("metadata", {})
        
        metrics_history.append({
            "document_id": doc_id,
            "filename": doc.get("filename", "Unknown"),
            "date": date,
            "length": metadata.get("length", 0),
            "sentences": metadata.get("num_sentences", 0),
            "clauses": metadata.get("num_clauses", 0),
            "risky_clauses": len(doc.get("risky_clauses", []))
        })
    
    # Convert to dataframe
    metrics_df = pd.DataFrame(metrics_history)
    
    # Sort by date
    metrics_df["date"] = pd.to_datetime(metrics_df["date"])
    metrics_df = metrics_df.sort_values("date")
    
    # Display line charts for different metrics
    metric_options = ["length", "sentences", "clauses", "risky_clauses"]
    selected_metric = st.selectbox(
        "Select metric to visualize",
        options=metric_options,
        format_func=lambda x: {
            "length": "Document Length",
            "sentences": "Number of Sentences",
            "clauses": "Number of Clauses",
            "risky_clauses": "Number of Risky Clauses"
        }.get(x, x.replace("_", " ").title())
    )
    
    # Plot selected metric
    if not metrics_df.empty:
        chart_data = metrics_df[["date", selected_metric, "filename"]]
        chart_data = chart_data.rename(columns={selected_metric: "value"})
        
        # Create a Streamlit line chart
        st.line_chart(
            chart_data.set_index("date")["value"], 
            use_container_width=True
        )
        
        # Display data table
        st.dataframe(
            metrics_df[["filename", "date", selected_metric]].sort_values("date", ascending=False),
            use_container_width=True
        )
    else:
        st.info("No trend data available yet.")