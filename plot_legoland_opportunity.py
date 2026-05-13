import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Load the dataset
csv_path = "msoa_attraction_opportunities.csv"
df = pd.read_csv(csv_path)

# Filter for LEGOLAND attractions
legoland_names = [
    "LEGOLAND® Windsor Resort",
    "LEGOLAND® Discovery Centre Birmingham",
    "LEGOLAND® Discovery Centre Manchester",
]

# Check which LEGOLAND attractions exist in the data
existing_legoland = [name for name in legoland_names if name in df['attraction_name'].unique()]
print("Found LEGOLAND attractions:", existing_legoland)

# For presentation, let's plot LEGOLAND Windsor Resort (the flagship)
target_attraction = "LEGOLAND® Windsor Resort"
lego_df = df[df['attraction_name'] == target_attraction].copy()

print(f"Rows for {target_attraction}: {len(lego_df)}")
print(f"Opportunity score range: {lego_df['opportunity_score_100'].min():.1f} - {lego_df['opportunity_score_100'].max():.1f}")

# Set up the plot
fig, ax = plt.subplots(figsize=(10, 14))

# Scatter plot: lat/lon colored by opportunity score
scatter = ax.scatter(
    lego_df['longitude_msoa'],
    lego_df['latitude_msoa'],
    c=lego_df['opportunity_score_100'],
    cmap='RdYlGn',  # Red (low) -> Yellow -> Green (high)
    s=15,
    alpha=0.8,
    edgecolors='none',
    vmin=0,
    vmax=100,
)

# Plot the attraction location
attraction_row = lego_df.iloc[0]
ax.scatter(
    attraction_row['longitude_attraction'],
    attraction_row['latitude_attraction'],
    c='blue',
    s=200,
    marker='*',
    edgecolors='white',
    linewidths=1.5,
    zorder=5,
    label='LEGOLAND Windsor',
)

# Colorbar
cbar = plt.colorbar(scatter, ax=ax, shrink=0.6, aspect=30, pad=0.02)
cbar.set_label('Opportunity Score (0-100)', fontsize=11)

# Map bounds (UK)
ax.set_xlim(-6.5, 2.0)
ax.set_ylim(49.5, 56.0)
ax.set_xlabel('Longitude', fontsize=11)
ax.set_ylabel('Latitude', fontsize=11)
ax.set_title(
    'LEGOLAND® Windsor Resort — Geographic Opportunity Heatmap\n'
    '(Opportunity Score by MSOA)',
    fontsize=13,
    pad=15,
)
ax.legend(loc='upper left', frameon=True)
ax.grid(True, alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('legoland_opportunity_map.png', dpi=300, bbox_inches='tight')
print("Saved: legoland_opportunity_map.png")
plt.show()
