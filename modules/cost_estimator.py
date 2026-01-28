import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class MigrationPhase(Enum):
    ASSESSMENT = "Assessment & Planning"
    PILOT = "Pilot Implementation"
    MIGRATION = "Full Migration"
    VALIDATION = "Testing & Validation"
    DEPLOYMENT = "Production Deployment"
    MONITORING = "Ongoing Monitoring"


@dataclass
class CostComponent:
    category: str
    description: str
    base_cost: float
    variable_cost_per_system: float
    timeline_months: int


@dataclass
class MigrationCostEstimate:
    total_cost: float
    cost_breakdown: Dict[str, float]
    timeline_months: int
    risk_contingency: float
    roi_years: float
    annual_savings: float


class QuantumMigrationCostEstimator:
    COST_COMPONENTS = {
        MigrationPhase.ASSESSMENT: CostComponent(
            "Assessment", "Cryptographic inventory and risk assessment",
            150000, 5000, 3
        ),
        MigrationPhase.PILOT: CostComponent(
            "Pilot", "Proof of concept and pilot implementation",
            300000, 15000, 6
        ),
        MigrationPhase.MIGRATION: CostComponent(
            "Migration", "Full system migration to PQC",
            500000, 25000, 12
        ),
        MigrationPhase.VALIDATION: CostComponent(
            "Validation", "Security testing and compliance validation",
            200000, 8000, 4
        ),
        MigrationPhase.DEPLOYMENT: CostComponent(
            "Deployment", "Production rollout and cutover",
            250000, 12000, 3
        ),
        MigrationPhase.MONITORING: CostComponent(
            "Monitoring", "Ongoing monitoring and maintenance (annual)",
            100000, 3000, 12
        ),
    }
    
    ALGORITHM_MIGRATION_COSTS = {
        "RSA-2048": 75000,
        "RSA-4096": 85000,
        "ECC-256": 65000,
        "ECC-384": 70000,
        "AES-128": 40000,
        "AES-256": 35000,
        "SHA-256": 30000,
        "SHA-3": 25000,
        "DES": 90000,
        "3DES": 80000,
    }
    
    USAGE_AREA_COMPLEXITY = {
        "Core Banking": 2.0,
        "Payment Processing": 2.2,
        "Customer Authentication": 1.5,
        "Internal Communications": 0.8,
        "Data Storage": 1.3,
        "API Security": 1.2,
        "Mobile Banking": 1.4,
        "ATM Network": 1.8
    }
    
    BANK_SIZE_MULTIPLIERS = {
        "Small": {"systems": 50, "multiplier": 0.5},
        "Medium": {"systems": 200, "multiplier": 0.8},
        "Large": {"systems": 500, "multiplier": 1.0},
        "Enterprise": {"systems": 2000, "multiplier": 1.5}
    }
    
    def __init__(self, bank_size: str = "Large", 
                 num_systems: int = None,
                 risk_tolerance: str = "Medium"):
        self.bank_size = bank_size
        size_config = self.BANK_SIZE_MULTIPLIERS.get(bank_size, self.BANK_SIZE_MULTIPLIERS["Large"])
        self.num_systems = num_systems or size_config["systems"]
        self.size_multiplier = size_config["multiplier"]
        self.risk_contingency_rate = {
            "Low": 0.15,
            "Medium": 0.25,
            "High": 0.35
        }.get(risk_tolerance, 0.25)
    
    def calculate_phase_cost(self, phase: MigrationPhase) -> float:
        component = self.COST_COMPONENTS[phase]
        base = component.base_cost * self.size_multiplier
        variable = component.variable_cost_per_system * self.num_systems
        return base + variable
    
    def calculate_algorithm_migration_cost(self, algorithms: List[str]) -> float:
        total = 0
        for algo in algorithms:
            base_cost = self.ALGORITHM_MIGRATION_COSTS.get(algo, 50000)
            total += base_cost * self.size_multiplier
        return total
    
    def calculate_total_migration_cost(self, 
                                        algorithms: List[str] = None,
                                        usage_areas: List[str] = None) -> MigrationCostEstimate:
        if algorithms is None:
            algorithms = ["RSA-2048", "ECC-256", "AES-256"]
        if usage_areas is None:
            usage_areas = ["Core Banking", "Payment Processing", "Customer Authentication"]
        
        cost_breakdown = {}
        total_timeline = 0
        
        for phase in MigrationPhase:
            phase_cost = self.calculate_phase_cost(phase)
            cost_breakdown[phase.value] = phase_cost
            if phase != MigrationPhase.MONITORING:
                total_timeline += self.COST_COMPONENTS[phase].timeline_months
        
        algo_cost = self.calculate_algorithm_migration_cost(algorithms)
        cost_breakdown["Algorithm-Specific Migration"] = algo_cost
        
        complexity_factor = sum(
            self.USAGE_AREA_COMPLEXITY.get(area, 1.0) 
            for area in usage_areas
        ) / len(usage_areas) if usage_areas else 1.0
        
        for key in cost_breakdown:
            cost_breakdown[key] *= complexity_factor
        
        subtotal = sum(cost_breakdown.values())
        
        risk_contingency = subtotal * self.risk_contingency_rate
        cost_breakdown["Risk Contingency"] = risk_contingency
        
        total_cost = subtotal + risk_contingency
        
        annual_risk_cost = self._estimate_annual_risk_cost()
        roi_years = total_cost / annual_risk_cost if annual_risk_cost > 0 else 10
        
        return MigrationCostEstimate(
            total_cost=total_cost,
            cost_breakdown=cost_breakdown,
            timeline_months=total_timeline,
            risk_contingency=risk_contingency,
            roi_years=roi_years,
            annual_savings=annual_risk_cost
        )
    
    def _estimate_annual_risk_cost(self) -> float:
        base_risk_cost = 1000000
        
        size_factor = self.BANK_SIZE_MULTIPLIERS.get(
            self.bank_size, {"multiplier": 1.0}
        )["multiplier"]
        
        probability_factor = 0.15
        
        return base_risk_cost * size_factor * probability_factor * (1 + self.num_systems / 1000)
    
    def generate_cost_timeline(self) -> pd.DataFrame:
        timeline_data = []
        cumulative_months = 0
        cumulative_cost = 0
        
        for phase in MigrationPhase:
            if phase == MigrationPhase.MONITORING:
                continue
                
            phase_cost = self.calculate_phase_cost(phase)
            component = self.COST_COMPONENTS[phase]
            
            cumulative_cost += phase_cost
            start_month = cumulative_months + 1
            end_month = cumulative_months + component.timeline_months
            cumulative_months = end_month
            
            timeline_data.append({
                "Phase": phase.value,
                "Start Month": start_month,
                "End Month": end_month,
                "Duration (Months)": component.timeline_months,
                "Phase Cost ($)": phase_cost,
                "Cumulative Cost ($)": cumulative_cost
            })
        
        return pd.DataFrame(timeline_data)
    
    def generate_roi_analysis(self, estimate: MigrationCostEstimate) -> pd.DataFrame:
        years = 10
        data = []
        cumulative_savings = 0
        
        for year in range(1, years + 1):
            annual_savings = estimate.annual_savings * (1.05 ** (year - 1))
            cumulative_savings += annual_savings
            net_benefit = cumulative_savings - estimate.total_cost
            roi_percent = (net_benefit / estimate.total_cost) * 100 if estimate.total_cost > 0 else 0
            
            data.append({
                "Year": year,
                "Annual Risk Savings ($)": annual_savings,
                "Cumulative Savings ($)": cumulative_savings,
                "Net Benefit ($)": net_benefit,
                "ROI (%)": roi_percent
            })
        
        return pd.DataFrame(data)
    
    def compare_scenarios(self) -> pd.DataFrame:
        scenarios = [
            ("Aggressive (2-year)", 0.7, "High"),
            ("Standard (3-year)", 1.0, "Medium"),
            ("Conservative (5-year)", 1.5, "Low")
        ]
        
        data = []
        for name, timeline_factor, risk in scenarios:
            original_tolerance = self.risk_contingency_rate
            self.risk_contingency_rate = {"Low": 0.15, "Medium": 0.25, "High": 0.35}[risk]
            
            estimate = self.calculate_total_migration_cost()
            adjusted_cost = estimate.total_cost * timeline_factor
            timeline = int(estimate.timeline_months * timeline_factor)
            
            data.append({
                "Scenario": name,
                "Total Cost ($)": adjusted_cost,
                "Timeline (Months)": timeline,
                "Risk Level": risk,
                "ROI (Years)": estimate.roi_years * timeline_factor
            })
            
            self.risk_contingency_rate = original_tolerance
        
        return pd.DataFrame(data)
