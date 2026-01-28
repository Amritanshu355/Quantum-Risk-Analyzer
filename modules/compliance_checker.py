import pandas as pd
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class RegulatoryBody(Enum):
    NIST = "NIST"
    PCI_DSS = "PCI-DSS"
    GDPR = "GDPR"
    SOX = "SOX"
    BASEL_III = "Basel III"
    FFIEC = "FFIEC"
    ISO_27001 = "ISO 27001"
    SWIFT_CSP = "SWIFT CSP"


@dataclass
class ComplianceRequirement:
    regulation: RegulatoryBody
    requirement_id: str
    description: str
    quantum_relevance: str
    deadline: str
    penalty_range: str


@dataclass
class ComplianceStatus:
    requirement: ComplianceRequirement
    current_status: str
    gap_analysis: str
    remediation_steps: List[str]
    estimated_effort_days: int
    risk_if_non_compliant: str


class QuantumComplianceChecker:
    QUANTUM_COMPLIANCE_REQUIREMENTS = [
        ComplianceRequirement(
            RegulatoryBody.NIST,
            "NIST-PQC-2024",
            "Post-Quantum Cryptography Standards Adoption",
            "Direct - Mandates transition to quantum-resistant algorithms",
            "2025-2030 (phased)",
            "Federal contract ineligibility"
        ),
        ComplianceRequirement(
            RegulatoryBody.PCI_DSS,
            "PCI-DSS-4.0-3.4",
            "Strong Cryptography for Cardholder Data",
            "High - Future versions will require quantum-safe encryption",
            "2024 (current), 2026+ (quantum)",
            "$5,000 - $100,000/month"
        ),
        ComplianceRequirement(
            RegulatoryBody.GDPR,
            "GDPR-Art-32",
            "Security of Processing",
            "Medium - State-of-art security includes quantum considerations",
            "Ongoing",
            "Up to 4% annual turnover"
        ),
        ComplianceRequirement(
            RegulatoryBody.SOX,
            "SOX-302/404",
            "Internal Controls Over Financial Reporting",
            "Medium - Cryptographic controls part of IT general controls",
            "Annual certification",
            "Criminal penalties, delisting"
        ),
        ComplianceRequirement(
            RegulatoryBody.BASEL_III,
            "Basel-III-OpRisk",
            "Operational Risk Management",
            "High - Quantum threats as emerging operational risk",
            "Ongoing",
            "Capital adequacy penalties"
        ),
        ComplianceRequirement(
            RegulatoryBody.FFIEC,
            "FFIEC-CAT",
            "Cybersecurity Assessment Tool",
            "High - Crypto agility becoming assessment criteria",
            "Ongoing examination",
            "Supervisory action"
        ),
        ComplianceRequirement(
            RegulatoryBody.ISO_27001,
            "ISO-27001-A.10",
            "Cryptographic Controls",
            "High - Algorithm selection and key management",
            "Ongoing certification",
            "Certification loss"
        ),
        ComplianceRequirement(
            RegulatoryBody.SWIFT_CSP,
            "SWIFT-CSP-2.0",
            "Customer Security Programme",
            "High - Transaction security and message integrity",
            "Annual attestation",
            "Network disconnection"
        ),
    ]
    
    COMPLIANCE_STATUS_LEVELS = {
        "Compliant": 100,
        "Partially Compliant": 70,
        "In Progress": 50,
        "Planning": 30,
        "Non-Compliant": 0
    }
    
    def __init__(self, bank_size: str = "Large", quantum_readiness_level: str = "Low"):
        self.bank_size = bank_size
        self.quantum_readiness_level = quantum_readiness_level
        self.readiness_scores = {
            "High": 0.8,
            "Medium": 0.5,
            "Low": 0.2,
            "None": 0.0
        }
    
    def assess_requirement(self, requirement: ComplianceRequirement) -> ComplianceStatus:
        readiness_score = self.readiness_scores.get(self.quantum_readiness_level, 0.2)
        
        status_thresholds = [
            (0.8, "Compliant"),
            (0.6, "Partially Compliant"),
            (0.4, "In Progress"),
            (0.2, "Planning"),
            (0.0, "Non-Compliant")
        ]
        
        current_status = "Non-Compliant"
        for threshold, status in status_thresholds:
            if readiness_score >= threshold:
                current_status = status
                break
        
        gap_analysis = self._generate_gap_analysis(requirement, current_status)
        remediation_steps = self._generate_remediation_steps(requirement, current_status)
        effort_days = self._estimate_effort(requirement, current_status)
        risk = self._assess_non_compliance_risk(requirement)
        
        return ComplianceStatus(
            requirement=requirement,
            current_status=current_status,
            gap_analysis=gap_analysis,
            remediation_steps=remediation_steps,
            estimated_effort_days=effort_days,
            risk_if_non_compliant=risk
        )
    
    def _generate_gap_analysis(self, req: ComplianceRequirement, status: str) -> str:
        if status == "Compliant":
            return "No significant gaps identified. Maintain current controls and monitor for updates."
        elif status == "Partially Compliant":
            return f"Partial implementation of {req.description}. Key gaps in quantum-specific controls."
        elif status == "In Progress":
            return f"Active remediation underway for {req.requirement_id}. Timeline adherence critical."
        elif status == "Planning":
            return f"Planning phase for {req.description}. Detailed roadmap required."
        else:
            return f"Significant gaps in meeting {req.requirement_id}. Immediate action required."
    
    def _generate_remediation_steps(self, req: ComplianceRequirement, status: str) -> List[str]:
        base_steps = [
            f"Conduct detailed assessment against {req.requirement_id} requirements",
            "Document current cryptographic inventory",
            "Identify quantum-vulnerable systems",
        ]
        
        if status in ["Non-Compliant", "Planning"]:
            base_steps.extend([
                "Develop quantum migration roadmap",
                "Allocate budget for compliance program",
                "Engage external auditors for gap assessment",
                "Establish governance committee for oversight"
            ])
        elif status in ["In Progress", "Partially Compliant"]:
            base_steps.extend([
                "Accelerate current migration activities",
                "Conduct internal audit of progress",
                "Document evidence of compliance efforts"
            ])
        
        base_steps.append("Implement continuous monitoring and reporting")
        
        return base_steps
    
    def _estimate_effort(self, req: ComplianceRequirement, status: str) -> int:
        base_effort = {
            RegulatoryBody.NIST: 180,
            RegulatoryBody.PCI_DSS: 120,
            RegulatoryBody.GDPR: 90,
            RegulatoryBody.SOX: 60,
            RegulatoryBody.BASEL_III: 150,
            RegulatoryBody.FFIEC: 100,
            RegulatoryBody.ISO_27001: 80,
            RegulatoryBody.SWIFT_CSP: 70
        }.get(req.regulation, 90)
        
        status_multipliers = {
            "Compliant": 0.1,
            "Partially Compliant": 0.4,
            "In Progress": 0.6,
            "Planning": 0.8,
            "Non-Compliant": 1.0
        }
        
        size_multipliers = {
            "Small": 0.5,
            "Medium": 0.75,
            "Large": 1.0,
            "Enterprise": 1.5
        }
        
        return int(base_effort * 
                   status_multipliers.get(status, 1.0) * 
                   size_multipliers.get(self.bank_size, 1.0))
    
    def _assess_non_compliance_risk(self, req: ComplianceRequirement) -> str:
        high_risk_bodies = [RegulatoryBody.PCI_DSS, RegulatoryBody.GDPR, 
                           RegulatoryBody.SWIFT_CSP, RegulatoryBody.SOX]
        
        if req.regulation in high_risk_bodies:
            return f"HIGH - {req.penalty_range}"
        else:
            return f"MEDIUM - {req.penalty_range}"
    
    def generate_compliance_report(self) -> pd.DataFrame:
        statuses = [self.assess_requirement(req) for req in self.QUANTUM_COMPLIANCE_REQUIREMENTS]
        
        data = []
        for status in statuses:
            data.append({
                "Regulation": status.requirement.regulation.value,
                "Requirement ID": status.requirement.requirement_id,
                "Description": status.requirement.description,
                "Quantum Relevance": status.requirement.quantum_relevance,
                "Deadline": status.requirement.deadline,
                "Current Status": status.current_status,
                "Gap Analysis": status.gap_analysis,
                "Effort (Days)": status.estimated_effort_days,
                "Risk Level": status.risk_if_non_compliant
            })
        
        return pd.DataFrame(data)
    
    def calculate_overall_compliance_score(self) -> float:
        statuses = [self.assess_requirement(req) for req in self.QUANTUM_COMPLIANCE_REQUIREMENTS]
        
        total_score = sum(
            self.COMPLIANCE_STATUS_LEVELS.get(s.current_status, 0) 
            for s in statuses
        )
        
        return total_score / len(statuses)
    
    def get_priority_actions(self) -> List[Dict]:
        statuses = [self.assess_requirement(req) for req in self.QUANTUM_COMPLIANCE_REQUIREMENTS]
        
        priority_actions = []
        for status in statuses:
            if status.current_status in ["Non-Compliant", "Planning"]:
                priority_actions.append({
                    "Regulation": status.requirement.regulation.value,
                    "Action": status.remediation_steps[0] if status.remediation_steps else "Review requirements",
                    "Effort": status.estimated_effort_days,
                    "Risk": status.risk_if_non_compliant
                })
        
        return sorted(priority_actions, key=lambda x: x["Effort"], reverse=True)
