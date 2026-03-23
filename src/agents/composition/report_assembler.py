from datetime import datetime
from src.agents.base.base_agent import BaseAgent
from src.schemas import Report


class ReportAssembler(BaseAgent):
    """报告组装器：8章节组装"""

    uses_external_data = False

    async def execute(self, input_data: dict) -> Report:
        """组装完整报告"""
        company_name = input_data["company_name"]
        company_code = input_data.get("company_code", "UNKNOWN")

        # 提取各层产出
        industry = input_data.get("industry_analysis", {})
        moat = input_data.get("moat_analysis", {})
        risk = input_data.get("risk_analysis", {})
        finance = input_data.get("finance_analysis", {})
        leader = input_data.get("leader_analysis", {})
        round1 = input_data.get("round1_judgment")
        round2 = input_data.get("round2_judgment")

        # 组装各章节
        ch2 = self._format_industry(industry)
        ch3 = self._format_moat(moat)
        ch4 = self._format_risk(risk, round1)
        ch5 = self._format_finance(finance)
        ch6 = self._format_leader(leader, round1)
        ch7 = self._format_position(round2)

        # 生成概述和总结
        ch1 = await self._generate_overview(company_name, ch2, ch3, ch4, ch5, ch6, ch7, round1, round2)
        ch8 = await self._generate_summary(company_name, ch2, ch3, ch4, ch5, ch6, ch7, round1, round2)

        return Report(
            company_code=company_code,
            company_name=company_name,
            date=datetime.now().strftime("%Y-%m-%d"),
            ch1_overview=ch1,
            ch2_industry=ch2,
            ch3_moat=ch3,
            ch4_risk=ch4,
            ch5_finance=ch5,
            ch6_leader=ch6,
            ch7_position=ch7,
            ch8_summary=ch8,
            consistency_warnings=[],
        )

    def _format_industry(self, analysis) -> str:
        if not analysis:
            return "# 第二章：行业前景与公司地位\n\n数据缺失：行业分析未完成"

        # 支持 dict 和对象
        def get_val(obj, key, default='N/A'):
            return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)

        return f"""# 第二章：行业前景与公司地位

## 政策环境
{get_val(analysis, 'policy_environment')}

## 行业周期
{get_val(analysis, 'industry_cycle')}

## 供需格局
{get_val(analysis, 'supply_demand')}

## 竞争格局
{get_val(analysis, 'competitive_landscape')}
"""

    def _format_moat(self, analysis) -> str:
        if not analysis:
            return "# 第三章：核心优势与护城河\n\n数据缺失：护城河分析未完成"

        def get_val(obj, key, default='N/A'):
            return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)

        moat_text = get_val(analysis, 'moat_summary', get_val(analysis, 'core_advantages'))
        ten_year = get_val(analysis, 'ten_year_moat', get_val(analysis, 'moat_assessment'))

        return f"""# 第三章：核心优势与护城河

{moat_text}

## 十年护城河判断
{ten_year}
"""

    def _format_risk(self, analysis, round1) -> str:
        def get_val(obj, key, default='N/A'):
            return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)

        risk_text = get_val(analysis, 'risk_summary', get_val(analysis, 'risk_matrix')) if analysis else '数据缺失：风险分析未完成'

        base = f"""# 第四章：风险与挑战

{risk_text}
"""
        if round1:
            base += f"""
## 重大风险深度评估（辩论结论）
**风险判定**: {round1.risk_verdict}

{round1.risk_reasoning}
"""
        return base

    def _format_finance(self, analysis) -> str:
        if not analysis:
            return "# 第五章：财务分析\n\n数据缺失：财务分析未完成"

        def get_val(obj, key, default='N/A'):
            return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)

        return f"""# 第五章：财务分析

{get_val(analysis, 'finance_summary', get_val(analysis, 'financial_health'))}
"""

    def _format_leader(self, analysis, round1) -> str:
        def get_val(obj, key, default='N/A'):
            return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)

        leader_text = get_val(analysis, 'leader_profile', get_val(analysis, 'profile')) if analysis else '数据缺失：人物画像未完成'

        base = f"""# 第六章：董事长人物画像

{leader_text}
"""
        if round1:
            base += f"""
## 信任评估（辩论结论）
**信任判定**: {round1.trust_verdict}

{round1.trust_reasoning}
"""
        return base

    def _format_position(self, round2) -> str:
        if not round2:
            return "# 第七章：成本研究与建仓建议\n\n判断层未执行"
        return f"""# 第七章：成本研究与建仓建议

## 投资决策
**决策**: {round2.decision}
**置信度**: {round2.confidence:.0%}

## 多头观点
{round2.bull_case}

## 空头观点
{round2.bear_case}

## 建仓建议
{round2.position_suggestion}
"""

    async def _generate_overview(self, company_name: str, *chapters) -> str:
        # 简化实现：不调用 LLM，直接生成固定格式
        return f"# 第一章：概述\n\n{company_name} 调研报告概述。"

    async def _generate_summary(self, company_name: str, *chapters) -> str:
        # 简化实现：不调用 LLM，直接生成固定格式
        return f"# 第八章：总结\n\n{company_name} 调研报告总结。"
