"""
AI-Powered Recommendation Engine for Quantum Risk Analyzer
Provides intelligent, context-aware recommendations for cryptographic migration
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class RecommendationPriority(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class AIRecommendation:
    asset_name: str
    priority: RecommendationPriority
    category: str
    title: str
    description: str
    actions: List[str]
    estimated_effort_days: int
    risk_if_ignored: str


class AIRecommendationEngine:
    """
    AI-powered recommendation engine that analyzes risk data
    and generates prioritized, actionable recommendations
    """

    # PQC (Post-Quantum Cryptography) migration mappings
    PQC_MIGRATIONS = {
        "RSA-2048": {
            "replacement": "CRYSTALS-Kyber (ML-KEM) for key exchange + CRYSTALS-Dilithium (ML-DSA) for signatures",
            "timeline": "12-18 months",
            "complexity": "High"
        },
        "RSA-4096": {
            "replacement": "CRYSTALS-Kyber (ML-KEM) with larger key sizes",
            "timeline": "12-18 months",
            "complexity": "High"
        },
        "ECC-256": {
            "replacement": "CRYSTALS-Dilithium or SPHINCS+ for signatures",
            "timeline": "12-18 months",
            "complexity": "Medium"
        },
        "ECC-384": {
            "replacement": "CRYSTALS-Dilithium Level 3 or Level 5",
            "timeline": "12-18 months",
            "complexity": "Medium"
        },
        "AES-128": {
            "replacement": "Upgrade to AES-256 (quantum-safe symmetric)",
            "timeline": "6-12 months",
            "complexity": "Low"
        },
        "AES-256": {
            "replacement": "Already quantum-resistant, maintain current implementation",
            "timeline": "N/A",
            "complexity": "None"
        },
        "SHA-256": {
            "replacement": "SHA-384 or SHA-512 for long-term security",
            "timeline": "6-12 months",
            "complexity": "Low"
        },
        "SHA-3": {
            "replacement": "Already quantum-resistant, maintain current implementation",
            "timeline": "N/A",
            "complexity": "None"
        },
        "DES": {
            "replacement": "IMMEDIATE: AES-256 (DES is broken even classically)",
            "timeline": "IMMEDIATE (0-3 months)",
            "complexity": "Critical"
        },
        "3DES": {
            "replacement": "AES-256 with proper key management",
            "timeline": "0-6 months",
            "complexity": "Medium"
        }
    }

    # Industry-specific compliance requirements
    COMPLIANCE_REQUIREMENTS = {
        "Core Banking": ["FFIEC", "SOX", "PCI-DSS", "NIST SP 800-208"],
        "Payment Processing": ["PCI-DSS", "SWIFT CSP", "NIST SP 800-208"],
        "Customer Authentication": ["NIST SP 800-63B", "PCI-DSS", "GDPR"],
        "Data Storage": ["GDPR", "SOX", "NIST SP 800-208"],
        "API Security": ["NIST SP 800-208", "OWASP", "PCI-DSS"],
        "Mobile Banking": ["PCI-DSS", "GDPR", "NIST SP 800-208"],
        "ATM Network": ["PCI-SSC", "NIST SP 800-208", "FFIEC"],
        "Internal Communications": ["SOX", "GDPR", "ISO 27001"]
    }

    def __init__(self, risk_data: pd.DataFrame, bank_size: str = "Medium"):
        self.risk_data = risk_data
        self.bank_size = bank_size
        self.recommendations: List[AIRecommendation] = []

    def analyze_and_generate_recommendations(self) -> List[AIRecommendation]:
        """
        Main method to analyze risk data and generate all recommendations
        """
        self.recommendations = []

        # Generate recommendations for each asset
        for _, row in self.risk_data.iterrows():
            rec = self._generate_asset_recommendation(row)
            if rec:
                self.recommendations.append(rec)

        # Add strategic recommendations
        self._add_strategic_recommendations()

        # Sort by priority
        priority_order = {
            RecommendationPriority.CRITICAL: 0,
            RecommendationPriority.HIGH: 1,
            RecommendationPriority.MEDIUM: 2,
            RecommendationPriority.LOW: 3
        }

        self.recommendations.sort(key=lambda x: priority_order[x.priority])

        return self.recommendations

    def _generate_asset_recommendation(self, row: pd.Series) -> AIRecommendation:
        """Generate recommendation for a single asset"""

        asset_name = row['Asset Name']
        algorithm = row['Algorithm']
        threat_level = row['Threat Level']
        vulnerability = row['Vulnerability Score']
        years_to_threat = row['Years to Threat']
        usage_area = row['Usage Area']
        migration_cost = row['Est. Migration Cost ($)']

        # Determine priority
        if threat_level == 'CRITICAL' or years_to_threat <= 3:
            priority = RecommendationPriority.CRITICAL
        elif threat_level == 'HIGH' or years_to_threat <= 5:
            priority = RecommendationPriority.HIGH
        elif threat_level == 'MEDIUM' or years_to_threat <= 10:
            priority = RecommendationPriority.MEDIUM
        else:
            priority = RecommendationPriority.LOW

        # Get PQC migration info
        pqc_info = self.PQC_MIGRATIONS.get(algorithm, {
            "replacement": "Consult cryptographic expert for migration path",
            "timeline": "TBD",
            "complexity": "Unknown"
        })

        # Generate category
        if priority == RecommendationPriority.CRITICAL:
            category = "Immediate Action Required"
        elif algorithm in ["DES", "3DES"]:
            category = "Legacy Algorithm Replacement"
        elif vulnerability > 80:
            category = "High Vulnerability Mitigation"
        elif years_to_threat < 5:
            category = "Timeline-Driven Migration"
        else:
            category = "Proactive Security Enhancement"

        # Generate actions
        actions = self._generate_actions(row, pqc_info, priority)

        # Estimate effort
        effort = self._estimate_effort(pqc_info, priority)

        # Risk if ignored
        risk_if_ignored = self._calculate_risk_if_ignored(row, priority)

        return AIRecommendation(
            asset_name=asset_name,
            priority=priority,
            category=category,
            title=f"Migrate {algorithm} to Post-Quantum Solution",
            description=f"Replace {algorithm} with {pqc_info['replacement']}. "
                        f"Estimated timeline: {pqc_info['timeline']}. "
                        f"Current vulnerability score: {vulnerability:.1f}%. "
                        f"Quantum threat expected in {years_to_threat:.1f} years.",
            actions=actions,
            estimated_effort_days=effort,
            risk_if_ignored=risk_if_ignored
        )

    def _generate_actions(self, row: pd.Series, pqc_info: Dict,
                          priority: RecommendationPriority) -> List[str]:
        """Generate specific action items for an asset"""

        actions = []

        # Phase 1: Assessment
        actions.append(f"1. Conduct detailed assessment of {row['Asset Name']} cryptographic implementation")

        # Phase 2: Planning
        actions.append(f"2. Design migration architecture using {pqc_info['replacement']}")

        # Phase 3: Testing
        actions.append("3. Set up test environment and validate PQC implementation")

        # Phase 4: Deployment
        if priority == RecommendationPriority.CRITICAL:
            actions.append("4. EMERGENCY: Deploy interim mitigations while full migration is in progress")
            actions.append("5. Execute production migration with rollback plan")
        else:
            actions.append("4. Schedule production migration during maintenance window")

        # Phase 5: Validation
        actions.append("5. Post-migration security validation and compliance verification")

        return actions

    def _estimate_effort(self, pqc_info: Dict, priority: RecommendationPriority) -> int:
        """Estimate effort in days based on complexity and priority"""

        complexity_effort = {
            "Critical": 60,
            "High": 45,
            "Medium": 30,
            "Low": 14,
            "None": 0
        }

        base_effort = complexity_effort.get(pqc_info.get("complexity", "Medium"), 30)

        # Adjust for priority
        if priority == RecommendationPriority.CRITICAL:
            base_effort = int(base_effort * 0.7)  # Faster but more intense

        return base_effort

    def _calculate_risk_if_ignored(self, row: pd.Series,
                                    priority: RecommendationPriority) -> str:
        """Calculate and return risk description if recommendation is ignored"""

        if priority == RecommendationPriority.CRITICAL:
            return ("CRITICAL RISK: Potential exposure of sensitive data to quantum attacks. "
                    "May result in regulatory violations, financial losses, and reputational damage. "
                    "Harvest-now-decrypt-later attacks may already be targeting this asset.")
        elif priority == RecommendationPriority.HIGH:
            return ("HIGH RISK: Significant vulnerability window within 5 years. "
                    "Data encrypted today may be at risk of future decryption. "
                    "Compliance gaps may emerge as regulations evolve.")
        elif priority == RecommendationPriority.MEDIUM:
            return ("MODERATE RISK: Planning window of 5-10 years. "
                    "Proactive migration recommended to avoid future technical debt. "
                    "Early adoption benefits include learning and reduced future costs.")
        else:
            return ("LOW RISK: Long-term monitoring recommended. "
                    "Continue to track quantum computing advancements and PQC standards. "
                    "Reassess annually or when threat timeline changes.")

    def _add_strategic_recommendations(self):
        """Add organization-wide strategic recommendations"""

        # Check for algorithm diversity
        unique_algorithms = self.risk_data['Algorithm'].unique()
        if len(unique_algorithms) < 3:
            self.recommendations.append(AIRecommendation(
                asset_name="Enterprise-wide",
                priority=RecommendationPriority.MEDIUM,
                category="Crypto-Agility",
                title="Implement Crypto-Agility Framework",
                description=f"Current portfolio uses only {len(unique_algorithms)} algorithm types. "
                            "Diversifying cryptographic algorithms reduces single-point-of-failure risk.",
                actions=[
                    "1. Audit all cryptographic dependencies across systems",
                    "2. Design abstraction layer for algorithm swaps",
                    "3. Implement configuration-driven algorithm selection",
                    "4. Create automated cryptographic inventory system"
                ],
                estimated_effort_days=90,
                risk_if_ignored="Lack of crypto-agility will make future migrations slower and more expensive"
            ))

        # Check for high-cost concentration
        total_cost = self.risk_data['Est. Migration Cost ($)'].sum()
        high_cost_assets = self.risk_data[self.risk_data['Est. Migration Cost ($)'] > 500000]
        if len(high_cost_assets) > 2:
            self.recommendations.append(AIRecommendation(
                asset_name="Budget Planning",
                priority=RecommendationPriority.HIGH,
                category="Financial Planning",
                title="Establish Quantum Migration Budget Reserve",
                description=f"Total estimated migration cost: ${total_cost:,.0f}. "
                            f"{len(high_cost_assets)} assets require significant investment (>$500K each).",
                actions=[
                    "1. Create dedicated quantum migration budget line item",
                    "2. Establish multi-year funding commitment",
                    "3. Explore vendor financing and government incentives",
                    "4. Build ROI models for executive approval"
                ],
                estimated_effort_days=30,
                risk_if_ignored="Unfunded mandate may result in delayed migrations and extended vulnerability windows"
            ))

        # Compliance recommendation
        self.recommendations.append(AIRecommendation(
            asset_name="Governance",
            priority=RecommendationPriority.HIGH,
            category="Compliance & Governance",
            title="Establish Quantum Readiness Governance Committee",
            description="Cross-functional team needed to oversee quantum migration across the organization.",
            actions=[
                "1. Appoint executive sponsor (CISO or CTO)",
                "2. Form working group with IT, Security, Compliance, and Business units",
                "3. Define quantum readiness KPIs and reporting cadence",
                "4. Create escalation paths for critical decisions"
            ],
            estimated_effort_days=14,
            risk_if_ignored="Lack of governance leads to fragmented efforts and missed dependencies"
        ))

    def get_top_recommendations(self, n: int = 5) -> List[AIRecommendation]:
        """Get top N recommendations by priority"""
        return self.recommendations[:n]

    def get_recommendations_by_category(self, category: str) -> List[AIRecommendation]:
        """Get recommendations filtered by category"""
        return [r for r in self.recommendations if r.category == category]

    def generate_executive_summary(self) -> str:
        """Generate an executive summary of all recommendations"""

        critical_count = len([r for r in self.recommendations if r.priority == RecommendationPriority.CRITICAL])
        high_count = len([r for r in self.recommendations if r.priority == RecommendationPriority.HIGH])

        total_effort = sum(r.estimated_effort_days for r in self.recommendations)

        summary = f"""
