import pandas as pd

# Create sample data
sample_data = [
    ["Core Banking TLS", "RSA-2048", 2048, "Core Banking", "Critical", 5000],
    ["Payment Gateway", "RSA-4096", 4096, "Payment Processing", "Critical", 2000],
    ["Customer Auth Keys", "ECC-256", 256, "Customer Authentication", "High", 500],
    ["Mobile App Signing", "ECC-384", 384, "Mobile Banking", "High", 100],
    ["Data-at-Rest", "AES-256", 256, "Data Storage", "Critical", 50000],
    ["API Gateway", "RSA-2048", 2048, "API Security", "Medium", 300],
    ["ATM Communication", "3DES", 168, "ATM Network", "High", 150],
]

# Create DataFrame
df = pd.DataFrame(
    sample_data,
    columns=[
        "Asset Name", 
        "Algorithm", 
        "Key Size", 
        "Usage Area", 
        "Data Sensitivity", 
        "Data Volume (GB)"
    ]
)

# Save to Excel
excel_file = "asset_inventory_template.xlsx"
df.to_excel(excel_file, index=False, engine='openpyxl')

print(f"Sample template created: {excel_file}")
print("\nFile preview:")
print(df)
