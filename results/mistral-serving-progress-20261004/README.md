# Mistral serving profile — first audited concurrency

Only c1 of three original profiles completed; c2/c4 and MiMo/report/exits remain required.

[u20261003-mistral35-serving-c1](../u20261003-mistral35-serving-c1/result.json):60/60 measured responses and2 separate warmups. Measured wall3229.284162s; HTTP aggregate output **4.75647209tok/s**, median latency53.513639s/p9554.773583s, median TTFT33.168544s/p9534.081739s. These are end-to-end serving definitions, not cold native decode or tasks solved.

Actual native prompt counts8215(8responses)/8216(52), all60actual outputs256, total15360outputtokens, reported reused inputtokens0. Input target8192 is distinct from observed counts; all are within the declared8192–8256 admissible interval. All60length-finished responses/rawtext/requests/SSE/usage retained; warmups excluded from metrics. Temperature0/noexplicit seed/cache_promptfalse, unchanged16384 context per native slot/1slot/900s requests/7200s job. Zero reused native input tokens does not mean zero physical native cache memory; existing native cache allocator snapshots are not retuned.

Whole-child minimum143.280380GiB available/positive swapgrowth0.000000MiB. All8 original M5 and8 publication artifact hashes/6 sourceblobs/corpus/model/native/runtime pins checked; original c1 workers exited. Raw model bytes/native source unchanged.

Task-owned display-awake assertion was disabled throughout c1; actual screen pixels were not inspected. The owner's later display-awake restoration occurred during c2 after measurement began; that condition change is preserved, with no causal timing-effect or clean concurrency-only attribution. The three-profile series is incomplete. This is our portable harness using AIPerf-style metric definitions, not an official benchmark submission or hardware ceiling.
