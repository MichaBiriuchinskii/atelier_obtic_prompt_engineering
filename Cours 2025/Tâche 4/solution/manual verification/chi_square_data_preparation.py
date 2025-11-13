import pandas as pd

# Charger les données
data = pd.read_csv('prizes.csv')

# Trouver les catégories communes
winners_prizes = set(data[data['person_role'] == 'winner']['prize_alias'].unique())
shortlisted_prizes = set(data[data['person_role'] == 'shortlisted']['prize_alias'].unique())
common_prizes = sorted(winners_prizes & shortlisted_prizes)

print(f"Prix communs ({len(common_prizes)}):")
for prize in common_prizes:
    print(f"  - {prize}")

# Filtrer les données pour les prix communs uniquement
data_common = data[data['prize_alias'].isin(common_prizes)]

# Séparer winners et shortlisted
winners = data_common[data_common['person_role'] == 'winner']
shortlisted = data_common[data_common['person_role'] == 'shortlisted']

# Fonction pour compter par genre et prix
def count_by_gender_and_prize(df):
    counts = {}
    for prize in common_prizes:
        prize_data = df[df['prize_alias'] == prize]
        gender_counts = prize_data['gender'].value_counts()
        counts[prize] = {
            'Femmes': gender_counts.get('woman', 0),
            'Hommes': gender_counts.get('man', 0),
            'Non-binaires': gender_counts.get('non-binary', 0)
        }
    return counts

# Calculer les comptes
winners_counts = count_by_gender_and_prize(winners)
shortlisted_counts = count_by_gender_and_prize(shortlisted)

# Créer les DataFrames
winners_df = pd.DataFrame(winners_counts).T
shortlisted_df = pd.DataFrame(shortlisted_counts).T

# Ajouter une ligne de totaux
winners_df.loc['TOTAL'] = winners_df.sum()
shortlisted_df.loc['TOTAL'] = shortlisted_df.sum()

print("\n=== GAGNANTS (Winners) ===")
print(winners_df)

print("\n=== SHORTLISTÉS (Shortlisted) ===")
print(shortlisted_df)

# Sauvegarder les fichiers
winners_df.to_csv('chi_square_winners.csv')
shortlisted_df.to_csv('chi_square_shortlisted.csv')

# Créer une table combinée pour le test chi-carré
# Format: rows = outcome (winner/shortlisted), columns = gender
chi_square_table = pd.DataFrame({
    'Femmes': [winners_df.loc['TOTAL', 'Femmes'], shortlisted_df.loc['TOTAL', 'Femmes']],
    'Hommes': [winners_df.loc['TOTAL', 'Hommes'], shortlisted_df.loc['TOTAL', 'Hommes']],
    'Non-binaires': [winners_df.loc['TOTAL', 'Non-binaires'], shortlisted_df.loc['TOTAL', 'Non-binaires']]
}, index=['Winner', 'Shortlisted'])

print("\n=== TABLE POUR TEST CHI-CARRÉ ===")
print(chi_square_table)

chi_square_table.to_csv('chi_square_contingency_table.csv')

print("\n✓ Fichiers sauvegardés:")
print("  - chi_square_winners.csv")
print("  - chi_square_shortlisted.csv")
print("  - chi_square_contingency_table.csv")
