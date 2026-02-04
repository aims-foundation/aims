#!/usr/bin/env python3
"""
Pre-compute small data subsets for interactive pyodide visualization in Chapter 1.
Saves subsets as JSON files that can be loaded in the browser.

Usage:
    python scripts/precompute_data_subsets.py
"""

import json
import pickle
import numpy as np
from pathlib import Path

# Configuration
N_TAKERS = 50  # Number of test takers (models) to include
N_ITEMS = 100  # Number of items (questions) to include
OUTPUT_DIR = Path(__file__).parent.parent / "src" / "data"

def numpy_to_list(arr):
    """Convert numpy array to nested list, handling NaN values."""
    result = []
    for row in arr:
        row_data = []
        for val in row:
            if np.isnan(val):
                row_data.append(None)
            else:
                row_data.append(float(val))
        result.append(row_data)
    return result

def main():
    # Use cached data
    cache_path = Path("/lfs/skampere2/0/sttruong/.cache/huggingface/hub/datasets--stair-lab--reeval_fa/snapshots/a0c7e788bbec27820dab1c9da39b56c43f792926")

    if not cache_path.exists():
        # Try home directory cache
        cache_path = Path.home() / ".cache/huggingface/hub/datasets--stair-lab--reeval_fa/snapshots"
        if cache_path.exists():
            snapshots = list(cache_path.iterdir())
            if snapshots:
                cache_path = snapshots[0]
        else:
            raise FileNotFoundError("No cached data found. Please run with HuggingFace authentication first.")

    print(f"Using cached data from: {cache_path}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Process HELM data
    print("\nProcessing HELM Benchmark data...")
    with open(cache_path / "data/HELM_benchmark.pkl", "rb") as f:
        helm_df = pickle.load(f)

    # DataFrame: rows are models, columns are questions
    helm_matrix = helm_df.values  # Convert to numpy array
    helm_n_takers = min(N_TAKERS, helm_matrix.shape[0])
    helm_n_items = min(N_ITEMS, helm_matrix.shape[1])
    helm_subset = helm_matrix[:helm_n_takers, :helm_n_items]

    # Get model names and item info for subset
    helm_models = list(helm_df.index[:helm_n_takers])

    helm_output = {
        "full_shape": [int(helm_matrix.shape[0]), int(helm_matrix.shape[1])],
        "subset_shape": [helm_n_takers, helm_n_items],
        "models": helm_models,
        "data": numpy_to_list(helm_subset)
    }

    helm_path = OUTPUT_DIR / "helm_subset.json"
    with open(helm_path, "w") as f:
        json.dump(helm_output, f)
    print(f"  Full: {helm_matrix.shape[0]} x {helm_matrix.shape[1]}")
    print(f"  Subset: {helm_n_takers} x {helm_n_items}")
    print(f"  Saved to: {helm_path}")

    # Process Open LLM data
    print("\nProcessing Open LLM Leaderboard data...")
    with open(cache_path / "data/benchmark_data_open_llm_full_no_arc.pkl", "rb") as f:
        openllm_df = pickle.load(f)

    openllm_matrix = openllm_df.values
    openllm_n_takers = min(N_TAKERS, openllm_matrix.shape[0])
    openllm_n_items = min(N_ITEMS, openllm_matrix.shape[1])
    openllm_subset = openllm_matrix[:openllm_n_takers, :openllm_n_items]

    # Get model names for subset
    openllm_models = list(openllm_df.index[:openllm_n_takers])

    openllm_output = {
        "full_shape": [int(openllm_matrix.shape[0]), int(openllm_matrix.shape[1])],
        "subset_shape": [openllm_n_takers, openllm_n_items],
        "models": openllm_models,
        "data": numpy_to_list(openllm_subset)
    }

    openllm_path = OUTPUT_DIR / "openllm_subset.json"
    with open(openllm_path, "w") as f:
        json.dump(openllm_output, f)
    print(f"  Full: {openllm_matrix.shape[0]} x {openllm_matrix.shape[1]}")
    print(f"  Subset: {openllm_n_takers} x {openllm_n_items}")
    print(f"  Saved to: {openllm_path}")

    print("\nDone! Data subsets saved to src/data/")

if __name__ == "__main__":
    main()
