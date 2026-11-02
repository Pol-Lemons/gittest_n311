import math 
import unittest
from pathlib import Path

import joblib
import pandas as pd

MODEL_PATH = (
    Path(__file__).resolve().parent
    /"audi_forest_app.joblib"
)

class TestModelBundle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not MODEL_PATH.is_file():
            raise FileNotFoundError(
                f"Model file not found: {MODEL_PATH}"
            )
        cls.bundle= joblib.load(MODEL_PATH)
    def test_require_bundle_keys(self):
        required_keys = {
            "pipeline",
            "features",
            "categories",
            "training_range",
            "known_configurations",
        }

        self.assertTrue(
            required_keys.issubset(self.bundle.keys()),
            "The model bundle is missing required keys."
        )

    def test_feature_contract(self):
        expected_features = {
            "model",
            "year",
            "transmission",
            "mileage",
            "fuelType",
            "tax",
            "mpg",
            "engineSize",
        }
        self.assertEqual(
            set(self.bundle["features"]),
            expected_features
        )
    def test_metadata_is_not_empty(self):
        self.assertTrue(self.bundle["categories"])
        self.assertTrue(self.bundle["training_range"])

        known = pd.DataFrame(
            self.bundle["known_configurations"]
        )
        self.assertFalse(known.empty)

    def test_pipeline_can_predict_one_car(self):
        pipeline = self.bundle["pipeline"]
        features = self.bundle["features"]
        ranges = self.bundle["training_range"]

        known = pd.DataFrame(
            self.bundle["known_configurations"]
        )

        configuration = known.iloc[0]

        def mid_point(column):
            minimum = ranges[column]["min"]
            maximum = ranges[column]["max"]
            return (minimum + maximum)/2
        sample_car = {
            "model": configuration["model"],
            "year": round((self.bundle["year_min"]+self.bundle["year_max"])/2),
            "transmission": configuration["transmission"],
            "mileage": mid_point("mileage"),
            "fuelType": configuration["fuelType"],
            "tax": mid_point("tax"),
            "mpg": mid_point("mpg"),
            "engineSize": configuration["engineSize"],
        }
        sample_df = pd.DataFrame(
            [sample_car],
            columns=features    
        )

        prediction = pipeline.predict(sample_df)

        self.assertEqual(len(prediction),1)
        self.assertTrue(math.isfinite(prediction[0]))
        self.assertGreater(prediction[0],0)
if __name__ == "__main__":
        unittest.main() 

    