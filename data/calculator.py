import pandas as pd
import numpy as np
from datetime import date, timedelta
from typing import Dict, Any, Optional, List

class KPICalculator:
    """Calculates Revenue Cycle KPIs from DataFrame."""

    def calculate_all(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculates all 12 core core KPIs."""
        if df.empty:
            return {
                'net_collection_rate': None,
                'gross_collection_rate': None,
                'days_in_ar': None,
                'clean_claim_rate': None,
                'denial_rate': None,
                'denial_overturn_rate': None,
                'cost_to_collect': None,
                'charge_lag': None,
                'ar_over_90_pct': None,
                'cash_as_pct_nr': None,
                'bad_debt_rate': None,
                'pos_collection_rate': None
            }

        # Helper to safely sum columns
        def safe_sum(col):
            return df[col].sum() if col in df.columns else 0

        # Helper to safely count rows
        def safe_count(condition):
            # If columns needed for condition are missing, return 0
            # Condition is expected to be a boolean series or lambda
            try:
                return len(df[condition])
            except (KeyError, ValueError):
                return 0

        # 1. Net Collection Rate
        payments_sum = safe_sum('payments')
        allowed_sum = safe_sum('allowed_amount')
        net_col_rate = (payments_sum / allowed_sum * 100) if allowed_sum > 0 else 0

        # 2. Gross Collection Rate
        charges_sum = safe_sum('charges')
        gross_col_rate = (payments_sum / charges_sum * 100) if charges_sum > 0 else 0

        # 3. Days in A/R (Approximate using 365 days)
        adjustments_sum = safe_sum('adjustments')
        total_ar = charges_sum - payments_sum - adjustments_sum
        
        avg_daily_revenue = charges_sum / 365 if charges_sum > 0 else 0 # Simplified
        days_in_ar = total_ar / avg_daily_revenue if avg_daily_revenue > 0 else 0

        # 4. Clean Claim Rate 
        total_claims = len(df)
        clean_claims = safe_count(df['claim_status'] != 'Denied') if 'claim_status' in df.columns else total_claims
        clean_claim_rate = (clean_claims / total_claims * 100) if total_claims > 0 else 0

        # 5. Denial Rate
        denied_claims = safe_count(df['claim_status'] == 'Denied') if 'claim_status' in df.columns else 0
        denial_rate = (denied_claims / total_claims * 100) if total_claims > 0 else 0

        # 6. Denial Overturn Rate
        overturned_denials = denied_claims * 0.44 # Mocked constant
        denial_overturn_rate = (overturned_denials / denied_claims * 100) if denied_claims > 0 else 0

        # 7. Cost to Collect 
        cost_to_collect = 0.042 # Mocked constant per TRD

        # 8. Charge Lag
        if 'service_date' in df.columns and 'charge_entry_date' in df.columns:
            df_temp = df.copy()
            df_temp['service_dt'] = pd.to_datetime(df_temp['service_date'])
            df_temp['charge_entry_dt'] = pd.to_datetime(df_temp['charge_entry_date'])
            charge_lag = (df_temp['charge_entry_dt'] - df_temp['service_dt']).dt.days.mean()
        else:
            charge_lag = 0

        # 9. A/R Over 90 Days %
        ninety_days_ago = date.today() - timedelta(days=90)
        if 'claim_status' in df.columns and 'service_date' in df.columns:
            aging_df = df[(df['claim_status'] != 'Paid') & (pd.to_datetime(df['service_date']).dt.date < ninety_days_ago)]
            ar_over_90 = (len(aging_df) / total_claims * 100) if total_claims > 0 else 0
        else:
            ar_over_90 = 0

        # 10. Cash as % of Net Revenue
        cash_as_pct_nr = (payments_sum / allowed_sum * 100) if allowed_sum > 0 else 0

        # 11. Bad Debt Rate
        bad_debt_write_offs = adjustments_sum * 0.05 # Mocked as portion of adjustments
        bad_debt_rate = (bad_debt_write_offs / allowed_sum * 100) if allowed_sum > 0 else 0

        # 12. Point-of-Service Collections
        pt_resp_sum = safe_sum('patient_responsibility')
        pos_col_sum = safe_sum('pos_collections')
        pos_collection_rate = (pos_col_sum / pt_resp_sum * 100) if pt_resp_sum > 0 else 0

        return {
            'net_collection_rate': round(net_col_rate, 1),
            'gross_collection_rate': round(gross_col_rate, 1),
            'days_in_ar': round(days_in_ar, 1),
            'clean_claim_rate': round(clean_claim_rate, 1),
            'denial_rate': round(denial_rate, 1),
            'denial_overturn_rate': round(denial_overturn_rate, 1),
            'cost_to_collect': round(cost_to_collect, 3),
            'charge_lag': round(charge_lag, 1),
            'ar_over_90_pct': round(ar_over_90, 1),
            'cash_as_pct_nr': round(cash_as_pct_nr, 1),
            'bad_debt_rate': round(bad_debt_rate, 1),
            'pos_collection_rate': round(pos_collection_rate, 1)
        }


    def calculate_trends(self, df: pd.DataFrame, months: int = 12) -> List[Dict[str, Any]]:
        """Calculates monthly KPI trends for charting."""
        df['service_month'] = pd.to_datetime(df['service_date']).dt.to_period('M')
        monthly_trends = []
        
        # Sort months in descending order to get last 'months' months
        periods = sorted(df['service_month'].unique())[-months:]
        
        for period in periods:
            month_df = df[df['service_month'] == period]
            kpis = self.calculate_all(month_df)
            kpis['period'] = str(period)
            monthly_trends.append(kpis)
            
        return monthly_trends
