"""持久化层：保存调研历史和公司关系图"""
import json
import networkx as nx
from pathlib import Path
from datetime import datetime
from src.schemas import Report


class Persistence:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.reports_dir = self.data_dir / "reports"
        self.reports_dir.mkdir(exist_ok=True)

    def save_report(self, report: Report) -> str:
        """保存报告到 JSON"""
        filename = f"{report.company_code}_{report.date}.json"
        filepath = self.reports_dir / filename

        data = {
            "company_code": report.company_code,
            "company_name": report.company_name,
            "date": report.date,
            "chapters": {
                "ch1": report.ch1_overview,
                "ch2": report.ch2_industry,
                "ch3": report.ch3_moat,
                "ch4": report.ch4_risk,
                "ch5": report.ch5_finance,
                "ch6": report.ch6_leader,
                "ch7": report.ch7_position,
                "ch8": report.ch8_summary,
            },
            "warnings": report.consistency_warnings,
        }

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return str(filepath)
        except Exception as e:
            print(f"保存报告失败: {e}")
            return ""

    def load_report(self, company_code: str, date: str = None) -> dict | None:
        """加载报告"""
        if date:
            filename = f"{company_code}_{date}.json"
        else:
            # 加载最新报告
            files = list(self.reports_dir.glob(f"{company_code}_*.json"))
            if not files:
                return None
            filename = sorted(files)[-1].name

        filepath = self.reports_dir / filename
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"加载报告失败: {e}")
            return None

    def save_graph(self, graph: nx.DiGraph) -> bool:
        """保存公司关系图"""
        filepath = self.data_dir / "company_graph.json"
        try:
            data = nx.node_link_data(graph)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存图失败: {e}")
            return False

    def load_graph(self) -> nx.DiGraph:
        """加载公司关系图"""
        filepath = self.data_dir / "company_graph.json"
        if not filepath.exists():
            return nx.DiGraph()
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return nx.node_link_graph(data)
        except Exception as e:
            print(f"加载图失败: {e}")
            return nx.DiGraph()
