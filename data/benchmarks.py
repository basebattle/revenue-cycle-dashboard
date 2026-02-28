from typing import Dict, Any, Optional

class BenchmarkData:
    """Provides industry benchmark data for revenue cycle KPIs."""

    def __init__(self):
        # HFMA 2024 medians for community hospitals (100-249 beds)
        # From TRD Appendix B
        self.benchmarks = {
            'net_collection_rate': {'25th': 94.5, '50th': 96.0, '75th': 97.8, '90th': 98.5},
            'gross_collection_rate': {'25th': 40.0, '50th': 48.0, '75th': 55.0, '90th': 60.0},
            'days_in_ar': {'25th': 48.0, '50th': 42.0, '75th': 36.0, '90th': 32.0},
            'clean_claim_rate': {'25th': 88.0, '50th': 92.0, '75th': 95.5, '90th': 97.0},
            'denial_rate': {'25th': 12.0, '50th': 9.5, '75th': 7.0, '90th': 5.5},
            'cost_to_collect': {'25th': 0.060, '50th': 0.045, '75th': 0.038, '90th': 0.032},
            'ar_over_90_pct': {'25th': 25.0, '50th': 20.0, '75th': 15.0, '90th': 12.0},
            'charge_lag': {'25th': 4.5, '50th': 3.0, '75th': 2.0, '90th': 1.5},
            'bad_debt_rate': {'25th': 5.0, '50th': 3.5, '75th': 2.0, '90th': 1.2},
            'pos_collection_rate': {'25th': 50.0, '50th': 65.0, '75th': 75.0, '90th': 85.0}
        }

    def get_benchmarks(self, hospital_type: str = "community", bed_count: int = 200) -> Dict[str, Any]:
        """Returns benchmark comparison for given hospital profile."""
        # For now, we only have one set of benchmarks. In V2, we can add more profiles.
        return self.benchmarks

    def get_benchmark_status(self, metric: str, value: float) -> str:
        """Compares value against benchmark and returns status emoji."""
        b = self.benchmarks.get(metric)
        if not b:
             return "⚪"
             
        # "Good" direction is up for some, down for others
        inverse_metrics = ['denial_rate', 'days_in_ar', 'cost_to_collect', 'ar_over_90_pct', 'charge_lag', 'bad_debt_rate']
        
        if metric in inverse_metrics:
            if value <= b['90th']: return "🌟"
            if value <= b['75th']: return "✅"
            if value <= b['50th']: return "⚠️"
            return "🔴"
        else:
            if value >= b['90th']: return "🌟"
            if value >= b['75th']: return "✅"
            if value >= b['50th']: return "⚠️"
            return "🔴"
