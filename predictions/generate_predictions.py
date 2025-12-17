"""
Generate test predictions for SHL Assessment Recommender
Creates CSV file in required format: firstname_lastname.csv
"""
import json
import requests
import pandas as pd
from typing import List, Dict
import time

# Configuration
API_URL = "https://shl-assessment-recommender-8awb.onrender.com/recommend"
TEST_DATA_PATH = "../data/Gen_AI Dataset.xlsx"
OUTPUT_CSV = "abhay_gupta.csv"

def load_test_data() -> pd.DataFrame:
    """Load test data from Excel file"""
    try:
        # Try to read the test sheet
        df = pd.read_excel(TEST_DATA_PATH, sheet_name='Test-Set')
        print(f"✅ Loaded {len(df)} test queries")
        return df
    except Exception as e:
        print(f"❌ Error loading test data: {e}")
        print("📝 Please ensure Gen_AI Dataset.xlsx is in the parent directory")
        return None

def get_recommendations(query: str, use_ai: bool = False, max_results: int = 10) -> List[Dict]:
    """Get recommendations from API"""
    try:
        response = requests.post(
            API_URL,
            json={"text": query, "use_ai": use_ai},
            timeout=30
        )
        response.raise_for_status()
        results = response.json()
        return results[:max_results]  # Ensure max 10 results
    except Exception as e:
        print(f"⚠️ API Error for query '{query[:50]}...': {e}")
        return []

def generate_predictions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate predictions for all test queries
    
    Returns:
        DataFrame with columns: Query, Assessment_url
    """
    predictions = []
    
    print(f"\n🔍 Generating predictions for {len(df)} test queries...\n")
    
    for idx, row in df.iterrows():
        query = row.get('Query', row.get('query', ''))
        
        if not query:
            print(f"⚠️ Skipping row {idx}: Missing query")
            continue
        
        print(f"Processing {idx+1}/{len(df)}: {query[:60]}...")
        
        # Get recommendations
        recommendations = get_recommendations(query, use_ai=False, max_results=10)
        
        if not recommendations:
            print(f"   ❌ No recommendations found")
            # Add at least one empty entry to maintain format
            predictions.append({
                'Query': query,
                'Assessment_url': ''
            })
            continue
        
        # Add each recommendation as a separate row
        for rec in recommendations:
            predictions.append({
                'Query': query,
                'Assessment_url': rec['url']
            })
        
        print(f"   ✅ Added {len(recommendations)} recommendations")
        
        # Small delay to avoid overwhelming API
        time.sleep(0.5)
    
    # Create DataFrame
    predictions_df = pd.DataFrame(predictions)
    
    return predictions_df

def save_predictions(df: pd.DataFrame, output_path: str):
    """Save predictions to CSV file"""
    df.to_csv(output_path, index=False)
    print(f"\n💾 Predictions saved to: {output_path}")
    print(f"📊 Total rows: {len(df)}")
    print(f"📝 Unique queries: {df['Query'].nunique()}")

def validate_format(df: pd.DataFrame) -> bool:
    """Validate the CSV format"""
    print("\n🔍 Validating CSV format...")
    
    # Check columns
    required_columns = ['Query', 'Assessment_url']
    if list(df.columns) != required_columns:
        print(f"❌ Invalid columns. Expected: {required_columns}, Got: {list(df.columns)}")
        return False
    
    print("✅ Columns are correct")
    
    # Check for empty values
    empty_queries = df['Query'].isna().sum()
    empty_urls = df['Assessment_url'].isna().sum()
    
    if empty_queries > 0:
        print(f"⚠️ Warning: {empty_queries} empty queries found")
    if empty_urls > 0:
        print(f"⚠️ Warning: {empty_urls} empty URLs found")
    
    # Show sample
    print("\n📋 Sample rows:")
    print(df.head(10).to_string(index=False))
    
    return True

def main():
    """Main prediction generation function"""
    print("🚀 Starting Test Predictions Generation\n")
    
    # Check if API is running
    try:
        health_response = requests.get("https://shl-assessment-recommender-8awb.onrender.com/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ API is running and healthy\n")
        else:
            print("⚠️ API health check failed")
            return
    except Exception as e:
        print(f"❌ Cannot connect to API at {API_URL}")
        print("Please ensure the API is deployed and accessible")
        return
    
    # Load test data
    df = load_test_data()
    if df is None:
        return
    
    # Generate predictions
    predictions_df = generate_predictions(df)
    
    # Validate format
    if not validate_format(predictions_df):
        print("\n❌ Format validation failed")
        return
    
    # Save to CSV
    save_predictions(predictions_df, OUTPUT_CSV)
    
    print("\n✅ Predictions generation complete!")
    print(f"\n📤 Submit this file: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
