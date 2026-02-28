# KPI Definitions and Styling
KPI_METADATA = {
    'net_collection_rate': {
        'label': 'Net Collection Rate',
        'format': 'percent',
        'is_inverse': False,
        'description': '(Payments / Allowed Amount) x 100',
        'color': '#2E86C1'
    },
    'gross_collection_rate': {
        'label': 'Gross Collection Rate',
        'format': 'percent',
        'is_inverse': False,
        'description': '(Payments / Charges) x 100',
        'color': '#3498DB'
    },
    'days_in_ar': {
        'label': 'Days in A/R',
        'format': 'days',
        'is_inverse': True,
        'description': '(Total A/R / Average Daily Net Revenue)',
        'color': '#117864'
    },
    'clean_claim_rate': {
        'label': 'Clean Claim Rate',
        'format': 'percent',
        'is_inverse': False,
        'description': '(Claims Accepted on First Submission / Total Claims) x 100',
        'color': '#28B463'
    },
    'denial_rate': {
        'label': 'Denial Rate',
        'format': 'percent',
        'is_inverse': True,
        'description': '(Denied Claims / Total Claims) x 100',
        'color': '#E67E22'
    },
    'ar_over_90_pct': {
        'label': 'A/R Over 90 Days %',
        'format': 'percent',
        'is_inverse': True,
        'description': '(A/R > 90 days / Total A/R) x 100',
        'color': '#CB4335'
    },
    'cost_to_collect': {
        'label': 'Cost to Collect',
        'format': 'currency',
        'is_inverse': True,
        'description': '(Total RC Department Cost / Total Collections)',
        'color': '#5D6D7E'
    },
    'charge_lag': {
        'label': 'Charge Lag',
        'format': 'days',
        'is_inverse': True,
        'description': 'Avg days between service date and charge entry',
        'color': '#7D3C98'
    },
    'denial_overturn_rate': {
        'label': 'Denial Overturn Rate',
        'format': 'percent',
        'is_inverse': False,
        'description': '(Overturned Denials / Total Denials) x 100',
        'color': '#F1C40F'
    },
    'cash_as_pct_nr': {
        'label': 'Cash as % of Net Revenue',
        'format': 'percent',
        'is_inverse': False,
        'description': '(Total Cash Collected / Net Revenue) x 100',
        'color': '#2471A3'
    },
    'bad_debt_rate': {
        'label': 'Bad Debt Rate',
        'format': 'percent',
        'is_inverse': True,
        'description': '(Bad Debt Write-offs / Net Revenue) x 100',
        'color': '#922B21'
    },
    'pos_collection_rate': {
        'label': 'POS Collections',
        'format': 'percent',
        'is_inverse': False,
        'description': '(POS Collections / Total Patient Responsibility) x 100',
        'color': '#1E8449'
    }
}

# Thresholds for Anomaly Detection
ANOMALY_THRESHOLDS = {
    'denial_rate': 0.15,  # 15% WoW increase
    'net_collection_rate': 0.05, # 5% YoY dip
    'days_in_ar': 0.10, # 10% WoW increase
}

# Visual Styling
CHART_THEME_COLORS = [
    '#1B4F72', '#2874A6', '#85C1E9', '#D6EAF8', 
    '#0B5345', '#117864', '#138D75', '#A3E4D7'
]

# Payer Categories
PAYER_CATEGORIES = ['Commercial', 'Medicare', 'Medicaid', 'Self-Pay', 'Blue Cross']