## AI-Generated Quantum Migration Summary

### Key Metrics
- **Total Recommendations**: {len(self.recommendations)}
- **Critical Priority**: {critical_count}
- **High Priority**: {high_count}
- **Estimated Total Effort**: {total_effort} person-days

### Top 3 Immediate Actions
"""

        for i, rec in enumerate(self.recommendations[:3], 1):
            summary += f"\n{i}. **{rec.title}** ({rec.priority.value})"
            summary += f"\n   - Asset: {rec.asset_name}"
            summary += f"\n   - Effort: {rec.estimated_effort_days} days"

        summary += f"""

### Strategic Themes Identified
"""
        categories = set(r.category for r in self.recommendations)
        for cat in categories:
            count = len([r for r in self.recommendations if r.category == cat])
            summary += f"\n- **{cat}**: {count} recommendations"

        return summary.strip()

    def export_to_json(self) -> List[Dict]:
        """Export recommendations as JSON-serializable list"""
        return [
            {
                "asset_name": r.asset_name,
                "priority": r.priority.value,
                "category": r.category,
                "title": r.title,
                "description": r.description,
                "actions": r.actions,
                "estimated_effort_days": r.estimated_effort_days,
                "risk_if_ignored": r.risk_if_ignored
            }
            for r in self.recommendations
        ]
