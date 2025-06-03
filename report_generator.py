# report_generator.py

import json
from datetime import datetime

def generate_report(audit_results, report_format="json"):
    """
    Generates a report based on audit results.
    Args:
        audit_results (list): A list of dictionaries, each representing an audit function's result.
        report_format (str): The desired report format ('json', 'text', or 'markdown').
    Returns:
        str: The generated report content.
    """
    report_data = {
        "audit_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "audit_summary": {
            "total_checks": len(audit_results),
            "passed": sum(1 for r in audit_results if r["status"] == "PASS"),
            "failed": sum(1 for r in audit_results if r["status"] == "FAIL"),
            "warnings": sum(1 for r in audit_results if r["status"] == "WARN"),
            "errors": sum(1 for r in audit_results if r["status"] == "ERROR")
        },
        "audit_details": audit_results
    }

    if report_format == "json":
        return json.dumps(report_data, indent=4, ensure_ascii=False)
    elif report_format == "text":
        report_content = f"### Automated Security Audit Report ###\n\n"
        report_content += f"Audit Time: {report_data['audit_timestamp']}\n\n"
        report_content += "--- Summary ---\n"
        report_content += f"Total Checks: {report_data['audit_summary']['total_checks']}\n"
        report_content += f"Passed: {report_data['audit_summary']['passed']}\n"
        report_content += f"Failed: {report_data['audit_summary']['failed']}\n"
        report_content += f"Warnings: {report_data['audit_summary']['warnings']}\n"
        report_content += f"Errors: {report_data['audit_summary']['errors']}\n\n"
        report_content += "--- Detailed Results ---\n"
        for result in report_data["audit_details"]:
            report_content += f"  [{result['status']}] {result['name']}\n"
            report_content += f"    Details: {result['details']}\n\n"
        return report_content
    elif report_format == "markdown":
        report_content = f"# Automated Security Audit Report\n\n"
        report_content += f"**Audit Time:** {report_data['audit_timestamp']}\n\n"
        report_content += "## Summary\n"
        report_content += f"- **Total Checks:** {report_data['audit_summary']['total_checks']}\n"
        report_content += f"- **Passed:** {report_data['audit_summary']['passed']}\n"
        report_content += f"- **Failed:** {report_data['audit_summary']['failed']}\n"
        report_content += f"- **Warnings:** {report_data['audit_summary']['warnings']}\n"
        report_content += f"- **Errors:** {report_data['audit_summary']['errors']}\n\n"
        report_content += "## Detailed Results\n"
        for result in report_data["audit_details"]:
            status_emoji = ""
            if result['status'] == "PASS":
                status_emoji = "✅"
            elif result['status'] == "FAIL":
                status_emoji = "❌"
            elif result['status'] == "WARN":
                status_emoji = "⚠️"
            elif result['status'] == "ERROR":
                status_emoji = "❗"

            report_content += f"### {status_emoji} {result['name']} ({result['status']})\n"
            report_content += f"**Details:** {result['details']}\n\n"
        return report_content
    else:
        return "Unsupported report format."

def save_report(report_content, filename="security_audit_report", report_format="txt"):
    """
    Saves the generated report content to a file.
    """
    full_filename = f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{report_format}"
    try:
        with open(full_filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"Report successfully saved to '{full_filename}'.")
    except Exception as e:
        print(f"Error saving report: {e}")