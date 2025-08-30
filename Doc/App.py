from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import pandas as pd

# Re-parse and fix missing decision/campus dates handling
def safe_parse_date(x):
    try:
        return pd.to_datetime(x)
    except:
        return pd.NaT

# Full corrected dataset with clarified decision and visit dates
data = [
    ("Brown University", "2024-12-01", [], None, "2025-03-26", "SPH | Rej", "SPH", "Midwest"),
    ("Duke University", "2024-12-02", ["2025-01-09", "2025-02-06"], None, "2025-02-12", "SoP | Offer", "SoP", "South"),
    ("Emory University", "2024-12-01", ["2025-01-02"], None, "2025-02-22", "SPH | Rej", "SPH", "Southeast"),
    ("Ohio State University", "2024-12-01", [], None, "2025-03-04", "SoP | Rej", "SoP", "Midwest"),
    ("Rutgers University", "2024-12-01", ["2025-01-07"], None, "2025-02-13", "SPH | Offer", "SPH", "Northeast"),
    ("UCSD/SDSU", "2024-12-01", [], None, "2025-03-14", "SPH | Rej", "SPH", "West Coast"),
    ("University of California Irvine", "2024-12-01", ["2025-01-27"], None, "2025-04-21", "SPH | Rej", "SPH", "West Coast"),
    ("University of California San Diego", "2025-01-08", ["2025-02-28"], None, "2025-03-24", "SPH | Offer", "SPH", "West Coast"),
    ("University of Florida", "2024-12-01", ["2025-01-03"], "2025-02-23", "2025-03-13", "SoP | Offer", "SoP", "South"),
    ("University of Illinois Chicago", "2025-02-15", ["2025-02-28"], None, "2025-03-07", "SoP | Offer", "SoP", "Midwest"),
    ("University of Maryland", "2024-12-02", ["2025-01-13", "2025-02-03"], "2025-03-03", None, "SoP", "SoP", "Northeast"),
    ("University of Michigan Ann Anbor", "2024-12-01", ["2025-02-03"], "2025-03-24", "2025-02-19", "SoP | Offer", "SoP", "Midwest"),
    ("University of Minnesota", "2024-11-30", ["2025-01-13"], "2025-02-11", "2025-03-31", "SoP | Rej", "SoP", "Midwest"),
    ("University of North Carolina", "2024-12-10", [], None, "2025-03-17", "SPH | Rej", "SPH", "Southeast"),
    ("University of North Carolina", "2024-12-03", ["2025-01-07"], None, "2025-01-21", "SoP | Rej", "SoP", "Southeast"),
    ("University of Pennsylvania", "2024-12-01", [], None, "2025-01-16", "SoM | Rej", "SoM", "Northeast"),
    ("University of Pittsburgh", "2025-01-08", ["2025-01-02"], None, "2025-03-12", "SoP | Rej", "SoP", "Northeast"),
    ("University of South California", "2024-12-01", ["2025-01-09", "2025-02-06"], None, "2025-02-14", "SoP | Offer", "SoP", "West Coast"),
    ("University of Texas Austin", "2024-12-01", ["2025-01-15"], None, "2025-02-12", "SoP | Offer", "SoP", "South"),
]

df = pd.DataFrame(data, columns=["University", "App_Date", "Interview_Dates", "Campus_Visit", "Decision_Date", "Decision_Label", "Type", "Region"])
df["App_Date"] = pd.to_datetime(df["App_Date"])
df["Decision_Date"] = df["Decision_Date"].apply(safe_parse_date)
df["Campus_Visit"] = df["Campus_Visit"].apply(safe_parse_date)
df["Interview_Dates"] = df["Interview_Dates"].apply(lambda x: [pd.to_datetime(d) for d in x])

# Colors
type_colors = {"SPH": "#3c78d8", "SoP": "#f6b26b", "SoM": "#93c47d"}
region_colors = {"West Coast": "#c9daf8", "Northeast": "#ead1dc", "Midwest": "#fce5cd", "Southeast": "#fff2cc", "South": "#d9ead3"}

# Plot
fig, ax = plt.subplots(figsize=(14, 10))
date_min = datetime(2024, 11, 20)
date_max = datetime(2025, 5, 1)
df = df.sort_values("University", ascending=True)
for i, row in df.iterrows():
    y_pos = df.index.get_loc(i)
    app_date = row["App_Date"]
    end_date = row["Decision_Date"]
    if pd.isna(end_date):
        if pd.notna(row["Campus_Visit"]):
            end_date = row["Campus_Visit"]
        elif row["Interview_Dates"]:
            end_date = max(row["Interview_Dates"])
        else:
            end_date = date_max
    ax.plot([app_date, end_date], [y_pos, y_pos], color=type_colors[row["Type"]], linewidth=2, marker=">", markersize=6)
    for interview_date in row["Interview_Dates"]:
        ax.plot(interview_date, y_pos, marker="*", color="black", markersize=10)
    if pd.notna(row["Campus_Visit"]):
        ax.plot(row["Campus_Visit"], y_pos, marker="^", color="black", markersize=6)
    if row["Decision_Label"]:
        ax.text(end_date, y_pos + 0.2, f"{row['Decision_Label']} ({end_date.date()})", fontsize=8)
    ax.axhspan(ymin=y_pos - 0.5, ymax=y_pos + 0.5, color=region_colors[row["Region"]], alpha=0.2)

# Labels and legend
ax.set_yticks(range(len(df)))
ax.set_yticklabels(df["University"])
ax.set_xlim(date_min, date_max)
ax.set_title("PhD Application Timeline with ★ Interviews & ▲ Campus Visits", fontsize=14, weight="bold")
plt.xticks(rotation=45)

legend_elements = [
    Line2D([0], [0], color=type_colors["SPH"], lw=4, label="SPH"),
    Line2D([0], [0], color=type_colors["SoP"], lw=4, label="SoP"),
    Line2D([0], [0], color=type_colors["SoM"], lw=4, label="SoM"),
    Line2D([0], [0], marker='*', color='w', label='Interview ★', markerfacecolor='black', markersize=10),
    Line2D([0], [0], marker='^', color='w', label='Campus Visit ▲', markerfacecolor='black', markersize=6),
    *[mpatches.Patch(color=color, label=region) for region, color in region_colors.items()]
]
ax.legend(handles=legend_elements, bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.savefig("/mnt/data/phd_app_timeline_FINAL.png", dpi=300)
plt.show()
