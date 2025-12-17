"""
Evaluation script for SHL Assessment Recommender
Calculates Mean Recall@K metrics on train data
"""
import json
import requests
import pandas as pd
from typing import List, Dict
import time

# Configuration
API_URL = "https://shl-assessment-recommender-8awb.onrender.com/recommend"
TRAIN_DATA_PATH = "../data/Gen_AI Dataset.xlsx"

def load_train_data() -> pd.DataFrame:
    """Load training data from Excel file"""
    try:
        # Try to read the train sheet
        df = pd.read_excel(TRAIN_DATA_PATH, sheet_name='Train-Set')
        print(f"✅ Loaded {len(df)} training examples")
        return df
    except Exception as e:
        print(f"❌ Error loading train data: {e}")
        print("📝 Please ensure Gen_AI Dataset.xlsx is in the parent directory")
        return None

def get_recommendations(query: str, use_ai: bool = False) -> List[Dict]:
    """Get recommendations from API"""
    try:
        response = requests.post(
            API_URL,
            json={"text": query, "use_ai": use_ai},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"⚠️ API Error for query '{query[:50]}...': {e}")
        return []

def calculate_recall_at_k(predicted_urls: List[str], relevant_urls: List[str], k: int = 10) -> float:
    """
    Calculate Recall@K metric
    
    Recall@K = (Number of relevant items in top K) / (Total relevant items)
    """
    if not relevant_urls:
        return 0.0
    
    # Get top K predictions
    top_k_predictions = predicted_urls[:k]
    
    # Count how many relevant items are in top K
    relevant_in_top_k = sum(1 for url in top_k_predictions if url in relevant_urls)
    
    # Calculate recall
    recall = relevant_in_top_k / len(relevant_urls)
    
    return recall

def evaluate_system(df: pd.DataFrame, k: int = 10) -> Dict:
    """
    Evaluate the recommendation system on train data
    
    Returns:
        Dictionary with evaluation metrics
    """
    recalls = []
    results = []
    
    print(f"\n🔍 Evaluating system with Recall@{k}...\n")
    
    for idx, row in df.iterrows():
        query = row.get('Query', row.get('query', ''))
        relevant_url = row.get('Assessment_url', row.get('assessment_url', ''))
        
        if not query or not relevant_url:
            print(f"⚠️ Skipping row {idx}: Missing query or URL")
            continue
        
        # Get recommendations
        recommendations = get_recommendations(query, use_ai=False)
        
        if not recommendations:
            print(f"❌ No recommendations for: {query[:50]}...")
            recalls.append(0.0)
            continue
        
        # Extract predicted URLs
        predicted_urls = [rec['url'] for rec in recommendations]
        
        # For train data, we might have multiple relevant URLs per query
        # If the data has one URL per row, we'll treat it as a list of one
        relevant_urls = [relevant_url] if isinstance(relevant_url, str) else relevant_url
        
        # Calculate recall
        recall = calculate_recall_at_k(predicted_urls, relevant_urls, k)
        recalls.append(recall)
        
        # Store result
        results.append({
            'query': query,
            'relevant_urls': relevant_urls,
            'predicted_urls': predicted_urls[:k],
            'recall': recall
        })
        
        print(f"Query {idx+1}/{len(df)}: Recall@{k} = {recall:.3f} | {query[:50]}...")
        
        # Small delay to avoid overwhelming API
        time.sleep(0.5)
    
    # Calculate mean recall
    mean_recall = sum(recalls) / len(recalls) if recalls else 0.0
    
    metrics = {
        'mean_recall_at_k': mean_recall,
        'k': k,
        'num_queries': len(recalls),
        'individual_recalls': recalls,
        'detailed_results': results
    }
    
    return metrics

def print_evaluation_report(metrics: Dict):
    """Print formatted evaluation report"""
    print("\n" + "="*60)
    print("📊 EVALUATION REPORT")
    print("="*60)
    print(f"\n📈 Mean Recall@{metrics['k']}: {metrics['mean_recall_at_k']:.4f}")
    print(f"📝 Number of Queries Evaluated: {metrics['num_queries']}")
    print(f"\n📉 Recall Distribution:")
    print(f"   Min: {min(metrics['individual_recalls']):.4f}")
    print(f"   Max: {max(metrics['individual_recalls']):.4f}")
    print(f"   Avg: {metrics['mean_recall_at_k']:.4f}")
    
    # Show some examples
    print(f"\n🔍 Sample Results (first 3):")
    for i, result in enumerate(metrics['detailed_results'][:3], 1):
        print(f"\n   Example {i}:")
        print(f"   Query: {result['query'][:60]}...")
        print(f"   Recall@{metrics['k']}: {result['recall']:.3f}")
        print(f"   Relevant: {len(result['relevant_urls'])} | Predicted: {len(result['predicted_urls'])}")
    
    print("\n" + "="*60)

def save_evaluation_results(metrics: Dict, output_path: str = "evaluation_results.json"):
    """Save evaluation results to JSON file"""
    # Remove detailed results for cleaner output
    summary = {
        'mean_recall_at_k': metrics['mean_recall_at_k'],
        'k': metrics['k'],
        'num_queries': metrics['num_queries'],
        'min_recall': min(metrics['individual_recalls']),
        'max_recall': max(metrics['individual_recalls']),
        'avg_recall': metrics['mean_recall_at_k']
    }
    
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n💾 Evaluation results saved to: {output_path}")

def main():
    """Main evaluation function"""
    print("🚀 Starting SHL Assessment Recommender Evaluation\n")
    
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
    
    # Load train data
    df = load_train_data()
    if df is None:
        return
    
    # Evaluate at different K values
    for k in [5, 10]:
        metrics = evaluate_system(df, k=k)
        print_evaluation_report(metrics)
        save_evaluation_results(metrics, f"evaluation_results_k{k}.json")
        print("\n" + "-"*60 + "\n")

if __name__ == "__main__":
    main()
