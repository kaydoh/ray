"""Small cluster training

This training run will start 4 workers on 4 nodes (including head node).

Test owner: krfricke

Acceptance criteria: Should run through and report final results.
"""
import json
import os
import time

import ray
from xgboost_ray import RayParams

from ray.util.xgboost.release_test_util import train_ray

if __name__ == "__main__":
    ray.client().job_name(os.environ["RAY_JOB_NAME"]).connect()

    ray_params = RayParams(
        elastic_training=False,
        max_actor_restarts=2,
        num_actors=4,
        cpus_per_actor=4,
        gpus_per_actor=0)

    @ray.remote
    def train():
        train_ray(
            path="/data/classification.parquet",
            num_workers=4,
            num_boost_rounds=100,
            num_files=25,
            regression=False,
            use_gpu=False,
            ray_params=ray_params,
            xgboost_params=None,
        )

    start = time.time()
    ray.get(train.remote())
    taken = time.time() - start

    result = {
        "time_taken": taken,
    }
    test_output_json = os.environ.get("TEST_OUTPUT_JSON",
                                      "/tmp/train_small.json")
    with open(test_output_json, "wt") as f:
        json.dump(result, f)

    print("PASSED.")
