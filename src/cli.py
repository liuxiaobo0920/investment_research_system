"""CLI 用户接口"""
import asyncio
import sys
from datetime import datetime
from src.agents.composition import ReportAssembler


async def research(company_name: str):
    """执行调研"""
    print(f"开始调研：{company_name}")

    # 简化实现：直接调用 ReportAssembler
    assembler = ReportAssembler(agent_id="cli_assembler")

    input_data = {
        "company_name": company_name,
        "company_code": "MOCK",
    }

    report = await assembler.execute(input_data)

    # 输出报告
    from pathlib import Path
    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / f"{company_name}_{datetime.now().strftime('%Y%m%d')}.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"{report.ch1_overview}\n\n")
        f.write(f"{report.ch2_industry}\n\n")
        f.write(f"{report.ch3_moat}\n\n")
        f.write(f"{report.ch4_risk}\n\n")
        f.write(f"{report.ch5_finance}\n\n")
        f.write(f"{report.ch6_leader}\n\n")
        f.write(f"{report.ch7_position}\n\n")
        f.write(f"{report.ch8_summary}\n\n")

    print(f"报告已生成：{output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != "research":
        print("用法: python -m src.cli research <公司名>")
        sys.exit(1)

    company = sys.argv[2]
    asyncio.run(research(company))
