import plotly.io as pio
import plotly.graph_objects as go
from .constants import CHART_THEME_COLORS

def apply_chart_theme():
    """Applies a consistent healthcare-themed visual style to all Plotly charts."""
    
    # Define custom template
    template = go.layout.Template()
    template.layout = go.Layout(
        # General visual style
        title_font=dict(size=20, family="Inter, sans-serif", color="#1F1F1F"),
        font=dict(family="Inter, sans-serif", color="#4A4A4A"),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        
        # Color sequence
        colorway=CHART_THEME_COLORS,
        
        # Axes styling
        xaxis=dict(
            showline=True,
            linecolor="#E0E0E0",
            gridcolor="#F5F5F5",
            zeroline=False
        ),
        yaxis=dict(
            showline=True,
            linecolor="#E0E0E0",
            gridcolor="#F5F5F5",
            zeroline=False
        ),
        
        # Legend styling
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        
        # Hover label styling
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_size=14,
            font_family="Inter, sans-serif"
        )
    )
    
    # Store template and set as default
    pio.templates["healthcare"] = template
    pio.templates.default = "healthcare"

# Initialize theme on import
apply_chart_theme()

def get_layout_config(title: str, height: int = 400) -> dict:
    """Returns standard layout dictionary for Plotly charts."""
    return {
        'title': title,
        'height': height,
        'template': 'healthcare',
        'margin': dict(l=50, r=50, t=100, b=50) # Increased top margin for legend
    }
