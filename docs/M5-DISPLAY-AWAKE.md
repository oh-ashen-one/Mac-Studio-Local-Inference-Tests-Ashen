# M5 display-awake configuration

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

Check that the disabled destination does not already exist before moving it. Keep the benchmark driver, model workers and separate system-awake assertion untouched. The backed-up plist can be moved back and bootstrapped for reversal. These removal commands were documented, not executed.
