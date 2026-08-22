# Specification lifecycle and drift

1. Create task linked to requirements and evidence.
2. Update proposed specification and acceptance criteria before code.
3. Record ADR for architectural, irreversible, security, or compatibility changes.
4. Implement the smallest compliant change.
5. Add tests and run the complete suite.
6. Record objections, residual risk, and evidence.
7. Update changelog and versions.
8. Compare released outcomes to assumptions and reopen the spec when reality differs.

Each release checks for undocumented behavior, requirements without tests, tests without accepted
requirements, changed providers/platforms/law/threats/users, and future controls described as current.
Checkpoints carry schema/workflow versions. Prompt, rubric, policy, model, and workflow changes remain
independently rollbackable.
