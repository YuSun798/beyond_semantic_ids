# Table 4 Catalog-Coverage Audit

Audit date: 2026-07-28

Table 4 reports the number of distinct catalog items in the union of every
test user's Top-\(K\) output:

\[
\left|\bigcup_u \operatorname{TopK}(u)\right| / |\mathcal I|.
\]

## Protocol invariants

- TIGER uses valid-prefix trie-constrained decoding and exact code lookup.
- There is no nearest-code or squared-code-distance fallback.
- Padding item 0 is excluded from the trie and all outputs.
- History items are filtered before the returned list is formed.
- Internal beam width starts at 100 and expands adaptively when necessary.
- Every method returns exactly 100 valid, distinct items for every test user.
- The strict summarizer aborts on an invalid ID, duplicate, short list,
  unexpected user count, or inconsistent catalog denominator.
- A second independent checker reproduced every count below without importing
  the strict summarizer.

## Exact results

| Dataset | Catalog | Users | Method | Union@10 | Coverage@10 | Union@100 | Coverage@100 |
|---|---:|---:|---|---:|---:|---:|---:|
| ML-1M | 3,416 | 6,040 | TIGER | 2,394 | 70.081967% | 3,314 | 97.014052% |
| ML-1M | 3,416 | 6,040 | CQG-Single | 2,380 | 69.672131% | 3,334 | 97.599532% |
| ML-1M | 3,416 | 6,040 | CQG-AR | 2,346 | 68.676815% | 3,335 | 97.628806% |
| Beauty | 12,101 | 22,363 | TIGER | 9,004 | 74.407074% | 11,661 | 96.363937% |
| Beauty | 12,101 | 22,363 | CQG-Single | 10,837 | 89.554582% | 12,090 | 99.909098% |
| Beauty | 12,101 | 22,363 | CQG-AR | 10,637 | 87.901826% | 12,078 | 99.809933% |
| Sports | 10,693 | 21,519 | TIGER | 10,047 | 93.958665% | 10,638 | 99.485645% |
| Sports | 10,693 | 21,519 | CQG-Single | 6,743 | 63.059946% | 10,366 | 96.941925% |
| Sports | 10,693 | 21,519 | CQG-AR | 7,676 | 71.785280% | 10,524 | 98.419527% |

## TIGER checkpoint selection and returned-list checks

| Dataset | Selected checkpoint | Mean length | Min length | Full-length fraction | Max internal beam |
|---|---|---:|---:|---:|---:|
| ML-1M | `decoder_step40000.pt` | 100 | 100 | 1.0 | 800 |
| Beauty | `decoder_step10000.pt` | 100 | 100 | 1.0 | 200 |
| Sports | `decoder_step40000.pt` | 100 | 100 | 1.0 | 200 |

Checkpoint selection used constrained validation on the same fixed 500-user
sample for all saved 10K--50K-step checkpoints.

## Ranked-list provenance

- ML-1M TIGER:
  `results/tiger_ml1m_s42_constrained_matched100_v2.json`
  (`sha256:22c74ebd047c26b0ec6751f8b4332a20e4ffa8680358d7132a1e8a698bfa618d`)
- Beauty TIGER:
  `results/tiger_beauty_s42_constrained_matched100_v2.json`
  (`sha256:b8407ff39c393a5170adaac6ffea4352f7980d9d1c172c20b20fe1b42bea3276`)
- Sports TIGER:
  `results/tiger_sports_s42_constrained_matched100_v2.json`
  (`sha256:469f12a3fc45b82d7266095215cd34f203f189e258a290713d6725663c0bc9fe`)

Strict summary hashes:

- ML-1M: `66470c538110e71e7c610038c60194c98abe5ab91c352c5c9a06e05a6ad0a3bf`
- Beauty: `c075dadbf2b0fd3b79ee85f199e89ae7665d24ecab61d695bde7e896274a6246`
- Sports: `cf68b61a2d679667677d9fa7897a92fad074dc6244573f5e60fcd704c4b2c885`

The large per-user ranked-list files are retained in the local/remote
reproduction archive rather than committed to Git.
