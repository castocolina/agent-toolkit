# Gemini CLI timeout diagnosis

1. Check the captured output, elapsed time, and the exact process PID/state launched for the task. No network socket alone does not prove a hang.
2. If the command exceeded its timeout, terminate only the owned PID/process group: send `TERM`, wait briefly, then `KILL` only if still present.
3. Check CLI version and authentication/configuration errors before retrying. Report the concrete symptom and request direction before changing approval mode or expanding access.
