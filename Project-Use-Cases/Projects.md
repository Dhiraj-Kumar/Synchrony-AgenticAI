## Overview

| # | Project | Level | Key Built-in Tools |
|---|---------|-------|--------------------|
| 1 | Tax Circular Q&A Agent | Intermediate | Retriever tool (BM25), DuckDuckGo |
| 2 | Bank Statement SQL Analyst | Intermediate | SQLDatabaseToolkit |
| 3 | Capital Gains Analyst | Intermediate | PythonREPLTool, ReadFileTool |
| 4 | Company Due-Diligence Brief | Intermediate | Wikipedia, YahooFinanceNews |
| 5 | SEC Filing Explorer | Showcase | RequestsGetTool, JsonSpec toolkit |
| 6 | Tax Rule Change Tracker | Intermediate | DuckDuckGo, RequestsGetTool, WriteFileTool |
| 7 | Expense Claim Auditor with Approval | Showcase | RequestsGetTool, File tools, HumanInTheLoopMiddleware |
| 8 | Invoice Audit Report Generator | Intermediate | FileManagementToolkit |
| 9 | Portfolio News Digest | Starter | YahooFinanceNews, WriteFileTool |
| 10 | Finance Research Scout | Starter | ArxivQueryRun, WikipediaQueryRun |

**Common setup:** `langchain`, `langchain-community`, one chat model provider package, and an LLM API key. No database server, no cloud account, no auth.

---

## 1. Tax Circular Q&A Agent

- **Scenario:** A finance team has a handful of tax circulars and FAQ notes. They want quick answers with a check for newer changes on the web.
- **Agent flow:** Question → search local circulars → if unclear or outdated, search the web → answer with source.
- **Built-in tools:** `create_retriever_tool` with a BM25 retriever (no embeddings, no vector DB), `DuckDuckGoSearchRun`
- **Custom tool:** None
- **Sample data:** 3 to 5 `.txt` circular files in a `circulars/` folder
- **Sample prompt:** "What is the TDS threshold on rent, and has it changed recently?"
- **Expected output:** Answer citing the local file, plus a note on any newer web finding.
- **Learning outcome:** Retrieval as a tool, tool selection between local and web sources.

## 2. Bank Statement SQL Analyst

- **Scenario:** An analyst wants to question a bank statement in plain English instead of writing SQL.
- **Agent flow:** Question → list tables → read schema → check query → run query → explain result.
- **Built-in tools:** `SQLDatabaseToolkit` (list tables, schema, query, query checker)
- **Custom tool:** One-time script that loads a sample CSV into SQLite
- **Sample data:** `statement.csv` with date, description, amount, category
- **Sample prompt:** "Top 5 spends last quarter. Any duplicate debits?"
- **Expected output:** Table of results with a short explanation.
- **Learning outcome:** SQL agent pattern, safe read-only querying.

## 3. Capital Gains Analyst

- **Scenario:** An investor has a trade history and needs short-term vs long-term gains.
- **Agent flow:** Read CSV → write pandas code → run it → summarize gains by holding period.
- **Built-in tools:** `PythonREPLTool`, `ReadFileTool`
- **Custom tool:** None
- **Sample data:** `trades.csv` with symbol, date, buy/sell, quantity, price
- **Sample prompt:** "Match buys and sells (FIFO) and show short-term and long-term gains."
- **Expected output:** Gains table plus a plain-language summary.
- **Learning outcome:** Code-execution tool, letting code (not the LLM) do the math.
- **Caution:** `PythonREPLTool` runs code. Use for demos only, never on untrusted input.

## 4. Company Due-Diligence Brief

- **Scenario:** A relationship manager needs a quick strengths-and-risks brief on a listed company.
- **Agent flow:** Company background → latest news → price summary → structured brief.
- **Built-in tools:** `WikipediaQueryRun`, `YahooFinanceNewsTool`
- **Custom tool:** `get_price_summary` (small yfinance wrapper)
- **Sample prompt:** "Prepare a due-diligence brief on INFY."
- **Expected output:** Background, recent news, price trend, 3 strengths, 3 risks.
- **Learning outcome:** Combining static and live sources into one report.

## 5. SEC Filing Explorer

- **Scenario:** An analyst wants key figures from a company's SEC filing data without reading raw JSON.
- **Agent flow:** Fetch EDGAR JSON → explore keys → find revenue, net income, debt → summarize.
- **Built-in tools:** `RequestsGetTool` (with `User-Agent` header), `JsonSpec` toolkit
- **Custom tool:** None
- **Sample prompt:** "Show revenue and net income for the last 3 fiscal years."
- **Expected output:** Year-wise figures with a short trend note.
- **Learning outcome:** Navigating large JSON, working with a real public API.
- **Note:** `RequestsGetTool` requires `allow_dangerous_requests=True`; EDGAR needs a `User-Agent`.

