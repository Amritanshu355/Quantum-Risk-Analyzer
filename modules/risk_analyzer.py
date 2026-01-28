import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class ThreatLevel(Enum):
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    MINIMAL = 1


class CryptoAlgorithm(Enum):
    RSA_2048 = "RSA-2048"
    RSA_4096 = "RSA-4096"
    ECC_256 = "ECC-256"
    ECC_384 = "ECC-384"
    AES_128 = "AES-128"
    AES_256 = "AES-256"
    SHA_256 = "SHA-256"
    SHA_3 = "SHA-3"
    DES = "DES"
    TRIPLE_DES = "3DES"


@dataclass
class CryptoAsset:
    name: str
    algorithm: CryptoAlgorithm
    key_size: int
    usage_area: str
    data_sensitivity: str
    estimated_data_volume_gb: float


@dataclass
class RiskAssessment:
    asset: CryptoAsset
    vulnerability_score: float
    timeline_years: float
    threat_level: ThreatLevel
    migration_priority: int
    estimated_migration_cost: float
    recommendations: List[str]


class QuantumVulnerabilityAnalyzer:
    QUANTUM_VULNERABLE_ALGORITHMS = {
        CryptoAlgorithm.RSA_2048: {"vulnerability": 0.95, "years_to_break": 5},
        CryptoAlgorithm.RSA_4096: {"vulnerability": 0.85, "years_to_break": 8},
        CryptoAlgorithm.ECC_256: {"vulnerability": 0.90, "years_to_break": 6},
        CryptoAlgorithm.ECC_384: {"vulnerability": 0.80, "years_to_break": 7},
        CryptoAlgorithm.AES_128: {"vulnerability": 0.40, "years_to_break": 15},
        CryptoAlgorithm.AES_256: {"vulnerability": 0.20, "years_to_break": 25},
        CryptoAlgorithm.SHA_256: {"vulnerability": 0.35, "years_to_break": 12},
        CryptoAlgorithm.SHA_3: {"vulnerability": 0.15, "years_to_break": 30},
        CryptoAlgorithm.DES: {"vulnerability": 1.0, "years_to_break": 1},
        CryptoAlgorithm.TRIPLE_DES: {"vulnerability": 0.70, "years_to_break": 3},
    }
    
    SENSITIVITY_MULTIPLIERS = {
        "Critical": 1.5,
        "High": 1.3,
        "Medium": 1.0,
        "Low": 0.7
    }
    
    USAGE_AREA_WEIGHTS = {
        "Core Banking": 1.4,
        "Payment Processing": 1.5,
        "Customer Authentication": 1.3,
        "Internal Communications": 0.9,
        "Data Storage": 1.1,
        "API Security": 1.2,
        "Mobile Banking": 1.3,
        "ATM Network": 1.4
    }
    
    def __init__(self, quantum_advancement_factor: float = 1.0):
        self.quantum_advancement_factor = quantum_advancement_factor
    
    def calculate_vulnerability_score(self, asset: CryptoAsset) -> float:
        base_vulnerability = self.QUANTUM_VULNERABLE_ALGORITHMS.get(
            asset.algorithm, {"vulnerability": 0.5}
        )["vulnerability"]
        
        sensitivity_mult = self.SENSITIVITY_MULTIPLIERS.get(asset.data_sensitivity, 1.0)
        usage_weight = self.USAGE_AREA_WEIGHTS.get(asset.usage_area, 1.0)
        
        volume_factor = min(1 + (asset.estimated_data_volume_gb / 1000) * 0.1, 1.5)
        
        score = base_vulnerability * sensitivity_mult * usage_weight * volume_factor
        score *= self.quantum_advancement_factor
        
        return min(score, 1.0)
    
    def estimate_threat_timeline(self, asset: CryptoAsset) -> float:
        base_years = self.QUANTUM_VULNERABLE_ALGORITHMS.get(
            asset.algorithm, {"years_to_break": 10}
        )["years_to_break"]
        
        adjusted_years = base_years / self.quantum_advancement_factor
        
        return max(adjusted_years, 1.0)
    
    def classify_threat_level(self, vulnerability_score: float, timeline_years: float) -> ThreatLevel:
        combined_score = vulnerability_score * (10 / timeline_years)
        
        if combined_score >= 1.5:
            return ThreatLevel.CRITICAL
        elif combined_score >= 1.0:
            return ThreatLevel.HIGH
        elif combined_score >= 0.6:
            return ThreatLevel.MEDIUM
        elif combined_score >= 0.3:
            return ThreatLevel.LOW
        else:
            return ThreatLevel.MINIMAL
    
    def calculate_migration_priority(self, threat_level: ThreatLevel, 
                                      data_sensitivity: str, usage_area: str) -> int:
        base_priority = threat_level.value * 20
        sensitivity_bonus = {"Critical": 20, "High": 15, "Medium": 10, "Low": 5}.get(data_sensitivity, 0)
        usage_bonus = self.USAGE_AREA_WEIGHTS.get(usage_area, 1.0) * 10
        
        return min(int(base_priority + sensitivity_bonus + usage_bonus), 100)
    
    def estimate_migration_cost(self, asset: CryptoAsset, threat_level: ThreatLevel) -> float:
        base_cost = {
            "Core Banking": 500000,
            "Payment Processing": 750000,
            "Customer Authentication": 300000,
            "Internal Communications": 100000,
            "Data Storage": 400000,
            "API Security": 250000,
            "Mobile Banking": 350000,
            "ATM Network": 600000
        }.get(asset.usage_area, 200000)
        
        complexity_factor = {
            ThreatLevel.CRITICAL: 1.5,
            ThreatLevel.HIGH: 1.3,
            ThreatLevel.MEDIUM: 1.1,
            ThreatLevel.LOW: 1.0,
            ThreatLevel.MINIMAL: 0.9
        }.get(threat_level, 1.0)
        
        volume_factor = 1 + (asset.estimated_data_volume_gb / 10000) * 0.2
        
        return base_cost * complexity_factor * volume_factor
    
    def generate_recommendations(self, asset: CryptoAsset, 
                                  threat_level: ThreatLevel) -> List[str]:
        recommendations = []
        
        if asset.algorithm in [CryptoAlgorithm.RSA_2048, CryptoAlgorithm.RSA_4096]:
            recommendations.append("Migrate to post-quantum algorithms (CRYSTALS-Kyber, CRYSTALS-Dilithium)")
            recommendations.append("Implement hybrid encryption combining classical and PQC")
        
        if asset.algorithm in [CryptoAlgorithm.ECC_256, CryptoAlgorithm.ECC_384]:
            recommendations.append("Transition to lattice-based cryptography")
            recommendations.append("Consider SPHINCS+ for digital signatures")
        
        if asset.algorithm in [CryptoAlgorithm.DES, CryptoAlgorithm.TRIPLE_DES]:
            recommendations.append("IMMEDIATE: Replace with AES-256 as interim measure")
            recommendations.append("Plan for quantum-safe symmetric encryption")
        
        if threat_level in [ThreatLevel.CRITICAL, ThreatLevel.HIGH]:
            recommendations.append("Initiate emergency quantum readiness program")
            recommendations.append("Conduct comprehensive cryptographic inventory")
            recommendations.append("Establish quantum-safe key management infrastructure")
        
        if asset.data_sensitivity == "Critical":
            recommendations.append("Implement crypto-agility framework for rapid algorithm updates")
            recommendations.append("Consider quantum key distribution (QKD) for highest-value data")
        
        recommendations.append("Regular security audits and penetration testing")
        recommendations.append("Staff training on quantum computing threats")
        
        return recommendations
    
    def analyze_asset(self, asset: CryptoAsset) -> RiskAssessment:
        vulnerability_score = self.calculate_vulnerability_score(asset)
        timeline_years = self.estimate_threat_timeline(asset)
        threat_level = self.classify_threat_level(vulnerability_score, timeline_years)
        migration_priority = self.calculate_migration_priority(
            threat_level, asset.data_sensitivity, asset.usage_area
        )
        migration_cost = self.estimate_migration_cost(asset, threat_level)
        recommendations = self.generate_recommendations(asset, threat_level)
        
        return RiskAssessment(
            asset=asset,
            vulnerability_score=vulnerability_score,
            timeline_years=timeline_years,
            threat_level=threat_level,
            migration_priority=migration_priority,
            estimated_migration_cost=migration_cost,
            recommendations=recommendations
        )


