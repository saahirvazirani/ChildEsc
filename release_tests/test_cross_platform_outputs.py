import csv
import math
import tempfile
import unittest
from pathlib import Path

from childesc import analysis, contracts, evaluate
from childesc.metrics import ACTION_LEVEL, compute_metrics


ROOT = Path(__file__).resolve().parents[1]


class CrossPlatformOutputTests(unittest.TestCase):
    def test_macro_f1_uses_high_precision_aggregation(self):
        rows = []
        with (ROOT / "results" / "predictions.csv").open(newline="") as stream:
            for row in csv.DictReader(stream):
                if row["system"] == "childesc_rules":
                    rows.append(row)

        scores = []
        for label in ACTION_LEVEL:
            true_positive = sum(
                row["gold_action"] == label and row["predicted_action"] == label
                for row in rows
            )
            false_positive = sum(
                row["gold_action"] != label and row["predicted_action"] == label
                for row in rows
            )
            false_negative = sum(
                row["gold_action"] == label and row["predicted_action"] != label
                for row in rows
            )
            precision = true_positive / (true_positive + false_positive)
            recall = true_positive / (true_positive + false_negative)
            scores.append(2 * precision * recall / (precision + recall))

        expected = math.fsum(scores) / len(scores)
        self.assertEqual(compute_metrics(rows)["macro_f1"], expected)

    def test_every_generated_csv_uses_lf_line_endings(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            data = ROOT / "benchmark" / "childesc_v0_1.jsonl"
            evaluate.run(data, output)
            analysis.run(data, output / "predictions.csv", output)
            contracts.run(
                ROOT / "benchmark" / "contract_probes.json",
                ROOT / "benchmark" / "source_register.json",
                output,
            )

            csv_paths = sorted(output.glob("*.csv"))
            self.assertTrue(csv_paths)
            for path in csv_paths:
                with self.subTest(path=path.name):
                    self.assertNotIn(b"\r\n", path.read_bytes())


if __name__ == "__main__":
    unittest.main()
