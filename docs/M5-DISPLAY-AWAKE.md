# M5 display-awake configuration

## Current owner preference: displays awake on both Macs, October4 2026

The owner directly requested caffeinate display-awake protection for both machines and their connected monitors, superseding the earlier display-sleep preference. On the M5 the exact retained LaunchAgent plist was restored and bootstrapped unchanged; launchctl and pmset verify its display-idle prevention assertion under PID27102. M5 system-awake PID50803 remains independently active. On the M3 controller the existing caffeinate PID1182 already prevents display/system idle sleep; it was preserved, with no duplicate permanent assertion or takeover. Display-wake requests were issued on both Macs. These are global display-idle assertions for each machine's connected monitors; physical monitor pixels were not independently inspected.

Receipt [owner display-awake transition](../hardware/owner-display-awake-20261004.json). M5 service creation16:35:44.864UTC/verified16:38:12UTC. Benchmark driver19150/wrapper26107/server26138 retained the same creation times during original serving-c2. The display-condition transition occurred after measurement started at16:31:10UTC; preserve original timings and record this covariate without a causal timing-effect claim. No stored power/lock/security setting or inference configuration changed.

Keep display-awake protection active on both Macs unless the owner changes this preference again. Verify M5 only through launchctl/pmset owning-PID metadata; never retry or elevate previously denied raw process-argument inspection. The M5 per-user agent runs at GUI login after reboot; no automatic login is enabled. The existing M3 assertion is verified current, without a new persistence-after-reboot claim.

## Historical owner preference: display sleep, October4 2026

The owner directly requested monitors off while testing continues. The named display-only service was unloaded through launchctl and its exact original plist retained as `.plist.disabled`; it will not automatically load at the next GUI login. Do not re-enable it without a new owner request. Display-only sleep requests succeeded on M5 and M3 controller. System-awake `caffeinate -is` PID50803 remains active on M5; no benchmark worker was stopped/restarted. Stored power/lock/security settings stayed unchanged. Receipt: `../hardware/owner-display-sleep-20261004.json`. Physical monitor pixels were not independently inspected. The prior installation evidence below is historical.

Owner-authorized through Midir on October 2, 2026. Target verified as Mac17,15 / Apple M5 Ultra. This affects display idle sleep only; the benchmark runner and system-awake assertion remain independently owned.

- Label: `com.ashen.benchmark.display-awake`
- M5 location: `~/Library/LaunchAgents/com.ashen.benchmark.display-awake.plist`
- Program: `/usr/bin/caffeinate -d`
- Domain: `gui/501` on the verified installation
- Settings: RunAtLoad and KeepAlive, Background process type
- [Exact plist](power/com.ashen.benchmark.display-awake.plist)

The LaunchAgent was successfully bootstrapped and verified running as PID 68047. `pmset -g assertions` showed its display-idle prevention assertion. The old task-owned display-only PID 67253 was terminated only after replacement verification and was confirmed absent afterward. System-awake PID 50803 and benchmark driver/worker PIDs 55667/66001/66017 remained unchanged and active.

**Persistence:** launchd loads this per-user agent at GUI login, including the next user login after reboot. It does not run before that login and does not enable automatic login. No reboot was performed to test persistence; installation, plist validation and current service/assertion state were verified.

The attempt to set AC `displaysleep` from 10 to 0 with `sudo -n pmset` was blocked by `sudo: a password is required`; the stored value remains **10 minutes**. No privileged change, password/lock change or security-protection change was made. Initial direct process-argument inspection for the launchd child was denied by macOS; that inspection was not retried or elevated. Verification used the normally permitted launchctl service metadata and pmset owning-PID assertion instead.

## Verify on the M5

```sh
launchctl print gui/501/com.ashen.benchmark.display-awake
pmset -g assertions
pmset -g custom
```

Use the live service PID rather than relying on the historical number above. Physical monitor pixels have not been independently inspected.

## Revert when the owner requests it

On the verified M5 as its logged-in user, unload only this named service and move its plist out of the auto-loaded location:

```sh
launchctl bootout gui/501/com.ashen.benchmark.display-awake
mv "$HOME/Library/LaunchAgents/com.ashen.benchmark.display-awake.plist" "$HOME/Library/LaunchAgents/com.ashen.benchmark.display-awake.plist.disabled"
```

Check that the disabled destination does not already exist before moving it. Keep the benchmark driver, model workers and separate system-awake assertion untouched. The backed-up plist can be moved back and bootstrapped for reversal. These removal commands were executed on October4 under the owner’s direct display-off request. The original plist bytes were retained and hash-checked. Re-enable only after a new owner request.
