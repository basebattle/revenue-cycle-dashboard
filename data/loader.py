import pandas as pd
import os
import logging
from datetime import date
from typing import Optional, Tuple, Dict, Any
from .schemas import ClaimRecord, DataQualityReport

logger = logging.getLogger(__name__)

class DataLoader:
    """Handles data ingestion from CSV or Google Sheets."""

    def __init__(self, data_path: Optional[str] = None):
        if data_path is None:
            # Fallback to the synthetic data path
            data_path = os.path.join(os.path.dirname(__file__), 'synthetic_hospital_data.csv')
        self.data_path = data_path

    def load_from_csv(self) -> Tuple[pd.DataFrame, DataQualityReport]:
        """Loads data from CSV file and performs validation."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found at {self.data_path}")

        try:
            df = pd.read_csv(self.data_path)
            
            # Basic normalization
            df['service_date'] = pd.to_datetime(df['service_date']).dt.date
            df['charge_entry_date'] = pd.to_datetime(df['charge_entry_date']).dt.date
            df['claim_submission_date'] = pd.to_datetime(df['claim_submission_date']).dt.date
            df['payment_date'] = pd.to_datetime(df['payment_date']).dt.date

            total_rows = len(df)
            valid_rows = 0
            invalid_rows = 0
            missing_payer_name = df['payer_name'].isna().sum()
            
            today = date.today()
            future_service_dates = (df['service_date'] > today).sum()

            validation_errors = []
            
            # Validate rows using Pydantic (expensive on large datasets - can be optimized)
            # For 15-20k rows it should be okay
            for idx, row in df.iterrows():
                try:
                    ClaimRecord(**row.to_dict())
                    valid_rows += 1
                except Exception as e:
                    invalid_rows += 1
                    if len(validation_errors) < 10: # Limit error collection
                        validation_errors.append(f"Row {idx}: {str(e)}")

            report = DataQualityReport(
                total_rows=total_rows,
                valid_rows=valid_rows,
                invalid_rows=invalid_rows,
                missing_payer_name=missing_payer_name,
                future_service_dates=future_service_dates,
                validation_errors=validation_errors
            )

            return df, report

        except Exception as e:
            logger.error(f"Error loading CSV data: {str(e)}")
            return pd.DataFrame(), DataQualityReport(
                total_rows=0, valid_rows=0, invalid_rows=0,
                missing_payer_name=0, future_service_dates=0,
                validation_errors=[str(e)], status="error"
            )

    def load_from_google_sheets(self, sheet_id: str) -> Tuple[pd.DataFrame, DataQualityReport]:
        """Loads data from Google Sheets. Placeholder for now."""
        # TODO: Implement gspread logic as specified in TRD Section 2.7
        logger.warning("Google Sheets loading not implemented yet. Using CSV.")
        return self.load_from_csv()

    def refresh_data(self) -> pd.DataFrame:
        """Force a data refresh and update storage."""
        # For now, just reload the CSV
        df, report = self.load_from_csv()
        if report.status == "error":
            logger.error(f"Failed to refresh data: {report.validation_errors}")
        return df
