# Charlotte Ultra — Historia zmian

## v6.3 — Pioneer Edition (2026-08)
**"World's First" features:**
- ⭐ Intent Ledger: AI zapamiętuje i wznawia zadania z localStorage
- ⭐ Soul Lease Mesh: multi-agent mesh w kartach przeglądarki (BroadcastChannel)
- ⭐ Browser Code Lab: sandbox AI z SHA-256 evidence record, zero serwera
- 21 paneli ogółem

## v6.2 — UX Edition (2026-07)
- Quick Action Bar (pasek u góry z 6 szybkimi akcjami)
- Onboarding Wizard (modal przy pierwszym uruchomieniu)
- Skróty klawiszowe Ctrl+1, Ctrl+2, Ctrl+3, Ctrl+4
- Nowy panel: Notepad AI
- Nowy panel: Kalkulator Budżetu
- Nowy panel: Generator Haseł Pro
- Nowy panel: System Check (diagnostyka przeglądarki)
- Dark/light mode toggle

## v6.1 — Security Edition (2026-06)
- sanitizeHTML() — pełna ochrona przed XSS
- SecureStorage z AES-GCM (szyfrowane klucze API w localStorage)
- CharlotteIntervals — jeden zarządca setInterval (zero memory leaks)
- LocalStore DRY — jeden wrapper localStorage
- Feistel cipher ostrzeżenie (nie do produkcji crypto)
- Monte Carlo limit (max iteracji, brak infinite loop)

## v6.0 — Base Edition (2026-05)
- 14 paneli: Chat AI, Trading Bot, Crypto Suite, Memory/IndexedDB, RAG/TF-IDF
- Voice STT+TTS PL, Multi-Agent, Skills, Observability, Legal AI PL
- WinPot, CMS, Deploy/Config, Business Plan, Crypto Cipher
- Fallback LLM: Ollama (0 zł) → DeepSeek → OpenAI → Azure → Offline
- Standalone HTML, zero instalacji, zero serwera
