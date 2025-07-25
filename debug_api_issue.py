import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def debug_api_issue():
    """Debug why bond recommendations are missing from API response"""
    
    # Same profile that worked in direct test
    profile = {
        "age": 55,
        "income": 120000,
        "capital": 100000,
        "expenses": 80000,
        "emi": 25000,
        "liquidity_need": 30000,
        "dependents": 2,
        "confidence": 0.2,
        "knowledge": 0.3,
        "comfort_with_negatives": 0.1,
        "market_awareness": 0.4,
        "experience": 0.2
    }
    
    print("DEBUGGING API BOND RECOMMENDATIONS ISSUE")
    print("=" * 60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/investment-profile/",
            json=profile,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            data = response.json()
            
            print("API Response Keys:", list(data.keys()))
            
            # Check debt allocation
            if 'allocation' in data and 'debt' in data['allocation']:
                debt_info = data['allocation']['debt']
                if isinstance(debt_info, dict):
                    debt_amount = debt_info['amount']
                    debt_pct = debt_info['percentage']
                    print(f"Debt Allocation: {debt_pct:.1f}% (Rs.{debt_amount:,.0f})")
                    
                    if debt_amount > 0:
                        print("✓ Debt allocation exists - should generate bond recommendations")
                    else:
                        print("✗ No debt allocation - no bond recommendations expected")
                else:
                    print(f"Debt Allocation: {debt_info}%")
            
            # Check for bond recommendations
            if 'bond_recommendations' in data:
                bonds = data['bond_recommendations']
                print(f"✓ Bond recommendations found: {len(bonds)} bonds")
                for bond in bonds:
                    print(f"  - {bond['name']} ({bond['symbol']}): {bond['weight']:.1f}%")
            else:
                print("✗ Bond recommendations missing from API response")
                
                # Check what recommendations ARE present
                rec_keys = [k for k in data.keys() if 'recommendation' in k]
                print(f"Available recommendations: {rec_keys}")
            
            return data
        else:
            print(f"API Error: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    debug_api_issue()