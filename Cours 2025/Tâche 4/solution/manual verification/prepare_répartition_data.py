import pandas as pd
import matplotlib.pyplot as plt

# Charger les données
data = pd.read_csv('prizes.csv')

# Filtrer les gagnants et les shortlistés
winners = data[data['person_role'] == 'winner']
shortlisted = data[data['person_role'] == 'shortlisted']

# Fonction pour calculer les proportions par genre
def calculate_proportions(df):
    proportions = {}
    counts = {}
    for prize in df['prize_alias'].unique():
        prize_data = df[df['prize_alias'] == prize]
        gender_counts = prize_data['gender'].value_counts(normalize=True) * 100
        gender_abs_counts = prize_data['gender'].value_counts()
        proportions[prize] = {
            'Femmes': f"{gender_counts.get('woman', 0):.1f}% ({gender_abs_counts.get('woman', 0)})",
            'Hommes': f"{gender_counts.get('man', 0):.1f}% ({gender_abs_counts.get('man', 0)})",
            'Non-binaires': f"{gender_counts.get('non-binary', 0):.1f}% ({gender_abs_counts.get('non-binary', 0)})"
        }
        counts[prize] = {
            'Femmes': gender_abs_counts.get('woman', 0),
            'Hommes': gender_abs_counts.get('man', 0),
            'Non-binaires': gender_abs_counts.get('non-binary', 0)
        }
    return proportions, counts

# Calculer les proportions pour les gagnants et les shortlistés
winners_proportions, winners_counts = calculate_proportions(winners)
shortlisted_proportions, shortlisted_counts = calculate_proportions(shortlisted)

# Afficher les résultats
for prize, values in winners_proportions.items():
    print(f"{prize} (Gagnants): {values}")

for prize, values in shortlisted_proportions.items():
    print(f"{prize} (Shortlistés): {values}")

# Sauvegarder les résultats dans un fichier CSV
winners_df_proportions = pd.DataFrame(winners_proportions).T
shortlisted_df_proportions = pd.DataFrame(shortlisted_proportions).T
winners_df_counts = pd.DataFrame(winners_counts).T
shortlisted_df_counts = pd.DataFrame(shortlisted_counts).T

winners_df_proportions.to_csv('winners_proportions.csv')
shortlisted_df_proportions.to_csv('shortlisted_proportions.csv')
winners_df_counts.to_csv('winners_counts.csv')
shortlisted_df_counts.to_csv('shortlisted_counts.csv')

# Visualisation
def plot_proportions(proportions, title):
    df = pd.DataFrame(proportions).T
    # Extract numeric values from percentage strings
    for col in df.columns:
        df[col] = df[col].str.extract(r'(\d+\.\d+)%', expand=False).astype(float)
    df = df.sort_values(by='Femmes', ascending=False)

    ax = df.plot(kind='barh', stacked=True, color=['#2b6cb0', '#a7dba0', '#f6c971'], figsize=(10, 8))

    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy()
        if width > 0:  # Only show label if there's a value
            ax.text(x + width / 2, y + height / 2, f"{width:.1f}%", ha='center', va='center')

    plt.title(title)
    plt.xlabel('Pourcentage')
    plt.ylabel('Prix')
    plt.legend(title='Genre')
    plt.tight_layout()
    plt.show()

plot_proportions(winners_proportions, "Répartition des genres — Gagnants par prix")
plot_proportions(shortlisted_proportions, "Répartition des genres — Shortlistés par prix")