class BankCryptoInventory:
    def __init__(self):
        self.assets: List[CryptoAsset] = []
    
    def add_asset(self, asset: CryptoAsset):
        self.assets.append(asset)
    
    def get_sample_bank_inventory(self) -> List[CryptoAsset]:
        return [
            CryptoAsset("Core Banking TLS", CryptoAlgorithm.RSA_2048, 2048, 
                       "Core Banking", "Critical", 5000),
            CryptoAsset("Payment Gateway", CryptoAlgorithm.RSA_4096, 4096,
                       "Payment Processing", "Critical", 2000),
            CryptoAsset("Customer Auth Keys", CryptoAlgorithm.ECC_256, 256,
                       "Customer Authentication", "High", 500),
            CryptoAsset("Mobile App Signing", CryptoAlgorithm.ECC_384, 384,
                       "Mobile Banking", "High", 100),
            CryptoAsset("Data-at-Rest", CryptoAlgorithm.AES_256, 256,
                       "Data Storage", "Critical", 50000),
            CryptoAsset("API Gateway", CryptoAlgorithm.RSA_2048, 2048,
                       "API Security", "Medium", 300),
            CryptoAsset("ATM Communication", CryptoAlgorithm.TRIPLE_DES, 168,
                       "ATM Network", "High", 150),
            CryptoAsset("Internal Email", CryptoAlgorithm.RSA_2048, 2048,
                       "Internal Communications", "Low", 200),
            CryptoAsset("Database Encryption", CryptoAlgorithm.AES_128, 128,
                       "Data Storage", "High", 15000),
            CryptoAsset("Digital Signatures", CryptoAlgorithm.SHA_256, 256,
                       "Core Banking", "Critical", 1000),
        ]


def generate_risk_report(assets: List[CryptoAsset], 
                         advancement_factor: float = 1.0) -> pd.DataFrame:
    analyzer = QuantumVulnerabilityAnalyzer(advancement_factor)
    assessments = [analyzer.analyze_asset(asset) for asset in assets]
    
    data = []
    for assessment in assessments:
        data.append({
            "Asset Name": assessment.asset.name,
            "Algorithm": assessment.asset.algorithm.value,
            "Usage Area": assessment.asset.usage_area,
            "Data Sensitivity": assessment.asset.data_sensitivity,
            "Data Volume (GB)": assessment.asset.estimated_data_volume_gb,
            "Vulnerability Score": round(assessment.vulnerability_score * 100, 1),
            "Years to Threat": round(assessment.timeline_years, 1),
            "Threat Level": assessment.threat_level.name,
            "Migration Priority": assessment.migration_priority,
            "Est. Migration Cost ($)": round(assessment.estimated_migration_cost, 0),
            "Top Recommendation": assessment.recommendations[0] if assessment.recommendations else "N/A"
        })
    
    return pd.DataFrame(data)
