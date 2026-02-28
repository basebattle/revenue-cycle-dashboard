import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_synthetic_data(num_rows=15000, start_date='2024-01-01', end_date='2025-12-31'):
    """Generates synthetic hospital financial data for testing."""
    np.random.seed(42)  # For reproducibility

    # Payers and their characteristics
    payers = {
        'UnitedHealthcare': {'weight': 0.25, 'category': 'Commercial', 'denial_rate': 0.12, 'payment_lag_avg': 45},
        'Aetna': {'weight': 0.15, 'category': 'Commercial', 'denial_rate': 0.11, 'payment_lag_avg': 50},
        'BCBS': {'weight': 0.20, 'category': 'Commercial', 'denial_rate': 0.09, 'payment_lag_avg': 40},
        'Medicare': {'weight': 0.20, 'category': 'Medicare', 'denial_rate': 0.05, 'payment_lag_avg': 20},
        'Medicaid': {'weight': 0.10, 'category': 'Medicaid', 'denial_rate': 0.08, 'payment_lag_avg': 60},
        'Self-Pay': {'weight': 0.10, 'category': 'Self-Pay', 'denial_rate': 0.15, 'payment_lag_avg': 90}
    }

    payer_names = list(payers.keys())
    payer_weights = [p['weight'] for p in payers.values()]

    # Denial Reasons
    denial_reasons = {
        'Prior Auth': 0.30,
        'Medical Necessity': 0.25,
        'Coding Error': 0.20,
        'Timely Filing': 0.10,
        'Missing Info': 0.15
    }
    reasons = list(denial_reasons.keys())
    reason_weights = list(denial_reasons.values())

    # Generate dates
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    delta_days = (end_dt - start_dt).days
    
    # Pre-generate random values
    claims_payer = np.random.choice(payer_names, size=num_rows, p=payer_weights)
    claims_service_date = [start_dt + timedelta(days=np.random.randint(0, delta_days)) for _ in range(num_rows)]
    
    data = []
    for i in range(num_rows):
        payer_name = claims_payer[i]
        payer_info = payers[payer_name]
        service_date = claims_service_date[i]
        
        # Charges: weighted toward 500-5000
        if np.random.random() < 0.8:
            charges = np.random.uniform(500, 5000)
        else:
            charges = np.random.uniform(5000, 45000)
            
        # Allowed Amount: usually 40-70% of charges
        allowed_pct = np.random.uniform(0.4, 0.7)
        allowed_amount = charges * allowed_pct
        
        # Denial logic
        is_denied = np.random.random() < payer_info['denial_rate']
        
        # Claim Status
        if is_denied:
            claim_status = 'Denied'
            denial_reason = np.random.choice(reasons, p=reason_weights)
            denial_category = 'Technical' if denial_reason in ['Timely Filing', 'Missing Info'] else 'Clinical'
            payments = 0
            patient_responsibility = 0
            payment_date = None
        else:
            claim_status = 'Paid'
            denial_reason = None
            denial_category = None
            # Payments: 70-90% of allowed
            payments = allowed_amount * np.random.uniform(0.7, 0.9)
            patient_responsibility = allowed_amount - payments
            
            # Payment Date
            lag = np.random.normal(payer_info['payment_lag_avg'], 10)
            lag = max(1, int(lag))
            payment_date = service_date + timedelta(days=lag)

        # POS Collections: 10-30% of patient responsibility for some
        pos_collections = 0
        if payer_info['category'] == 'Commercial' or payer_info['category'] == 'Self-Pay':
             if np.random.random() < 0.6: # 60% chance they pay something at POS
                pos_collections = patient_responsibility * np.random.uniform(0.1, 0.5)

        # Charge entry date: 1-5 days after service date
        charge_entry_date = service_date + timedelta(days=np.random.randint(1, 5))
        
        # Claim submission date: 1-3 days after charge entry
        claim_submission_date = charge_entry_date + timedelta(days=np.random.randint(1, 3))

        data.append({
            'claim_id': f'CLM-{100000 + i}',
            'service_date': service_date.strftime('%Y-%m-%d'),
            'payer_name': payer_name,
            'payer_category': payer_info['category'],
            'cpt_code': np.random.choice(['99213', '99214', '99215', '45378', '45385', '70450', '71046']),
            'charges': round(charges, 2),
            'allowed_amount': round(allowed_amount, 2),
            'payments': round(payments, 2),
            'adjustments': round(charges - allowed_amount, 2),
            'patient_responsibility': round(patient_responsibility, 2),
            'pos_collections': round(pos_collections, 2),
            'claim_status': claim_status,
            'denial_reason': denial_reason,
            'denial_category': denial_category,
            'charge_entry_date': charge_entry_date.strftime('%Y-%m-%d'),
            'claim_submission_date': claim_submission_date.strftime('%Y-%m-%d'),
            'payment_date': payment_date.strftime('%Y-%m-%d') if payment_date else None,
            'facility': 'Main Campus' if np.random.random() < 0.8 else 'East Wing'
        })

    df = pd.DataFrame(data)
    
    # Save to CSV
    output_path = os.path.join(os.path.dirname(__file__), 'synthetic_hospital_data.csv')
    df.to_csv(output_path, index=False)
    print(f"Generated {num_rows} rows of synthetic data at {output_path}")

if __name__ == "__main__":
    generate_synthetic_data()
