import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App Settings
    app_name: str = "Revenue Cycle Intelligence"
    debug: bool = False
    
    # API Keys
    anthropic_api_key: Optional[str] = None
    
    # Data Settings
    google_sheet_id: Optional[str] = None
    csv_data_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'synthetic_hospital_data.csv')
    cache_db_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'query_cache.db')
    
    # Agent Settings
    model_name: str = "claude-3-5-sonnet-20240620"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
