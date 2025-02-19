import plotly.graph_objects as go
import numpy as np

def create_frames(amplitude=1, frequency=4, duration_factor=100):
    """
    Generates animation frames for an oscillating point based on given amplitude and frequency.
    
    Parameters:
        amplitude (float): Amplitude of oscillation.
        frequency (float): Frequency of oscillation.
        duration_factor (int): Duration scaling factor for animation.

    Returns:
        list: List of Plotly frames for the animation.
    """
    t = np.linspace(0, duration_factor * (10 / frequency), duration_factor * 100)
    x = amplitude * np.sin(frequency * t)  

    frames = [go.Frame(
        data=[go.Scatter(x=[x[i]], y=[0], mode='markers', marker=dict(size=12, color='blue'))],
        name=f"freq_{frequency}_frame_{i}"
    ) for i in range(duration_factor * 100)]
    
    return frames

# Define frequency values for the slider
frequency_values = np.linspace(1, 10, 10)  # Frequency from 1 to 10

# Generate frames for each frequency
all_frames = []
frame_dict = {}

for freq in frequency_values:
    frames = create_frames(amplitude=1, frequency=freq, duration_factor=100)
    all_frames.extend(frames)
    frame_dict[freq] = [f.name for f in frames]

# Initialize figure
fig = go.Figure(
    data=[go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=12, color='blue'))],
    layout=go.Layout(
        title=dict(
            text="Vestibular Rehab: Oscillating Point",
            font=dict(size=20, family="Times New Roman", weight=5)
        ),
        xaxis=dict(range=[-2, 2], showticklabels=False),
        yaxis=dict(range=[-0.5, 0.5], showticklabels=False),
        showlegend=False,
        plot_bgcolor='white'
    ),
    frames=all_frames
)

# Create slider for frequency control
steps = []

for freq in frequency_values:
    step = dict(
        method="animate",
        args=[
            frame_dict[freq],  # Precomputed frames
            {"frame": {"duration": int(100/freq), "redraw": True}, "mode": "immediate"}
        ],
        label=str(freq)  
    )
    steps.append(step)

sliders = [dict(
    active=frequency_values.tolist().index(1),
    currentvalue={"prefix": "Frequency: "},
    pad={"t": 50},
    steps=steps
)]

# Add Play and Pause buttons
fig.update_layout(
    sliders=sliders,
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        buttons=[
            dict(
                label='Play',
                method='animate',
                args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True)]
            ),
            dict(
                label='Pause',
                method='animate',
                args=[[None], dict(frame=None, mode="immediate")]  
            )
        ]
    )]
)

# Save figure as an HTML file
fig.write_html("oscillating_point.html")

print("✅ Visualization saved as 'index.html'. Open this file in a web browser to view it.")
