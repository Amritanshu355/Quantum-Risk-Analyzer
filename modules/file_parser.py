import pandas as pd
import io
from typing import List, Optional
from modules.risk_analyzer import CryptoAsset, CryptoAlgorithm


class FileParser:
    """Parser for Excel and CSV files containing cryptographic asset inventory."""
    
    REQUIRED_COLUMNS = {
        'Asset Name', 
        'Algorithm', 
        'Key Size', 
        'Usage Area', 
        'Data Sensitivity',
        'Data Volume (GB)'
    }
    
    ALGORITHM_MAP = {
        'RSA-2048': CryptoAlgorithm.RSA_2048,
        'RSA 2048': CryptoAlgorithm.RSA_2048,
        'RSA_2048': CryptoAlgorithm.RSA_2048,
        'RSA-4096': CryptoAlgorithm.RSA_4096,
        'RSA 4096': CryptoAlgorithm.RSA_4096,
        'RSA_4096': CryptoAlgorithm.RSA_4096,
        'ECC-256': CryptoAlgorithm.ECC_256,
        'ECC 256': CryptoAlgorithm.ECC_256,
        'ECC_256': CryptoAlgorithm.ECC_256,
        'ECC-384': CryptoAlgorithm.ECC_384,
        'ECC 384': CryptoAlgorithm.ECC_384,
        'ECC_384': CryptoAlgorithm.ECC_384,
        'AES-128': CryptoAlgorithm.AES_128,
        'AES 128': CryptoAlgorithm.AES_128,
        'AES_128': CryptoAlgorithm.AES_128,
        'AES-256': CryptoAlgorithm.AES_256,
        'AES 256': CryptoAlgorithm.AES_256,
        'AES_256': CryptoAlgorithm.AES_256,
        'SHA-256': CryptoAlgorithm.SHA_256,
        'SHA 256': CryptoAlgorithm.SHA_256,
        'SHA_256': CryptoAlgorithm.SHA_256,
        'SHA-3': CryptoAlgorithm.SHA_3,
        'SHA 3': CryptoAlgorithm.SHA_3,
        'SHA_3': CryptoAlgorithm.SHA_3,
        'DES': CryptoAlgorithm.DES,
        '3DES': CryptoAlgorithm.TRIPLE_DES,
        'Triple DES': CryptoAlgorithm.TRIPLE_DES,
    }
    
    SENSITIVITY_MAP = {
        'CRITICAL': 'Critical',
        'HIGH': 'High',
        'MEDIUM': 'Medium',
        'LOW': 'Low',
    }
    
    @classmethod
    def parse_excel(cls, file_bytes: bytes, file_extension: str = 'xlsx') -> pd.DataFrame:
        """Parse Excel file into DataFrame."""
        try:
            excel_data = pd.ExcelFile(io.BytesIO(file_bytes))
            dfs = []
            for sheet_name in excel_data.sheet_names:
                df = pd.read_excel(excel_data, sheet_name=sheet_name)
                dfs.append(df)
            combined_df = pd.concat(dfs, ignore_index=True) if len(dfs) > 1 else dfs[0]
            return combined_df
        except Exception as e:
            raise Exception(f"Error parsing Excel file: {str(e)}")
    
    @classmethod
    def parse_csv(cls, file_bytes: bytes) -> pd.DataFrame:
        """Parse CSV file into DataFrame."""
        try:
            return pd.read_csv(io.BytesIO(file_bytes))
        except Exception as e:
            raise Exception(f"Error parsing CSV file: {str(e)}")
    
    @classmethod
    def validate_dataframe(cls, df: pd.DataFrame) -> tuple[bool, List[str]]:
        """Validate that DataFrame contains all required columns and data."""
        missing_cols = []
        normalized_cols = [col.strip().lower().replace(' ', '_') for col in df.columns]
        
        for req_col in cls.REQUIRED_COLUMNS:
            normalized_req = req_col.strip().lower().replace(' ', '_')
            if normalized_req not in normalized_cols:
                missing_cols.append(req_col)
        
        if missing_cols:
            return False, missing_cols
        
        return True, []
    
    @classmethod
    def dataframe_to_assets(cls, df: pd.DataFrame) -> List[CryptoAsset]:
        """Convert DataFrame to list of CryptoAsset objects."""
        assets = []
        
        for _, row in df.iterrows():
            try:
                asset_name = cls._get_field(row, 'Asset Name')
                if pd.isna(asset_name) or str(asset_name).strip() == '':
                    continue
                
                algorithm_str = cls._get_field(row, 'Algorithm')
                algorithm = cls._parse_algorithm(algorithm_str)
                
                key_size = int(cls._get_field(row, 'Key Size', 2048))
                
                usage_area = cls._get_field(row, 'Usage Area', 'Core Banking')
                
                sensitivity_str = cls._get_field(row, 'Data Sensitivity', 'Medium')
                data_sensitivity = cls._parse_sensitivity(sensitivity_str)
                
                data_volume = float(cls._get_field(row, 'Data Volume (GB)', 100))
                
                asset = CryptoAsset(
                    name=str(asset_name),
                    algorithm=algorithm,
                    key_size=key_size,
                    usage_area=str(usage_area),
                    data_sensitivity=data_sensitivity,
                    estimated_data_volume_gb=data_volume
                )
                assets.append(asset)
                
            except Exception as e:
                continue
        
        return assets
    
    @classmethod
    def _get_field(cls, row, field_name, default=None):
        """Get field from row with case insensitivity."""
        normalized_fields = {
            col.strip().lower().replace(' ', '_'): col 
            for col in row.index
        }
        normalized_target = field_name.strip().lower().replace(' ', '_')
        
        if normalized_target in normalized_fields:
            return row[normalized_fields[normalized_target]]
        return default
    
    @classmethod
    def _parse_algorithm(cls, algo_str) -> CryptoAlgorithm:
        """Parse algorithm string to CryptoAlgorithm enum."""
        if isinstance(algo_str, CryptoAlgorithm):
            return algo_str
        
        algo_str = str(algo_str).strip().upper()
        
        if algo_str in cls.ALGORITHM_MAP:
            return cls.ALGORITHM_MAP[algo_str]
        
        for key in cls.ALGORITHM_MAP:
            if key.upper() in algo_str or algo_str in key.upper():
                return cls.ALGORITHM_MAP[key]
        
        return CryptoAlgorithm.RSA_2048
    
    @classmethod
    def _parse_sensitivity(cls, sensitivity_str) -> str:
        """Parse sensitivity string to standardized format."""
        if pd.isna(sensitivity_str):
            return 'Medium'
        
        sensitivity_str = str(sensitivity_str).strip().upper()
        
        if sensitivity_str in cls.SENSITIVITY_MAP:
            return cls.SENSITIVITY_MAP[sensitivity_str]
        
        for key in cls.SENSITIVITY_MAP:
            if key in sensitivity_str:
                return cls.SENSITIVITY_MAP[key]
        
        return 'Medium'
    
    @classmethod
    def parse_file(cls, file_bytes: bytes, file_type: str) -> tuple[bool, Optional[List[CryptoAsset]], Optional[str]]:
        """
        Main method to parse uploaded file.
        Returns (success, assets_list, error_message)
        """
        try:
            if file_type in ['xlsx', 'xls']:
                df = cls.parse_excel(file_bytes, file_type)
            elif file_type == 'csv':
                df = cls.parse_csv(file_bytes)
            else:
                return False, None, f"Unsupported file type: {file_type}"
            
            is_valid, missing_cols = cls.validate_dataframe(df)
            if not is_valid:
                return False, None, f"Missing required columns: {', '.join(missing_cols)}"
            
            assets = cls.dataframe_to_assets(df)
            
            if not assets:
                return False, None, "No valid crypto assets found in file"
            
            return True, assets, None
            
        except Exception as e:
            return False, None, f"Error processing file: {str(e)}"
