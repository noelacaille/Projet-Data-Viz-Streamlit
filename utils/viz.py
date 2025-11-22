import plotly.express as px
import plotly.graph_objects as go

# Define consistent color palette
COLOR_MAP = {
    "Voiture": "#d62728",  # Red
    "Transports en commun": "#1f77b4",  # Blue
    "Pas de transport": "#2ca02c",  # Green
    "Deux-roues motorisé": "#ff7f0e",  # Orange
    "Autre": "#7f7f7f" # Gray
}

def get_color_map():
    return COLOR_MAP

def plot_mode_distribution(df_filtered):
    """
    Pie chart of global mode distribution in the filtered area.
    """
    # Sum up all values for each mode
    mode_cols = [c for c in df_filtered.columns if c in COLOR_MAP.keys()]
    
    # If columns are not exactly matching keys, we might need to adjust prep.py or here.
    # Let's assume prep.py pivot columns match the CSV values: 
    # "Voiture", "Transports en commun", "Pas de transport", "Deux-roues motorisé"
    
    # Check which columns exist
    existing_cols = [c for c in mode_cols if c in df_filtered.columns]
    
    total_values = df_filtered[existing_cols].sum().reset_index()
    total_values.columns = ['Mode', 'Total']
    
    fig = px.pie(
        total_values, 
        values='Total', 
        names='Mode', 
        color='Mode',
        color_discrete_map=COLOR_MAP,
        title="Répartition globale des modes de transport"
    )
    return fig

def plot_top_flop_communes(df_filtered, mode="Voiture", top_n=10):
    """
    Bar chart of top and bottom communes for a specific mode percentage.
    """
    col_name = f'pct_{mode}'
    if col_name not in df_filtered.columns:
        return None
        
    # Sort by percentage
    df_sorted = df_filtered.sort_values(col_name, ascending=False)
    
    # Take top N and bottom N
    top = df_sorted.head(top_n)
    bottom = df_sorted.tail(top_n)
    
    # Combine for display
    # We might want to display them separately or together. 
    # Let's do Top N dependent on the mode.
    
    fig = px.bar(
        top,
        x=col_name,
        y='libelle_commune',
        orientation='h',
        title=f"Top {top_n} communes : {mode} (%)",
        color=col_name,
        color_continuous_scale='Reds' if mode == 'Voiture' else 'Blues',
        labels={col_name: f'% {mode}', 'libelle_commune': 'Commune'}
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

def plot_scatter_size_vs_mode(df_filtered, mode="Voiture"):
    """
    Scatter plot: Total Actifs vs % Mode.
    """
    col_name = f'pct_{mode}'
    if col_name not in df_filtered.columns:
        return None
        
    fig = px.scatter(
        df_filtered,
        x='Total_Actifs',
        y=col_name,
        hover_name='libelle_commune',
        title=f"Taille de la commune vs Usage {mode}",
        log_x=True, # Log scale often better for city sizes
        labels={'Total_Actifs': 'Nombre d\'actifs (Log)', col_name: f'% {mode}'},
        opacity=0.6
    )
    return fig

def plot_boxplot_distribution(df_filtered, mode="Voiture"):
    """
    Boxplot of mode percentage distribution by department.
    """
    col_name = f'pct_{mode}'
    if col_name not in df_filtered.columns:
        return None
        
    fig = px.box(
        df_filtered,
        x='dept',
        y=col_name,
        title=f"Distribution de l'usage {mode} par département",
        labels={'dept': 'Département', col_name: f'% {mode}'},
        color='dept'
    )
    return fig
