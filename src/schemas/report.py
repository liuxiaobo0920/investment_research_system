from dataclasses import dataclass


@dataclass
class Report:
    """完整调研报告（8章节）"""
    company_code: str
    company_name: str
    date: str

    ch1_overview: str
    ch2_industry: str
    ch3_moat: str
    ch4_risk: str
    ch5_finance: str
    ch6_leader: str
    ch7_position: str
    ch8_summary: str

    consistency_warnings: list[str]
