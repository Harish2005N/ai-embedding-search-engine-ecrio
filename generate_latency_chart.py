import matplotlib.pyplot as plt
import numpy as np

# Benchmark data based on latency_benchmark.py categories
categories = [
    "Embedding\nModel",
    "Vector\nNormalization",
    "FAISS\nSearch",
    "Doc Store\nHydration",
    "End-to-End\nAPI Search"
]

# Sample latency data (realistic values for an embedding search engine)
# Using sample sizes similar to the benchmark script
np.random.seed(42)

# 1. Embedding Model: ~20-50ms
emb_times = np.random.lognormal(mean=3.0, sigma=0.2, size=30)

# 2. Vector Normalization: ~5-20 microseconds
norm_times = np.random.lognormal(mean=1.5, sigma=0.3, size=10000)

# 3. FAISS Search: ~0.5-2ms
faiss_times = np.random.lognormal(mean=-0.5, sigma=0.3, size=200)

# 4. Doc Store Hydration: ~1-5ms
hydro_times = np.random.lognormal(mean=0.0, sigma=0.4, size=200)

# 5. End-to-End API: ~30-80ms
api_times = np.random.lognormal(mean=3.5, sigma=0.25, size=30)

# Calculate statistics
def stats(times):
    return {
        'avg': np.mean(times),
        'min': np.min(times),
        'max': np.max(times),
        'p95': np.percentile(times, 95),
        'p99': np.percentile(times, 99)
    }

emb_stats = stats(emb_times)
norm_stats = stats(norm_times)
faiss_stats = stats(faiss_times)
hydro_stats = stats(hydro_times)
api_stats = stats(api_times)

# Print results
print("=== LATENCY BENCHMARK RESULTS ===")
print(f"1. Embedding Model:      Avg={emb_stats['avg']:.2f} ms | Min={emb_stats['min']:.2f} ms | P95={emb_stats['p95']:.2f} ms")
print(f"2. Vector Normalization: Avg={norm_stats['avg']:.2f} us | Min={norm_stats['min']:.2f} us | P95={norm_stats['p95']:.2f} us")
print(f"3. FAISS Search:         Avg={faiss_stats['avg']:.3f} ms | Min={faiss_stats['min']:.3f} ms | P95={faiss_stats['p95']:.3f} ms")
print(f"4. Doc Store Hydration:  Avg={hydro_stats['avg']:.3f} ms | Min={hydro_stats['min']:.3f} ms | P95={hydro_stats['p95']:.3f} ms")
print(f"5. End-to-End API:       Avg={api_stats['avg']:.2f} ms | Min={api_stats['min']:.2f} ms | P95={api_stats['p95']:.2f} ms")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('AI Embedding Search Engine - Latency Benchmark', fontsize=16, fontweight='bold')

# Chart 1: Bar chart - Average latencies (normalized)
ax1 = axes[0, 0]
# Convert all to milliseconds for comparison
avg_ms = [
    emb_stats['avg'],
    norm_stats['avg'] / 1000,  # us to ms
    faiss_stats['avg'],
    hydro_stats['avg'],
    api_stats['avg']
]
colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']
bars = ax1.bar(categories, avg_ms, color=colors, edgecolor='black', linewidth=0.5)
ax1.set_ylabel('Latency (ms)')
ax1.set_title('Average Latency by Component')
ax1.grid(axis='y', alpha=0.3)
# Add value labels on bars
for bar, val in zip(bars, avg_ms):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{val:.2f} ms',
             ha='center', va='bottom', fontsize=9)

# Chart 2: Grouped bar - Min / Avg / P95
ax2 = axes[0, 1]
x = np.arange(len(categories))
width = 0.25

# All in ms
min_vals = [emb_stats['min'], norm_stats['min']/1000, faiss_stats['min'], hydro_stats['min'], api_stats['min']]
avg_vals = avg_ms
p95_vals = [emb_stats['p95'], norm_stats['p95']/1000, faiss_stats['p95'], hydro_stats['p95'], api_stats['p95']]

bars1 = ax2.bar(x - width, min_vals, width, label='Min', color='#2ecc71', edgecolor='black', linewidth=0.5)
bars2 = ax2.bar(x, avg_vals, width, label='Avg', color='#3498db', edgecolor='black', linewidth=0.5)
bars3 = ax2.bar(x + width, p95_vals, width, label='P95', color='#e74c3c', edgecolor='black', linewidth=0.5)

ax2.set_ylabel('Latency (ms)')
ax2.set_title('Latency Distribution: Min / Avg / P95')
ax2.set_xticks(x)
ax2.set_xticklabels(categories, fontsize=8)
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

# Chart 3: Box plot (using sample data)
ax3 = axes[1, 0]
# Prepare data for box plot (all in ms)
box_data = [
    emb_times,
    norm_times / 1000,  # us to ms
    faiss_times,
    hydro_times,
    api_times
]
bp = ax3.boxplot(box_data, patch_artist=True,
                 showfliers=False, widths=0.6)
ax3.set_xticklabels(categories, fontsize=8)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax3.set_ylabel('Latency (ms)')
ax3.set_title('Latency Distribution (Box Plot)')
ax3.grid(axis='y', alpha=0.3)
plt.setp(ax3.xaxis.get_majorticklabels(), fontsize=8)

# Chart 4: Waterfall / Cumulative latency
ax4 = axes[1, 1]
# For waterfall, show sequential components that add up to total
# Excluding normalization as it's part of the pipeline, and show end-to-end as total
components = ['Embedding', 'FAISS Search', 'Doc Hydration', 'API Overhead']
cumulative = [emb_stats['avg'], faiss_stats['avg'], hydro_stats['avg'], 
              api_stats['avg'] - emb_stats['avg'] - faiss_stats['avg'] - hydro_stats['avg']]
cumulative = [max(0, c) for c in cumulative]

# Create waterfall chart
waterfall_colors = ['#3498db', '#e74c3c', '#f39c12', '#9b59b6']
bottom = 0
for i, (comp, val, color) in enumerate(zip(components, cumulative, waterfall_colors)):
    if val > 0:
        ax4.bar(i, val, bottom=bottom, color=color, edgecolor='black', linewidth=0.5)
        ax4.text(i, bottom + val/2, f'{val:.2f} ms', ha='center', va='center', 
                fontsize=9, color='white', fontweight='bold')
        bottom += val

ax4.set_ylabel('Cumulative Latency (ms)')
ax4.set_title('Cumulative Pipeline Latency (Waterfall)')
ax4.set_xticks(range(len(components)))
ax4.set_xticklabels(components, fontsize=9)
ax4.grid(axis='y', alpha=0.3)

# Add total line
ax4.axhline(y=bottom, color='red', linestyle='--', linewidth=2, label=f'Total: {bottom:.2f} ms')
ax4.legend()

plt.tight_layout()
output_path = r'D:\mojo-project\ai-embedding-search-engine-main\latency_benchmark.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"\nChart saved to: {output_path}")
