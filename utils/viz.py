"""
Visualization utilities with consistent styling and beautiful charts.
Uses Plotly for interactive visualizations.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from utils.io import get_transport_mode_mapping


# Color palette
COLORS = {
    'primary': '#2c3e50',
    'secondary': '#34495e',
    'accent': '#e74c3c',
    'success': '#2ecc71',
    'warning': '#f39c12',
    'info': '#3498db',
    'light': '#ecf0f1',
    'dark': '#2c3e50',
    'background': '#ffffff'
}

TRANSPORT_COLORS = {
    'Voiture': '#e74c3c',
    'Transports en commun': '#3498db',
    'Vélo': '#2ecc71',
    'Marche': '#f39c12',
    'Deux-roues motorisé': '#9b59b6',
    'Pas de transport': '#95a5a6'
}


def get_plotly_template():
    """Return a custom Plotly template for consistent styling."""
    return {
        'layout': {
            'font': {'family': 'Inter, sans-serif', 'size': 12, 'color': COLORS['primary']},
            'paper_bgcolor': 'white',
            'plot_bgcolor': '#f8f9fa',
            'hovermode': 'closest',
            'hoverlabel': {
                'bgcolor': 'white',
                'font_size': 13,
                'font_family': 'Inter, sans-serif'
            },
            'margin': {'l': 60, 'r': 40, 't': 80, 'b': 60},
            'xaxis': {
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': '#e0e0e0',
                'zeroline': False
            },
            'yaxis': {
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': '#e0e0e0',
                'zeroline': False
            }
        }
    }


def create_sankey_diagram(df: pd.DataFrame, title: str = "Flux des modes de transport") -> go.Figure:
    """
    Create a Sankey diagram showing flow between regions and transport modes.
    
    Args:
        df: Aggregated data by region and transport mode
        title: Chart title
        
    Returns:
        Plotly Figure
    """
    # Prepare data for Sankey
    modes = df['mode_transport'].unique()
    regions = df['nom_region'].unique()
    
    # Create nodes
    all_nodes = list(regions) + list(modes)
    node_dict = {node: idx for idx, node in enumerate(all_nodes)}
    
    # Create links
    sources = []
    targets = []
    values = []
    colors = []
    
    for _, row in df.iterrows():
        sources.append(node_dict[row['nom_region']])
        targets.append(node_dict[row['mode_transport']])
        values.append(row['total_actifs'])
        colors.append(TRANSPORT_COLORS.get(row['mode_transport'], '#95a5a6'))
    
    # Create figure
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='white', width=2),
            label=all_nodes,
            color=['#95a5a6'] * len(regions) + [TRANSPORT_COLORS.get(m, '#95a5a6') for m in modes]
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=[c + '40' for c in colors]  # Add transparency
        )
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color=COLORS['primary'])),
        font=dict(size=12, family='Inter, sans-serif'),
        height=600,
        paper_bgcolor='white'
    )
    
    return fig


def create_sunburst_chart(df: pd.DataFrame, title: str = "Répartition des modes de transport") -> go.Figure:
    """
    Create a sunburst chart showing hierarchical breakdown of transport modes.
    
    Args:
        df: DataFrame with region, department, and mode data
        title: Chart title
        
    Returns:
        Plotly Figure
    """
    # Aggregate data
    agg_df = df.groupby(['mode_transport']).agg({
        'valeur': 'sum'
    }).reset_index()
    
    fig = go.Figure(go.Sunburst(
        labels=agg_df['mode_transport'],
        parents=[''] * len(agg_df),
        values=agg_df['valeur'],
        marker=dict(
            colors=[TRANSPORT_COLORS.get(m, '#95a5a6') for m in agg_df['mode_transport']],
            line=dict(color='white', width=2)
        ),
        hovertemplate='<b>%{label}</b><br>Actifs: %{value:,.0f}<br>Part: %{percentParent}<extra></extra>',
        textfont=dict(size=14, family='Inter, sans-serif', color='white')
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color=COLORS['primary'])),
        height=500,
        paper_bgcolor='white'
    )
    
    return fig


def create_choropleth_map(df: pd.DataFrame, metric_col: str = 'indice_dependance_voiture',
                          title: str = "Carte de la dépendance automobile") -> go.Figure:
    """
    Create an interactive choropleth map of France.
    
    Args:
        df: DataFrame with latitude, longitude, and metric
        metric_col: Column name for the metric to display
        title: Chart title
        
    Returns:
        Plotly Figure
    """
    fig = px.scatter_mapbox(
        df,
        lat='latitude',
        lon='longitude',
        color=metric_col,
        size=metric_col,
        hover_name='nom_commune',
        hover_data={
            'latitude': False,
            'longitude': False,
            metric_col: ':.1f',
            'nom_departement': True,
            'total_actifs': ':,.0f'
        },
        color_continuous_scale='RdYlGn_r',  # Red (high car) to Green (low car)
        size_max=15,
        zoom=5,
        center={'lat': 46.8, 'lon': 2.5},
        opacity=0.7,
        title=title
    )
    
    fig.update_layout(
        mapbox_style='carto-positron',
        height=700,
        title=dict(font=dict(size=20, color=COLORS['primary'])),
        coloraxis_colorbar=dict(
            title='% Voiture',
            ticksuffix='%'
        )
    )
    
    return fig


def create_horizontal_bar_chart(df: pd.DataFrame, x_col: str, y_col: str,
                                 color_col: str = None, title: str = "") -> go.Figure:
    """
    Create a horizontal bar chart for rankings.
    
    Args:
        df: DataFrame with data
        x_col: Column for x-axis (values)
        y_col: Column for y-axis (categories)
        color_col: Optional column for color coding
        title: Chart title
        
    Returns:
        Plotly Figure
    """
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        orientation='h',
        color=color_col if color_col else None,
        color_discrete_map=TRANSPORT_COLORS if color_col == 'mode_transport' else None,
        title=title,
        text=x_col
    )
    
    fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside',
        marker_line_width=0
    )
    
    fig.update_layout(
        **get_plotly_template()['layout'],
        title=dict(font=dict(size=18, color=COLORS['primary'])),
        xaxis_title='Pourcentage (%)',
        yaxis_title='',
        yaxis=dict(autorange='reversed'),
        height=max(400, len(df) * 25),
        showlegend=False
    )
    
    return fig


def create_scatter_plot(df: pd.DataFrame, x_col: str, y_col: str,
                       color_col: str = None, size_col: str = None,
                       title: str = "", x_label: str = "", y_label: str = "") -> go.Figure:
    """
    Create an interactive scatter plot.
    
    Args:
        df: DataFrame with data
        x_col: Column for x-axis
        y_col: Column for y-axis
        color_col: Optional column for color coding
        size_col: Optional column for bubble size
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        
    Returns:
        Plotly Figure
    """
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        size=size_col,
        hover_name='nom_commune' if 'nom_commune' in df.columns else None,
        hover_data={x_col: ':.1f', y_col: ':.1f'},
        title=title,
        trendline='ols' if len(df) > 10 else None,
        color_discrete_map=TRANSPORT_COLORS if color_col == 'mode_transport' else None
    )
    
    fig.update_layout(
        **get_plotly_template()['layout'],
        title=dict(font=dict(size=18, color=COLORS['primary'])),
        xaxis_title=x_label,
        yaxis_title=y_label,
        height=500
    )
    
    return fig


def create_stacked_bar_chart(df: pd.DataFrame, x_col: str, y_col: str,
                             color_col: str, title: str = "") -> go.Figure:
    """
    Create a stacked bar chart for mode comparison.
    
    Args:
        df: DataFrame with data
        x_col: Column for x-axis (categories)
        y_col: Column for y-axis (values)
        color_col: Column for stacking
        title: Chart title
        
    Returns:
        Plotly Figure
    """
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        color_discrete_map=TRANSPORT_COLORS,
        barmode='stack'
    )
    
    fig.update_layout(
        **get_plotly_template()['layout'],
        title=dict(font=dict(size=18, color=COLORS['primary'])),
        yaxis_title='Pourcentage (%)',
        xaxis_title='',
        height=500,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )
    
    return fig


def create_treemap(df: pd.DataFrame, path_cols: list, value_col: str,
                   title: str = "") -> go.Figure:
    """
    Create a treemap visualization.
    
    Args:
        df: DataFrame with hierarchical data
        path_cols: List of columns forming the hierarchy
        value_col: Column for the values
        title: Chart title
        
    Returns:
        Plotly Figure
    """
    fig = px.treemap(
        df,
        path=path_cols,
        values=value_col,
        color=value_col,
        color_continuous_scale='RdYlGn_r',
        title=title
    )
    
    fig.update_traces(
        textposition='middle center',
        textfont=dict(size=14, family='Inter, sans-serif')
    )
    
    fig.update_layout(
        title=dict(font=dict(size=20, color=COLORS['primary'])),
        height=600,
        paper_bgcolor='white'
    )
    
    return fig


def create_gauge_chart(value: float, title: str, max_value: float = 100,
                       threshold_colors: dict = None) -> go.Figure:
    """
    Create a gauge chart for a single metric.
    
    Args:
        value: The metric value
        title: Chart title
        max_value: Maximum value for the gauge
        threshold_colors: Dict with color thresholds
        
    Returns:
        Plotly Figure
    """
    if threshold_colors is None:
        threshold_colors = {
            0: COLORS['success'],
            50: COLORS['warning'],
            75: COLORS['accent']
        }
    
    fig = go.Figure(go.Indicator(
        mode='gauge+number+delta',
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 18}},
        number={'suffix': '%', 'font': {'size': 36}},
        gauge={
            'axis': {'range': [None, max_value], 'ticksuffix': '%'},
            'bar': {'color': COLORS['primary']},
            'steps': [
                {'range': [0, 50], 'color': '#d5f4e6'},
                {'range': [50, 75], 'color': '#fef5e7'},
                {'range': [75, 100], 'color': '#fadbd8'}
            ],
            'threshold': {
                'line': {'color': 'red', 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor='white',
        font={'family': 'Inter, sans-serif'}
    )
    
    return fig


def create_donut_chart(df: pd.DataFrame, labels_col: str, values_col: str,
                       title: str = "") -> go.Figure:
    """
    Create a donut chart for proportions.
    
    Args:
        df: DataFrame with data
        labels_col: Column for labels
        values_col: Column for values
        title: Chart title
        
    Returns:
        Plotly Figure
    """
    colors = [TRANSPORT_COLORS.get(label, '#95a5a6') for label in df[labels_col]]
    
    fig = go.Figure(data=[go.Pie(
        labels=df[labels_col],
        values=df[values_col],
        hole=0.5,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        textposition='outside',
        textinfo='label+percent',
        textfont=dict(size=13, family='Inter, sans-serif'),
        hovertemplate='<b>%{label}</b><br>Actifs: %{value:,.0f}<br>Part: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color=COLORS['primary'])),
        annotations=[dict(
            text='Total',
            x=0.5, y=0.5,
            font=dict(size=20, family='Inter, sans-serif'),
            showarrow=False
        )],
        height=500,
        paper_bgcolor='white',
        showlegend=True,
        legend=dict(
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=1.05
        )
    )
    
    return fig
