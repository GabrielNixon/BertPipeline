#!/usr/bin/env python3
import os, sys, json
from pathlib import Path

# repo root on path
ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from bertmap.onto.onto_box import OntoBox
from bertmap.map.nes_map import NormEditSimMapping

def main(cfg_path):
    with open(cfg_path, "r") as f:
        cfg = json.load(f)

    d = cfg["data"]
    m = cfg["map"]
    bert_tok = cfg["bert"]["tokenizer_path"]

    task_dir = Path(d["task_dir"])
    task_dir.mkdir(parents=True, exist_ok=True)

    # Build OntoBox objects (constructor matches your fork)
    src = OntoBox(
        onto_file=d["src_onto_file"],
        onto_iri_abbr=d["src_onto"],
        synonym_properties=d.get("properties", ["label"]),
        tokenizer_path=bert_tok,
        cut=int(d.get("cut", 0)),
        from_saved=False,
    )
    print(src)

    tgt_path = d.get("tgt_onto_file") or d.get("tgt_onto_fil")
    tgt = OntoBox(
        onto_file=tgt_path,
        onto_iri_abbr=d["tgt_onto"],
        synonym_properties=d.get("properties", ["label"]),
        tokenizer_path=bert_tok,
        cut=int(d.get("cut", 0)),
        from_saved=False,
    )
    print(tgt)

    # Run NES mapping for each candidate_limit
    limits = m.get("candidate_limits", [50])
    for cl in limits:
        print(f"\n[NES] Running NormEditSimMapping with candidate_limit={cl} …")
        mapper = NormEditSimMapping(src_ob=src, tgt_ob=tgt, candidate_limit=int(cl), save_dir=str(task_dir))
        mapper.run()
        print(f"[NES] Done candidate_limit={cl}. Outputs under: {task_dir}/")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=True)
    args = parser.parse_args()
    main(args.config)