## 6. Tax Rule Change Tracker

- **Scenario:** A tax team wants a dated summary of recent budget, GST, or TDS updates.
- **Agent flow:** Search → open source pages → extract changes → write summary file.
- **Built-in tools:** `DuckDuckGoSearchRun`, `RequestsGetTool`, `WriteFileTool`
- **Custom tool:** None
- **Sample prompt:** "Summarize GST changes announced this quarter and save them."
- **Expected output:** `tax_updates.md` with date, change, and source link.
- **Learning outcome:** Search-then-read workflow, file output.

## 7. Expense Claim Auditor with Approval

- **Scenario:** Finance audits employee claims in mixed currencies and needs a manager sign-off before the report is final.
- **Agent flow:** Read claims → convert via Frankfurter → check policy → **pause for approval** → write report.
- **Built-in tools:** `RequestsGetTool`, `ReadFileTool`, `WriteFileTool`, `HumanInTheLoopMiddleware`
- **Custom tool:** `check_policy_limit`
- **Sample data:** `claims.json` with amount, currency, date, category
- **Sample prompt:** "Audit these claims in INR and flag policy breaches."
- **Expected output:** Audit report written only after human approval.
- **Learning outcome:** 1.x human-in-the-loop middleware (needs a checkpointer), approval gates.

## 8. Invoice Audit Report Generator

- **Scenario:** An accounts team wants a folder of invoices checked for GST math errors and bad GSTIN formats.
- **Agent flow:** List folder → read each invoice → validate → write exceptions report.
- **Built-in tools:** `FileManagementToolkit` (list, read, write; set `root_dir` to a sandbox folder)
- **Custom tools:** `validate_gst_math`, `validate_gstin`
- **Sample data:** 8 to 10 small invoice files, a few with deliberate errors
- **Sample prompt:** "Audit all invoices and list the exceptions."
- **Expected output:** `audit_report.md` grouped by error type.
- **Learning outcome:** File toolkit, mixing built-in and custom tools, validation reporting.

## 9. Portfolio News Digest

- **Scenario:** An investor wants a daily digest of news for a small watchlist, classified by impact.
- **Agent flow:** For each ticker → fetch news → classify positive, negative, or neutral → save digest.
- **Built-in tools:** `YahooFinanceNewsTool`, `WriteFileTool`
- **Custom tool:** None
- **Sample prompt:** "Digest today's news for TCS, INFY, HDFCBANK."
- **Expected output:** Digest file with a ticker, headline, impact label, and reason.
- **Learning outcome:** Structured output with `response_format`, a good first project.

## 10. Finance Research Scout

- **Scenario:** A student or analyst wants recent research on a quantitative finance topic, with unfamiliar terms explained.
- **Agent flow:** Search papers → compare → explain key terms → shortlist.
- **Built-in tools:** `ArxivQueryRun`, `WikipediaQueryRun`
- **Custom tool:** None
- **Sample prompt:** "Find recent papers on credit risk modelling and explain the key terms."
- **Expected output:** Shortlist with title, one-line finding, and glossary.
- **Learning outcome:** Multi-tool chaining with zero setup, a good first project.

---

## Built-in Tools Reference

| Tool | Package | Key Needed | Caveat |
|------|---------|-----------|--------|
| DuckDuckGoSearchRun | langchain-community, ddgs | No | May rate-limit |
| WikipediaQueryRun | langchain-community, wikipedia | No | None |
| ArxivQueryRun | langchain-community, arxiv | No | None |
| YahooFinanceNewsTool | langchain-community, yfinance | No | Unofficial source, may throttle |
| RequestsGetTool | langchain-community | No | Needs `allow_dangerous_requests=True` |
| SQLDatabaseToolkit | langchain-community, sqlalchemy | No | Use a demo DB |
| FileManagementToolkit | langchain-community | No | Restrict with `root_dir` |
| PythonREPLTool | langchain-experimental | No | Executes code; demo only |
| create_retriever_tool + BM25 | langchain, rank_bm25 | No | None |
| HumanInTheLoopMiddleware | langchain (1.x) | No | Needs a checkpointer |

## Concept Coverage

| Concept | Projects |
|---------|----------|
| Web search plus source reading | 1, 6 |
| Retrieval as a tool | 1 |
| SQL agent | 2 |
| Code execution | 3 |
| Live public data | 4, 5, 9, 10 |
| Large JSON navigation | 5 |
| File read/write | 3, 6, 7, 8, 9 |
| Human-in-the-loop | 7 |
| Structured output | 9 |

## Suggested Learning Order

| Level | Projects |
|-------|----------|
| Starter | 10, 9 |
| Intermediate | 2, 8, 1, 6 |
| Showcase | 7, 5 |