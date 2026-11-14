# Ludwig

This is a local-first Wittgenstein learning app. Preserve these requirements:

- Keep notes, preferences, and imported source files on the device. Do not add analytics, cloud sync, remote AI requests, or third-party runtime assets without a clear user instruction.
- Keep explanations accessible while preserving philosophical distinctions. Identify invented examples, scholarly disagreements, and secondary commentary.
- Ground textual claims in `data/sources.json`. Do not invent quotations, page offsets, German originals, or bibliographic metadata. Use stable numbered remarks where possible.
- Preserve JSON content IDs and IndexedDB identities across updates.
- Rebuild the complete offline pack after every app or content change. Keep navigation and assets compatible with a subdirectory deployment.
- Run `npm run check`. Check notes across reloads, offline navigation, and mobile layout for changes that affect those flows.
- Do not commit users’ notes, imported books, credentials, keystores, or test downloads.
