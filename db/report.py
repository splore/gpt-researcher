import json
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_utils import save_report_sections


async def save_sections(psql_sess: AsyncSession, research_report: dict, task_id: str, report_style: str):
    research_data = research_report.get('research_data')
    sections = []
    sources_section = {"order": 0, "report_id": task_id, "title": 'sources', "content":
        json.dumps(research_report.get('sources')), "guideline": '',
                       "editable": False}
    for section in research_data:
        title, = section
        content = section[title]
        sections.append(
            {"order": 0, "report_id": task_id, "title": title, "content": content, "guideline": '',
             "editable": True})

    if report_style == 'summary':
        sections.append(sources_section)
    else:
        for index, key in enumerate(['executive_summary', 'introduction', 'table_of_contents']):
            sections.insert(index, {"order": 0, "report_id": task_id, "title": key,
                                    "content": research_report.get(key), "guideline": '',
                                    "editable": False})

        sections.append({"order": 0, "report_id": task_id, "title": 'conclusion',
                         "content": research_report.get('conclusion'), "guideline": '', "editable": False})
        sections.append(sources_section)

    sections = [{**d, 'order': index} for index, d in enumerate(sections)]
    await save_report_sections(psql_sess, sections)
