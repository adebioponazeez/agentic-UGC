# Failure and recovery

Invalid input rejects before model calls. Transient provider failure retries within policy. Persistent
failure opens the circuit and checkpoints failure. Budget exhaustion fails before the next logical
call. Approval failure rejects without state transition. Storage failure propagates and cannot claim
completion. Critical policy failure must block regardless of average score.

Never regenerate an approved stage on normal resume; interpret unsupported state; retry unsafe side
effects; change run identity; or recover without recording authority and reason. Failed-stage auto
resume, leases, and transactional outbox remain production work.
