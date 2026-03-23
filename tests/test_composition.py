import pytest
from src.agents.composition import ReportAssembler, ConsistencyChecker
from src.schemas import Report, RiskTrustJudgment, InvestmentJudgment


@pytest.mark.asyncio
async def test_report_assembler_basic():
    """测试基础报告组装"""
    assembler = ReportAssembler(agent_id="test_assembler")

    input_data = {
        "company_name": "测试公司",
        "company_code": "000001",
        "industry_analysis": {
            "policy_environment": "政策友好",
            "industry_cycle": "成长期",
            "supply_demand": "供不应求",
            "competitive_landscape": "竞争激烈"
        },
        "moat_analysis": {
            "moat_summary": "品牌护城河强",
            "ten_year_moat": "可持续"
        },
        "risk_analysis": {
            "risk_summary": "风险可控"
        },
        "finance_analysis": {
            "finance_summary": "财务健康"
        },
        "leader_analysis": {
            "leader_profile": "经验丰富"
        }
    }

    report = await assembler.execute(input_data)

    assert isinstance(report, Report)
    assert report.company_name == "测试公司"
    assert "第二章" in report.ch2_industry
    assert "政策友好" in report.ch2_industry


@pytest.mark.asyncio
async def test_report_with_debate_results():
    """测试包含辩论结果的报告组装"""
    assembler = ReportAssembler(agent_id="test_assembler")

    round1 = RiskTrustJudgment(
        risk_verdict="可控",
        risk_reasoning="风险在可控范围内",
        trust_verdict="值得信任",
        trust_reasoning="董事长诚信记录良好",
        evidence_references=[]
    )

    round2 = InvestmentJudgment(
        decision="买入",
        confidence=0.75,
        risk_trust_input=round1,
        bull_case="增长强劲",
        bear_case="估值偏高",
        key_factors=["护城河", "财务"],
        evidence_references=[],
        position_suggestion="分批建仓"
    )

    input_data = {
        "company_name": "测试公司",
        "risk_analysis": {"risk_summary": "风险可控"},
        "leader_analysis": {"leader_profile": "经验丰富"},
        "round1_judgment": round1,
        "round2_judgment": round2
    }

    report = await assembler.execute(input_data)

    assert "可控" in report.ch4_risk
    assert "值得信任" in report.ch6_leader
    assert "买入" in report.ch7_position
    assert "0.75" in report.ch7_position or "75%" in report.ch7_position


@pytest.mark.asyncio
async def test_consistency_checker_detects_contradiction():
    """测试一致性检查器检测矛盾"""
    checker = ConsistencyChecker(agent_id="test_checker")

    report = Report(
        company_code="000001",
        company_name="测试公司",
        date="2026-03-23",
        ch1_overview="概述",
        ch2_industry="行业",
        ch3_moat="护城河",
        ch4_risk="风险判定: 严重",
        ch5_finance="财务",
        ch6_leader="信任判定: 值得信任",
        ch7_position="决策: 买入",
        ch8_summary="总结",
        consistency_warnings=[]
    )

    warnings = await checker.execute({"report": report})

    assert len(warnings) > 0
    assert any("严重风险" in w for w in warnings)


@pytest.mark.asyncio
async def test_consistency_checker_no_warning():
    """测试一致性检查器无警告"""
    checker = ConsistencyChecker(agent_id="test_checker")

    report = Report(
        company_code="000001",
        company_name="测试公司",
        date="2026-03-23",
        ch1_overview="概述",
        ch2_industry="行业",
        ch3_moat="护城河",
        ch4_risk="风险判定: 可控",
        ch5_finance="财务",
        ch6_leader="信任判定: 值得信任",
        ch7_position="决策: 买入",
        ch8_summary="总结",
        consistency_warnings=[]
    )

    warnings = await checker.execute({"report": report})

    assert len(warnings) == 0
