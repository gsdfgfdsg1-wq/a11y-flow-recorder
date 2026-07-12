#!/usr/bin/env python3
"""Validate recorded accessibility flows and emit a Playwright test."""
import argparse
import json
from pathlib import Path


INTERACTIVE = {"button", "link", "input", "select", "textarea"}


def audit(flow):
    issues, previous_tabindex = [], -1
    for index, step in enumerate(flow["steps"]):
        element = step.get("element", {})
        role = element.get("role")
        if role in INTERACTIVE and not element.get("name"):
            issues.append({"step": index, "rule": "accessible-name", "message": f"{role} has no accessible name"})
        if step.get("action") == "keyboard" and not element.get("keyboard_reachable", False):
            issues.append({"step": index, "rule": "keyboard-path", "message": "target is not keyboard reachable"})
        tabindex = element.get("tabindex")
        if isinstance(tabindex, int) and tabindex > 0 and tabindex < previous_tabindex:
            issues.append({"step": index, "rule": "focus-order", "message": "positive tabindex moves backwards"})
        if isinstance(tabindex, int) and tabindex > 0:
            previous_tabindex = tabindex
    return {"issues": issues, "ok": not issues, "steps_checked": len(flow["steps"])}


def playwright(flow):
    lines = ["import { test, expect } from '@playwright/test';", "", "test('recorded accessible flow', async ({ page }) => {"]
    for step in flow["steps"]:
        selector = step.get("element", {}).get("selector", "body")
        action = step.get("action")
        if action == "click":
            lines.append(f"  await page.locator({selector!r}).click();")
        elif action == "fill":
            lines.append(f"  await page.locator({selector!r}).fill({step.get('value', '')!r});")
        elif action == "keyboard":
            lines.append(f"  await page.locator({selector!r}).press({step.get('key', 'Tab')!r});")
    lines.extend(["  await expect(page.locator('body')).toBeVisible();", "});"])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("flow")
    parser.add_argument("--test-out")
    args = parser.parse_args()
    flow = json.loads(Path(args.flow).read_text())
    report = audit(flow)
    if args.test_out:
        Path(args.test_out).write_text(playwright(flow))
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
