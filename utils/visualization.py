"""
Visualization utilities for the Legal AI Platform
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from typing import Dict, List, Any

def create_risk_meter(risk_score: float, risk_level: str):
    """
    Create a risk meter visualization
    
    Args:
        risk_score: Risk score (0.0 to 1.0)
        risk_level: Risk level ('low', 'medium', or 'high')
        
    Returns:
        Plotly figure object
    """
    # Define colors
    colors = {
        "low": "#10B981",  # Green
        "medium": "#F59E0B",  # Yellow/Orange
        "high": "#DC2626"  # Red
    }
    
    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score * 100,
        title={"text": f"Risk Score: {risk_level.capitalize()}"},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": colors[risk_level]},
            "steps": [
                {"range": [0, 30], "color": "#DCFCE7"},  # Light green
                {"range": [30, 60], "color": "#FEF3C7"},  # Light yellow
                {"range": [60, 100], "color": "#FEE2E2"}  # Light red
            ],
            "threshold": {
                "line": {"color": "black", "width": 4},
                "thickness": 0.75,
                "value": risk_score * 100
            }
        }
    ))
    
    # Update layout
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    
    return fig

def create_risk_distribution(risky_clauses: List[Dict[str, Any]]):
    """
    Create a risk distribution visualization
    
    Args:
        risky_clauses: List of risky clause data
        
    Returns:
        Plotly figure object
    """
    if not risky_clauses:
        # Create empty chart with message
        fig = go.Figure()
        fig.add_annotation(
            text="No risk data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Count risk types
    risk_counts = {}
    for clause in risky_clauses:
        risk_type = clause.get("risk_type", "unknown")
        risk_counts[risk_type] = risk_counts.get(risk_type, 0) + 1
    
    # Create dataframe
    df = pd.DataFrame({
        "Risk Type": list(risk_counts.keys()),
        "Count": list(risk_counts.values())
    })
    
    # Sort by count descending
    df = df.sort_values("Count", ascending=False)
    
    # Create bar chart
    fig = px.bar(
        df,
        x="Risk Type",
        y="Count",
        title="Risk Distribution",
        color="Count",
        color_continuous_scale=["#10B981", "#F59E0B", "#DC2626"],
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Risk Type",
        yaxis_title="Number of Clauses",
        height=400,
        margin=dict(l=20, r=20, t=50, b=100),
        xaxis={'categoryorder':'total descending'}
    )
    
    return fig

def create_document_comparison_chart(docs_data: Dict[str, Dict[str, Any]]):
    """
    Create a radar chart comparing multiple documents
    
    Args:
        docs_data: Dictionary mapping document IDs to document data
        
    Returns:
        Plotly figure object
    """
    if len(docs_data) <= 1:
        # Create empty chart with message
        fig = go.Figure()
        fig.add_annotation(
            text="At least two documents are required for comparison",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Categories for radar chart
    categories = [
        "Risk Score", 
        "Length", 
        "Complexity", 
        "Clauses", 
        "Reading Time"
    ]
    
    fig = go.Figure()
    
    for doc_id, doc_data in docs_data.items():
        # Calculate metrics (scaled from 0 to 1)
        risk_score = doc_data.get("risk_score", 0)
        
        # Text length (normalize by longest document)
        max_length = max([d.get("metadata", {}).get("length", 1) for d in docs_data.values()])
        length_score = doc_data.get("metadata", {}).get("length", 0) / max_length
        
        # Complexity (based on sentence length)
        avg_sentence_length = doc_data.get("metadata", {}).get("length", 0) / max(1, doc_data.get("metadata", {}).get("num_sentences", 1))
        complexity_score = min(1.0, avg_sentence_length / 50)  # Cap at 50 words per sentence
        
        # Number of clauses (normalize by maximum)
        max_clauses = max([d.get("metadata", {}).get("num_clauses", 1) for d in docs_data.values()])
        clauses_score = doc_data.get("metadata", {}).get("num_clauses", 0) / max_clauses
        
        # Estimated reading time (normalize by maximum)
        reading_time = doc_data.get("metadata", {}).get("length", 0) / 250  # Words per minute
        max_reading_time = max([d.get("metadata", {}).get("length", 1) / 250 for d in docs_data.values()])
        reading_time_score = reading_time / max_reading_time
        
        # Create radar chart values
        values = [
            risk_score,
            length_score,
            complexity_score,
            clauses_score,
            reading_time_score
        ]
        
        # Add trace for this document
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=doc_data.get("filename", f"Document {doc_id}")
        ))
    
    # Update layout
    fig.update_layout(
        title="Document Comparison",
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=True,
        height=500
    )
    
    return fig

def create_risk_trend_chart(risk_history: List[Dict[str, Any]]):
    """
    Create a chart showing risk trends over time
    
    Args:
        risk_history: List of historical risk data
        
    Returns:
        Plotly figure object
    """
    if not risk_history:
        # Create empty chart with message
        fig = go.Figure()
        fig.add_annotation(
            text="No historical risk data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Create dataframe
    df = pd.DataFrame(risk_history)
    
    # Ensure date column is datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Sort by date
    df = df.sort_values('date')
    
    # Create line chart
    fig = px.line(
        df, 
        x='date', 
        y='risk_score',
        title='Risk Score Trend',
        color='document_type',
        markers=True,
        hover_data=['filename']
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Risk Score",
        height=400,
        yaxis=dict(range=[0, 1])
    )
    
    return fig

def highlight_risky_text(text: str, risky_clauses: List[Dict[str, Any]]) -> str:
    """
    Highlight risky clauses in the document text
    
    Args:
        text: Document text
        risky_clauses: List of risky clause data
        
    Returns:
        HTML with highlighted risky clauses
    """
    if not risky_clauses:
        return f"<div style='white-space: pre-wrap;'>{text}</div>"
    
    # Colors for different risk levels
    colors = {
        "high": "#FECACA",  # Light red
        "medium": "#FEF3C7",  # Light yellow
        "low": "#DCFCE7"  # Light green
    }
    
    # Sort clauses by start index to ensure proper highlighting
    sorted_clauses = sorted(risky_clauses, key=lambda x: x.get("start_index", 0))
    
    # Build HTML with highlights
    html = "<div style='white-space: pre-wrap;'>"
    last_end = 0
    
    for clause in sorted_clauses:
        start = clause.get("start_index", 0)
        end = clause.get("end_index", 0)
        risk_type = clause.get("risk_type", "unknown")
        confidence = clause.get("confidence", 1.0)
        
        # Determine risk level based on confidence and risk type
        if confidence > 0.7:
            risk_level = "high"
        elif confidence > 0.4:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # Add text before this clause
        html += text[last_end:start]
        
        # Add highlighted clause
        highlight_color = colors[risk_level]
        html += f"<span style='background-color: {highlight_color}; padding: 2px; border-radius: 3px;' title='{risk_type}'>{text[start:end]}</span>"
        
        last_end = end
    
    # Add remaining text
    html += text[last_end:]
    html += "</div>"
    
    return html

def create_side_by_side_comparison(original_text: str, simplified_text: str) -> str:
    """
    Create a side-by-side comparison of original and simplified text
    
    Args:
        original_text: Original legal text
        simplified_text: Simplified plain English text
        
    Returns:
        HTML for side-by-side comparison
    """
    html = """
    <div style="display: flex; width: 100%;">
        <div style="flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-right: 5px;">
            <h4 style="color: #1E3A8A;">Legal Text</h4>
            <div style="white-space: pre-wrap;">
    """
    
    html += original_text
    
    html += """
            </div>
        </div>
        <div style="flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-left: 5px;">
            <h4 style="color: #10B981;">Plain English</h4>
            <div style="white-space: pre-wrap;">
    """
    
    html += simplified_text
    
    html += """
            </div>
        </div>
    </div>
    """
    
    return html