import pandas as pd
from pymongo import MongoClient

# Load the dataset from the provided URL (ensure you have the file downloaded)
file_path = 'Zomato_Data_Set/zomato.csv'
country_code_file_path = 'Zomato_Data_Set/Country-Code.xlsx'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path, encoding='ISO-8859-1')
country_code = pd.read_excel(country_code_file_path)
final_df=pd.merge(df,country_code,on="Country Code",how="left")
final_df['Cuisines'] = final_df['Cuisines'].fillna('Not Specified')


# Preprocess the DataFrame if necessary (e.g., handle missing values, rename columns)
# df.dropna(subset=['Restaurant Name', 'Address', 'Cuisines'], inplace=True)

# MongoDB configuration
client = MongoClient('localhost', 27017)
db = client['zomato_db']
collection = db['restaurants']

# Load data into MongoDB
data = final_df.to_dict(orient='records')
collection.insert_many(data)
print("Data successfully loaded into MongoDB.")
