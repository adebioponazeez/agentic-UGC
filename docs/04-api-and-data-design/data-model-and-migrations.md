# Data model and migration policy

**Status:** MVP contract

- `events`: append-oriented run/stage events.
- `lessons`: domain lesson, confidence, evidence reference.
- `checkpoints`: latest durable payload, status, artifact hash.
- `approvals`: unique run/digest approval and reviewer identity.

| Data | Class | Rule |
|---|---|---|
| Goal/artifact | Internal | Tenant-scoped in production |
| Approver identity | Personal | Minimize and restrict |
| Credentials | Secret | Never persist or put in model context |
| Provider content | Sensitive | Metadata default; content opt-in |
| Research/media | Personal/IP possible | Consent, rights, purpose, deletion required |

## Migration rules

Read `PRAGMA user_version`; apply ordered transactional migrations; reject newer databases; back up
before destructive migration; test empty/current/previous versions; never reinterpret historical
approval digests or events. SQLite is local MVP storage, not multi-worker production storage.
