import pytest
import networkx as nx
from src.state.persistence import Persistence
from src.schemas import Report


def test_save_and_load_report(tmp_path):
    """测试报告保存和加载"""
    persistence = Persistence(data_dir=str(tmp_path))

    report = Report(
        company_code="000001",
        company_name="测试公司",
        date="2026-03-23",
        ch1_overview="概述",
        ch2_industry="行业",
        ch3_moat="护城河",
        ch4_risk="风险",
        ch5_finance="财务",
        ch6_leader="人物",
        ch7_position="建仓",
        ch8_summary="总结",
        consistency_warnings=[]
    )

    # 保存
    filepath = persistence.save_report(report)
    assert filepath != ""

    # 加载
    loaded = persistence.load_report("000001", "2026-03-23")
    assert loaded is not None
    assert loaded["company_name"] == "测试公司"


def test_save_and_load_graph(tmp_path):
    """测试图保存和加载"""
    persistence = Persistence(data_dir=str(tmp_path))

    # 创建图
    graph = nx.DiGraph()
    graph.add_node("公司A", type="company")
    graph.add_node("公司B", type="company")
    graph.add_edge("公司A", "公司B", relation="竞争")

    # 保存
    assert persistence.save_graph(graph) is True

    # 加载
    loaded_graph = persistence.load_graph()
    assert loaded_graph.number_of_nodes() == 2
    assert loaded_graph.has_edge("公司A", "公司B")
