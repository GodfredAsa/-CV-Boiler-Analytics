import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read the Excel file
df = pd.read_excel('data.xlsx')

# Basic data exploration
print("\n=== Basic Data Overview ===")
print(f"Total number of records: {len(df)}")
print("\nColumns in the dataset:")
print(df.columns.tolist())

# Examine unique values in Toestel type
print("\n=== Unique Values in Toestel type ===")
print(df['Toestel type'].unique())

# Filter for CV boilers (where 'Toestel type' contains 'KETEL')
cv_boilers = df[df['Toestel type'].str.contains('KETEL', case=False, na=False)]

# Analyze CV boiler distribution per postal code
cv_by_postal = cv_boilers.groupby('Opstel Postcode').size().reset_index(name='cv_boiler_count')

print("\nTop 10 postal codes by number of CV boilers:")
print(cv_by_postal.sort_values('cv_boiler_count', ascending=False).head(10))

# Calculate statistics about CV boilers
print("\n=== CV Boiler Analysis ===")
total_cv = cv_by_postal['cv_boiler_count'].sum()
print(f"Total number of CV boilers: {total_cv}")
print(f"Average number of CV boilers per postal code: {cv_by_postal['cv_boiler_count'].mean():.2f}")
print(f"Median number of CV boilers per postal code: {cv_by_postal['cv_boiler_count'].median():.2f}")

# Identify individual CV boilers (postal codes with only 1 CV boiler)
individual_cv = cv_by_postal[cv_by_postal['cv_boiler_count'] == 1]
print("\n=== Individual CV Boiler Analysis ===")
print(f"Number of postal codes with individual CV boilers: {len(individual_cv)}")
print(f"Total number of individual CV boilers: {individual_cv['cv_boiler_count'].sum()}")

# Calculate potential Gateway coverage
print("\n=== Gateway Coverage Analysis ===")
print("Assuming RF coverage requirements:")
print("- Urban areas: < 1km line-of-sight")
print("- Suburban areas: < 3km line-of-sight")
print("- LoRa packet loss < 1% per sensor per 24 hours")
print("- Min RSSI > -120 dBm")
print("- Min SNR > -10 dB")

# Create visualizations
plt.figure(figsize=(12, 6))
sns.histplot(data=cv_by_postal, x='cv_boiler_count', bins=30)
plt.title('Distribution of CV Boilers per Postal Code')
plt.xlabel('Number of CV Boilers')
plt.ylabel('Count of Postal Codes')
plt.savefig('cv_distribution.png')

# Calculate cost implications
GATEWAY_COST = 500  # Example cost in euros
INSTALLATION_COST = 300  # Example cost in euros

total_individual_cv = individual_cv['cv_boiler_count'].sum()
total_cost = total_individual_cv * (GATEWAY_COST + INSTALLATION_COST)

print("\n=== Cost Analysis ===")
print(f"Estimated total cost for individual Gateways: €{total_cost:,.2f}")
print(f"Cost per individual CV boiler: €{(GATEWAY_COST + INSTALLATION_COST):,.2f}")

# Save detailed analysis to CSV
cv_by_postal.to_csv('cv_analysis_results.csv', index=False) 