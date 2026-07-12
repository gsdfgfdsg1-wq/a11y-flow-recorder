import unittest
from a11y_flow import audit, playwright


class A11yFlowTests(unittest.TestCase):
    def test_accepts_named_keyboard_flow(self):
        flow = {"steps": [{"action": "keyboard", "key": "Enter", "element": {"role": "button", "name": "Save", "selector": "#save", "keyboard_reachable": True}}]}
        self.assertTrue(audit(flow)["ok"])
        self.assertIn("press('Enter')", playwright(flow))

    def test_detects_missing_accessible_name(self):
        flow = {"steps": [{"action": "click", "element": {"role": "button", "selector": "#delete"}}]}
        self.assertEqual(audit(flow)["issues"][0]["rule"], "accessible-name")

    def test_detects_keyboard_dead_end(self):
        flow = {"steps": [{"action": "keyboard", "element": {"role": "link", "name": "Next", "keyboard_reachable": False}}]}
        self.assertEqual(audit(flow)["issues"][0]["rule"], "keyboard-path")


if __name__ == "__main__":
    unittest.main()
