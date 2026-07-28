#!/usr/bin/env python3
"""Strict union-of-output catalog coverage for protocol-matched ranked lists."""

import argparse
import json
import pickle


def load_rows(path):
    raw = json.load(open(path))
    if "per_user" in raw:
        raw = raw["per_user"]
    if not isinstance(raw, dict):
        raise TypeError(f"{path}: expected a user-keyed JSON object")
    return raw


def summarize(path, expected_users, catalog_size, ks):
    rows = load_rows(path)
    if len(rows) != expected_users:
        raise ValueError(
            f"{path}: {len(rows)} users, expected {expected_users}"
        )
    output = {}
    for cutoff in ks:
        union = set()
        for uid, row in rows.items():
            items = [int(item) for item in row["top_items"]]
            if len(items) < cutoff:
                raise ValueError(
                    f"{path}: user {uid} has {len(items)} items, needs {cutoff}"
                )
            top = items[:cutoff]
            if len(top) != len(set(top)):
                raise ValueError(f"{path}: user {uid} has duplicates at {cutoff}")
            invalid = [item for item in top if item <= 0 or item > catalog_size]
            if invalid:
                raise ValueError(
                    f"{path}: user {uid} has invalid IDs {invalid[:5]}"
                )
            union.update(top)
        output[str(cutoff)] = {
            "unique_retrieved_items": len(union),
            "catalog_size": catalog_size,
            "catalog_coverage": len(union) / catalog_size,
        }
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument(
        "--method", action="append", nargs=2, metavar=("NAME", "JSON"),
        required=True,
    )
    parser.add_argument("--ks", default="10,100")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    with open(args.data, "rb") as handle:
        data = pickle.load(handle)
    expected_users = len(data["test"])
    catalog_size = int(data["num_items"]) - 1
    ks = [int(value) for value in args.ks.split(",")]
    result = {
        name: summarize(path, expected_users, catalog_size, ks)
        for name, path in args.method
    }
    with open(args.output, "w") as handle:
        json.dump(result, handle, indent=2)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
