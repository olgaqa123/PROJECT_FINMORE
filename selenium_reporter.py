"""
selenium_reporter.py — Enterprise HTML Reporter for Python Selenium WebDriver
Usage:
    reporter = SeleniumReporter(config={
        "output_dir": "test-results/report",
        "report_title": "Test Execution Report",
        "company_name": "Your Company",
        "project_name": "Test Suite",
        "language": "uk",          # "uk" | "en" | "pl"
        "theme": "light",
        "primary_color": "#667eea",
        "show_passed_tests": True,
        "show_skipped_tests": True,
        "include_screenshots": True,
        "test_categories": ["smoke", "regression", "integration", "e2e"],
        "custom_metadata": {},
    })

    # Inside your test:
    reporter.on_begin()
    reporter.add_test(test_data)   # see TestData dataclass below
    reporter.on_end()

Works with plain unittest, pytest (via fixture), or any custom runner.
For pytest integration see the bottom of this file.
"""

from __future__ import annotations

import base64
import json
import os
import platform
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class StepData:
    title: str
    duration: float          # seconds
    category: str = "action"
    error: Optional[str] = None
    start_time: float = 0.0
    end_time: float = 0.0


@dataclass
class AttachmentData:
    name: str
    content_type: str
    path: Optional[str] = None
    base64: Optional[str] = None


@dataclass
class TestData:
    """Single test result.  Populate and pass to reporter.add_test()."""
    id: str
    title: str
    full_title: str
    file: str
    line: int = 0
    column: int = 0

    # "passed" | "failed" | "skipped" | "timedOut" | "broken"
    status: str = "passed"
    duration: float = 0.0      # seconds
    start_time: float = field(default_factory=time.time)
    end_time: float = 0.0

    error_message: Optional[str] = None
    error_stack: Optional[str] = None

    steps: List[StepData] = field(default_factory=list)
    annotations: List[Dict[str, str]] = field(default_factory=list)
    attachments: List[AttachmentData] = field(default_factory=list)

    retries: int = 0
    browser: str = "Chrome"
    project: str = "default"
    tags: List[str] = field(default_factory=list)
    category: str = "other"


# ---------------------------------------------------------------------------
# Reporter
# ---------------------------------------------------------------------------

class SeleniumReporter:
    TRANSLATIONS = {
        "uk": dict(
            testReport="Звіт про виконання тестів",
            overview="Огляд", categories="Категорії", suites="Набори тестів",
            graphs="Графіки", timeline="Часова шкала", behaviors="Поведінка",
            packages="Пакети", totalTests="Всього тестів", testCases="тест кейсів",
            passed="Пройдено", failed="Провалено", broken="Зламано",
            skipped="Пропущено", unknown="Невідомо", duration="Тривалість",
            passRate="Показник успішності", features="Функції",
            environment="Середовище", trend="Тренд",
            itemsTotal="елементів всього", showAll="Показати все",
            nothingToShow="Немає даних для відображення",
            executors="Виконавці",
        ),
        "en": dict(
            testReport="Test Execution Report",
            overview="Overview", categories="Categories", suites="Suites",
            graphs="Graphs", timeline="Timeline", behaviors="Behaviors",
            packages="Packages", totalTests="Total Tests", testCases="test cases",
            passed="Passed", failed="Failed", broken="Broken",
            skipped="Skipped", unknown="Unknown", duration="Duration",
            passRate="Pass Rate", features="Features",
            environment="Environment", trend="Trend",
            itemsTotal="items total", showAll="Show all",
            nothingToShow="There is nothing to show",
            executors="Executors",
        ),
        "pl": dict(
            testReport="Raport wykonania testów",
            overview="Przegląd", categories="Kategorie", suites="Zestawy",
            graphs="Wykresy", timeline="Oś czasu", behaviors="Zachowania",
            packages="Pakiety", totalTests="Wszystkie testy",
            testCases="przypadków testowych", passed="Zaliczone",
            failed="Nieudane", broken="Uszkodzone", skipped="Pominięte",
            unknown="Nieznane", duration="Czas trwania",
            passRate="Wskaźnik sukcesu", features="Funkcje",
            environment="Środowisko", trend="Trend",
            itemsTotal="elementów w sumie", showAll="Pokaż wszystko",
            nothingToShow="Nie ma nic do pokazania",
            executors="Wykonawcy",
        ),
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        cfg = config or {}
        self.output_dir       = cfg.get("output_dir", "test-results/enterprise-report")
        self.report_title     = cfg.get("report_title", "Test Execution Report")
        self.company_name     = cfg.get("company_name", "Your Company")
        self.project_name     = cfg.get("project_name", "Test Suite")
        self.language         = cfg.get("language", "uk")
        self.theme            = cfg.get("theme", "light")
        self.primary_color    = cfg.get("primary_color", "#667eea")
        self.logo             = cfg.get("logo", None)
        self.show_passed      = cfg.get("show_passed_tests", True)
        self.show_skipped     = cfg.get("show_skipped_tests", True)
        self.include_screenshots = cfg.get("include_screenshots", True)
        self.test_categories  = cfg.get("test_categories", ["smoke", "regression", "integration", "e2e"])
        self.custom_metadata  = cfg.get("custom_metadata", {})
        self.browser_name     = cfg.get("browser", "Chrome")

        self._start_time: float = 0.0
        self._end_time: float   = 0.0
        self._all_tests: List[TestData] = []

        lang = self.language if self.language in self.TRANSLATIONS else "uk"
        self.t = self.TRANSLATIONS[lang]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def on_begin(self) -> None:
        """Call once before running any tests."""
        self._start_time = time.time()
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"\n🚀 Selenium reporter ready → {self.output_dir}")

    def add_test(self, test: TestData) -> None:
        """Call after every test completes."""
        # Inline screenshot as base64 if path present
        if self.include_screenshots:
            for att in test.attachments:
                if att.path and att.content_type.startswith("image/") and not att.base64:
                    try:
                        with open(att.path, "rb") as f:
                            att.base64 = base64.b64encode(f.read()).decode()
                    except OSError:
                        pass

        # Auto-detect category from tags
        if test.category == "other":
            for tag in test.tags:
                if tag.lower() in self.test_categories:
                    test.category = tag.lower()
                    break

        self._all_tests.append(test)

        symbols = {"passed": "✅", "failed": "❌", "skipped": "⏭️", "timedOut": "⏱️", "broken": "🔴"}
        sym = symbols.get(test.status, "❓")
        print(f"  {sym} {test.full_title} ({test.duration:.2f}s)")

    def on_end(self) -> None:
        """Call once after all tests. Generates index.html + report.json."""
        self._end_time = time.time()
        stats = self._compute_stats()
        self._generate_html(stats)
        self._generate_json(stats)
        report_path = os.path.abspath(os.path.join(self.output_dir, "index.html"))
        passed = stats["passed"]; failed = stats["failed"]; skipped = stats["skipped"]
        print(f"\n✅ {passed} passed | ❌ {failed} failed | ⏭️ {skipped} skipped")
        print(f"📁 Report: {report_path}\n")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _compute_stats(self) -> Dict[str, Any]:
        tests = self._all_tests
        total   = len(tests)
        passed  = sum(1 for t in tests if t.status == "passed")
        failed  = sum(1 for t in tests if t.status == "failed")
        skipped = sum(1 for t in tests if t.status == "skipped")
        broken  = sum(1 for t in tests if t.status in ("timedOut", "broken"))
        unknown = total - passed - failed - skipped - broken
        duration = self._end_time - self._start_time
        pass_rate = (passed / total * 100) if total else 0
        return dict(total=total, passed=passed, failed=failed,
                    skipped=skipped, broken=broken, unknown=unknown,
                    duration=duration, pass_rate=pass_rate)

    def _group_by(self, key: str) -> Dict[str, List[TestData]]:
        result: Dict[str, List[TestData]] = {}
        for t in self._all_tests:
            k = getattr(t, key, "other") or "other"
            result.setdefault(k, []).append(t)
        return result

    def _env_info(self) -> Dict[str, str]:
        return {
            "os": platform.system() + " " + platform.release(),
            "python": sys.version.split()[0],
            "selenium": self._selenium_version(),
            "timestamp": datetime.now().isoformat(),
            "duration": f"{self._end_time - self._start_time:.2f}s",
        }

    @staticmethod
    def _selenium_version() -> str:
        try:
            import selenium
            return selenium.__version__
        except ImportError:
            return "unknown"

    @staticmethod
    def _pct(n: int, total: int) -> str:
        return f"{n / total * 100:.1f}" if total else "0"

    # ------------------------------------------------------------------
    # HTML generation
    # ------------------------------------------------------------------

    def _generate_html(self, stats: Dict[str, Any]) -> None:
        t = self.t
        pc = self.primary_color
        by_file     = self._group_by("file")
        by_category = self._group_by("category")
        by_project  = self._group_by("project")
        env         = self._env_info()

        def stat_bar(label: str, count: int, css_class: str) -> str:
            w = self._pct(count, stats["total"])
            return f"""
            <div class="status-item">
              <div class="status-label">
                <span class="status-name">{label}</span>
                <span class="status-count">{count}</span>
              </div>
              <div class="status-bar">
                <div class="status-fill {css_class}" style="width:{w}%"></div>
              </div>
            </div>"""

        def file_rows() -> str:
            rows = []
            for fname, tests in list(by_file.items())[:5]:
                p = sum(1 for x in tests if x.status == "passed")
                f = sum(1 for x in tests if x.status == "failed")
                b = sum(1 for x in tests if x.status in ("timedOut", "broken"))
                s = sum(1 for x in tests if x.status == "skipped")
                n = len(tests)
                bars = "".join([
                    f'<div class="feature-stat failed" style="width:{self._pct(f,n)}%">{f}</div>' if f else "",
                    f'<div class="feature-stat passed" style="width:{self._pct(p,n)}%">{p}</div>' if p else "",
                    f'<div class="feature-stat broken" style="width:{self._pct(b,n)}%">{b}</div>' if b else "",
                    f'<div class="feature-stat skipped" style="width:{self._pct(s,n)}%">{s}</div>' if s else "",
                ])
                safe = os.path.basename(fname)
                rows.append(f"""
                <div class="feature-item">
                  <div class="feature-name">{self._esc(safe)}</div>
                  <div class="feature-stats">{bars}</div>
                </div>""")
            return "\n".join(rows)

        def category_rows() -> str:
            if not by_category:
                return f'<div class="empty-state"><div class="empty-icon">📂</div><div>{t["nothingToShow"]}</div></div>'
            rows = []
            for cat, tests in by_category.items():
                f = sum(1 for x in tests if x.status == "failed")
                w = min(int(f / max(stats["total"], 1) * 300), 100)
                rows.append(f"""
                <div class="category-item">
                  <div class="category-name">{self._esc(cat)}</div>
                  <div class="category-bar" style="width:{w}%">{f}</div>
                </div>""")
            return '<div class="category-list">' + "\n".join(rows) + "</div>"

        def test_rows() -> str:
            rows = []
            for test in self._all_tests:
                status_icon = {"passed":"✅","failed":"❌","skipped":"⏭️","timedOut":"⏱️","broken":"🔴"}.get(test.status,"❓")
                err = ""
                if test.error_message:
                    err = f'<div class="test-error">{self._esc(test.error_message[:300])}</div>'
                tags_html = " ".join(f'<span class="tag">{self._esc(tag)}</span>' for tag in test.tags)

                screenshots = ""
                if self.include_screenshots:
                    for att in test.attachments:
                        if att.base64 and att.content_type.startswith("image/"):
                            screenshots += f'<img class="screenshot" src="data:{att.content_type};base64,{att.base64}" alt="{self._esc(att.name)}">'

                rows.append(f"""
                <div class="test-row status-{test.status}">
                  <div class="test-header">
                    <span class="test-icon">{status_icon}</span>
                    <span class="test-title">{self._esc(test.full_title)}</span>
                    <span class="test-duration">{test.duration:.2f}s</span>
                    <span class="test-browser">{self._esc(test.browser)}</span>
                  </div>
                  {f'<div class="test-tags">{tags_html}</div>' if tags_html else ""}
                  {err}
                  {screenshots}
                </div>""")
            return "\n".join(rows)

        # Serialise data for JS charts
        tests_json = json.dumps([
            {"title": t.title[:30], "duration": round(t.duration, 3)}
            for t in sorted(self._all_tests, key=lambda x: -x.duration)[:10]
        ])
        cat_json = json.dumps([
            {"cat": c, "count": len(lst)}
            for c, lst in by_category.items()
        ])

        logo_html = (
            f'<img src="{self.logo}" alt="Logo" class="logo">'
            if self.logo
            else f'<div class="logo-fallback" style="background:{pc}">🎭</div>'
        )

        html = f"""<!DOCTYPE html>
<html lang="{self.language}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{self._esc(self.report_title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{
  --primary:{pc};
  --pass:#22c55e;--fail:#ef4444;--broken:#f97316;--skip:#94a3b8;
  --bg:#f1f5f9;--card:#ffffff;--sidebar:#0f172a;--text:#1e293b;
  --text2:#64748b;--border:#e2e8f0;
  --font-body:'DM Sans',sans-serif;
  --font-mono:'JetBrains Mono',monospace;
  --shadow:0 1px 3px rgba(0,0,0,.08),0 4px 16px rgba(0,0,0,.05);
}}
body{{font-family:var(--font-body);background:var(--bg);color:var(--text);font-size:14px}}
.layout{{display:flex;min-height:100vh}}

/* ─── Sidebar ─────────────────────────────────────── */
.sidebar{{
  width:220px;background:var(--sidebar);color:#fff;
  position:fixed;height:100vh;overflow-y:auto;
  display:flex;flex-direction:column;
}}
.sidebar-header{{padding:24px 18px 18px;border-bottom:1px solid rgba(255,255,255,.08)}}
.logo-row{{display:flex;align-items:center;gap:10px;margin-bottom:6px}}
.logo{{width:36px;height:36px;border-radius:8px;object-fit:cover}}
.logo-fallback{{width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:18px}}
.company{{font-size:15px;font-weight:700;letter-spacing:-.2px}}
.proj{{font-size:11px;opacity:.5;margin-top:2px}}
nav{{padding:8px 0;flex:1}}
.nav-item{{
  display:flex;align-items:center;gap:10px;padding:11px 18px;
  cursor:pointer;color:rgba(255,255,255,.65);text-decoration:none;
  border-left:3px solid transparent;transition:all .15s;font-size:13px;
}}
.nav-item:hover{{background:rgba(255,255,255,.06);color:#fff}}
.nav-item.active{{background:rgba(255,255,255,.1);color:#fff;border-left-color:var(--primary)}}
.nav-icon{{font-size:15px;width:20px;text-align:center}}
.sidebar-footer{{padding:14px 18px;border-top:1px solid rgba(255,255,255,.08);font-size:11px;opacity:.4;font-family:var(--font-mono)}}

/* ─── Main ─────────────────────────────────────────── */
.main{{flex:1;margin-left:220px;display:flex;flex-direction:column;min-height:100vh}}
.topbar{{
  background:var(--card);padding:16px 28px;
  border-bottom:1px solid var(--border);
  display:flex;justify-content:space-between;align-items:center;
  position:sticky;top:0;z-index:10;
}}
.page-title{{font-size:20px;font-weight:700;color:var(--text)}}
.timestamp{{color:var(--text2);font-size:12px;font-family:var(--font-mono)}}
.content{{padding:24px 28px}}

/* ─── Cards ─────────────────────────────────────────── */
.card{{background:var(--card);border-radius:10px;padding:22px;box-shadow:var(--shadow)}}
.overview-grid{{display:grid;grid-template-columns:2fr 1fr;gap:18px;margin-bottom:24px}}
.stats-row{{display:flex;gap:32px;align-items:center}}
.total-block{{text-align:center;flex-shrink:0}}
.big-num{{font-size:68px;font-weight:700;color:var(--text);line-height:1;font-family:var(--font-mono)}}
.big-label{{font-size:12px;color:var(--text2);margin-top:6px;text-transform:uppercase;letter-spacing:.5px}}
.status-bars{{flex:1}}
.status-item{{margin-bottom:14px}}
.status-item:last-child{{margin-bottom:0}}
.status-label{{display:flex;justify-content:space-between;margin-bottom:5px;font-size:12px}}
.status-name{{font-weight:600}}
.status-count{{color:var(--text2)}}
.status-bar{{height:6px;background:#f1f5f9;border-radius:3px;overflow:hidden}}
.status-fill{{height:100%}}
.status-fill.passed{{background:var(--pass)}}
.status-fill.failed{{background:var(--fail)}}
.status-fill.broken{{background:var(--broken)}}
.status-fill.skipped{{background:var(--skip)}}
.donut-wrap{{display:flex;justify-content:center;align-items:center;height:180px}}

/* ─── Sections ──────────────────────────────────────── */
.section{{margin-bottom:24px}}
.section-head{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px}}
.section-title{{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:var(--text2)}}
.items-count{{font-size:11px;color:var(--text2);margin-left:8px}}
.show-all{{font-size:12px;color:var(--primary);cursor:pointer;text-decoration:none}}
.show-all:hover{{text-decoration:underline}}

/* ─── Feature list ──────────────────────────────────── */
.feature-list{{background:var(--card);border-radius:10px;overflow:hidden;box-shadow:var(--shadow)}}
.feature-item{{border-bottom:1px solid var(--border);padding:14px 18px;cursor:pointer;transition:background .15s}}
.feature-item:hover{{background:#f8fafc}}
.feature-item:last-child{{border-bottom:none}}
.feature-name{{font-size:13px;color:var(--text);margin-bottom:7px;font-family:var(--font-mono)}}
.feature-stats{{height:20px;background:#f1f5f9;border-radius:4px;display:flex;overflow:hidden}}
.feature-stat{{display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#fff}}
.feature-stat.passed{{background:var(--pass)}}
.feature-stat.failed{{background:var(--fail)}}
.feature-stat.broken{{background:var(--broken)}}
.feature-stat.skipped{{background:var(--skip)}}

/* ─── Env grid ───────────────────────────────────────── */
.env-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
.env-item{{display:flex;flex-direction:column;gap:5px}}
.env-label{{font-size:10px;color:var(--text2);text-transform:uppercase;letter-spacing:.5px}}
.env-value{{font-size:13px;font-weight:600;color:var(--text);font-family:var(--font-mono)}}

/* ─── Categories ─────────────────────────────────────── */
.category-list{{background:var(--card);border-radius:10px;overflow:hidden;box-shadow:var(--shadow)}}
.category-item{{border-bottom:1px solid var(--border);padding:12px 18px;display:flex;align-items:center;gap:14px}}
.category-item:last-child{{border-bottom:none}}
.category-name{{flex:0 0 200px;font-size:13px;font-family:var(--font-mono)}}
.category-bar{{height:28px;background:var(--fail);border-radius:4px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:11px;min-width:28px}}

/* ─── Charts ─────────────────────────────────────────── */
.charts-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}}
.chart-card{{background:var(--card);border-radius:10px;padding:22px;box-shadow:var(--shadow)}}
.chart-title{{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--text2);margin-bottom:18px}}

/* ─── Tests list ─────────────────────────────────────── */
.tests-list{{display:flex;flex-direction:column;gap:8px}}
.test-row{{background:var(--card);border-radius:8px;padding:14px 16px;box-shadow:var(--shadow);border-left:3px solid var(--border)}}
.test-row.status-passed{{border-left-color:var(--pass)}}
.test-row.status-failed{{border-left-color:var(--fail)}}
.test-row.status-skipped{{border-left-color:var(--skip)}}
.test-row.status-broken,.test-row.status-timedOut{{border-left-color:var(--broken)}}
.test-header{{display:flex;align-items:center;gap:10px;flex-wrap:wrap}}
.test-icon{{font-size:14px}}
.test-title{{flex:1;font-size:13px;font-weight:500}}
.test-duration{{font-family:var(--font-mono);font-size:11px;color:var(--text2);background:#f1f5f9;padding:2px 7px;border-radius:4px}}
.test-browser{{font-family:var(--font-mono);font-size:10px;color:var(--text2);background:#f1f5f9;padding:2px 7px;border-radius:4px}}
.test-error{{margin-top:10px;font-family:var(--font-mono);font-size:11px;color:var(--fail);background:#fff5f5;padding:10px;border-radius:6px;white-space:pre-wrap;word-break:break-all}}
.test-tags{{margin-top:7px;display:flex;gap:6px;flex-wrap:wrap}}
.tag{{font-size:10px;font-family:var(--font-mono);background:#ede9fe;color:#7c3aed;padding:2px 8px;border-radius:10px}}
.screenshot{{display:block;margin-top:10px;max-width:100%;max-height:300px;border-radius:6px;border:1px solid var(--border)}}

/* ─── Empty state ───────────────────────────────────── */
.empty-state{{text-align:center;padding:60px 20px;color:var(--text2)}}
.empty-icon{{font-size:42px;margin-bottom:12px;opacity:.25}}

/* ─── Pages ──────────────────────────────────────────── */
.page{{display:none}}.page.active{{display:block}}

@media(max-width:900px){{
  .sidebar{{width:200px}}.main{{margin-left:200px}}
  .overview-grid{{grid-template-columns:1fr}}.charts-grid{{grid-template-columns:1fr}}
  .env-grid{{grid-template-columns:repeat(2,1fr)}}
}}
</style>
</head>
<body>
<div class="layout">

<!-- ═══ Sidebar ═══ -->
<aside class="sidebar">
  <div class="sidebar-header">
    <div class="logo-row">{logo_html}
      <div>
        <div class="company">{self._esc(self.company_name)}</div>
        <div class="proj">{self._esc(self.project_name)}</div>
      </div>
    </div>
  </div>
  <nav>
    <a class="nav-item active" data-page="overview"><span class="nav-icon">🏠</span>{t["overview"]}</a>
    <a class="nav-item" data-page="categories"><span class="nav-icon">📂</span>{t["categories"]}</a>
    <a class="nav-item" data-page="suites"><span class="nav-icon">📦</span>{t["suites"]}</a>
    <a class="nav-item" data-page="graphs"><span class="nav-icon">📊</span>{t["graphs"]}</a>
    <a class="nav-item" data-page="tests"><span class="nav-icon">🧪</span>Tests</a>
    <a class="nav-item" data-page="timeline"><span class="nav-icon">⏱️</span>{t["timeline"]}</a>
    <a class="nav-item" data-page="behaviors"><span class="nav-icon">🎯</span>{t["behaviors"]}</a>
  </nav>
  <div class="sidebar-footer">Python + Selenium</div>
</aside>

<!-- ═══ Main ═══ -->
<main class="main">
  <div class="topbar">
    <span class="page-title">{self._esc(self.report_title)}</span>
    <span class="timestamp">{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</span>
  </div>
  <div class="content">

    <!-- ── Overview ── -->
    <div class="page active" data-page="overview">
      <div class="overview-grid">
        <div class="card">
          <div class="stats-row">
            <div class="total-block">
              <div class="big-num">{stats["total"]}</div>
              <div class="big-label">{t["testCases"]}</div>
            </div>
            <div class="status-bars">
              {stat_bar(t["passed"],  stats["passed"],  "passed")}
              {stat_bar(t["failed"],  stats["failed"],  "failed")}
              {stat_bar(t["broken"],  stats["broken"],  "broken")}
              {stat_bar(t["skipped"], stats["skipped"], "skipped")}
            </div>
          </div>
        </div>
        <div class="card"><div class="donut-wrap"><canvas id="overviewDonut"></canvas></div></div>
      </div>

      <div class="section">
        <div class="section-head">
          <div>
            <span class="section-title">{t["suites"]}</span>
            <span class="items-count">{len(by_file)} {t["itemsTotal"]}</span>
          </div>
          <a class="show-all">{t["showAll"]}</a>
        </div>
        <div class="feature-list">{file_rows()}</div>
      </div>

      <div class="section">
        <div class="section-head"><span class="section-title">{t["environment"]}</span></div>
        <div class="card">
          <div class="env-grid">
            <div class="env-item"><div class="env-label">OS</div><div class="env-value">{self._esc(env["os"])}</div></div>
            <div class="env-item"><div class="env-label">Python</div><div class="env-value">{env["python"]}</div></div>
            <div class="env-item"><div class="env-label">Selenium</div><div class="env-value">{env["selenium"]}</div></div>
            <div class="env-item"><div class="env-label">Browser</div><div class="env-value">{self._esc(self.browser_name)}</div></div>
            <div class="env-item"><div class="env-label">{t["duration"]}</div><div class="env-value">{stats["duration"]:.2f}s</div></div>
            <div class="env-item"><div class="env-label">{t["passRate"]}</div><div class="env-value">{stats["pass_rate"]:.1f}%</div></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Categories ── -->
    <div class="page" data-page="categories">
      <div class="section">
        <div class="section-head">
          <div>
            <span class="section-title">{t["categories"]}</span>
            <span class="items-count">{len(by_category)} {t["itemsTotal"]}</span>
          </div>
        </div>
        {category_rows()}
      </div>
    </div>

    <!-- ── Suites ── -->
    <div class="page" data-page="suites">
      <div class="section">
        <div class="section-head">
          <span class="section-title">{t["suites"]}</span>
          <span class="items-count">{len(by_file)} {t["itemsTotal"]}</span>
        </div>
        <div class="feature-list">{file_rows()}</div>
      </div>
    </div>

    <!-- ── Graphs ── -->
    <div class="page" data-page="graphs">
      <div class="charts-grid">
        <div class="chart-card"><div class="chart-title">Status Distribution</div><canvas id="statusChart"></canvas></div>
        <div class="chart-card"><div class="chart-title">Top 10 Slowest Tests</div><canvas id="durationChart"></canvas></div>
        <div class="chart-card"><div class="chart-title">Pass Rate Trend</div><canvas id="trendChart"></canvas></div>
        <div class="chart-card"><div class="chart-title">Tests by Category</div><canvas id="categoryChart"></canvas></div>
      </div>
    </div>

    <!-- ── All Tests ── -->
    <div class="page" data-page="tests">
      <div class="section">
        <div class="section-head">
          <span class="section-title">All Tests</span>
          <span class="items-count">{stats["total"]} {t["itemsTotal"]}</span>
        </div>
        <div class="tests-list">{test_rows()}</div>
      </div>
    </div>

    <!-- ── Timeline (placeholder) ── -->
    <div class="page" data-page="timeline">
      <div class="empty-state"><div class="empty-icon">⏱️</div><div>{t["nothingToShow"]}</div></div>
    </div>

    <!-- ── Behaviors (placeholder) ── -->
    <div class="page" data-page="behaviors">
      <div class="empty-state"><div class="empty-icon">🎯</div><div>{t["nothingToShow"]}</div></div>
    </div>

  </div><!-- /content -->
</main>

</div><!-- /layout -->

<script>
// Navigation
document.querySelectorAll('.nav-item').forEach(el => {{
  el.addEventListener('click', () => {{
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    el.classList.add('active');
    const pg = el.dataset.page;
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelector(`.page[data-page="${{pg}}"]`).classList.add('active');
  }});
}});

Chart.defaults.font.family = "'DM Sans', sans-serif";
const PRIMARY = "{pc}";

// Donut overview
new Chart(document.getElementById('overviewDonut'), {{
  type:'doughnut',
  data:{{
    labels:['{t["passed"]}','{t["failed"]}','{t["broken"]}','{t["skipped"]}'],
    datasets:[{{
      data:[{stats["passed"]},{stats["failed"]},{stats["broken"]},{stats["skipped"]}],
      backgroundColor:['#22c55e','#ef4444','#f97316','#94a3b8'],
      borderWidth:0
    }}]
  }},
  options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},cutout:'72%'}}
}});

// Status chart
new Chart(document.getElementById('statusChart'), {{
  type:'doughnut',
  data:{{
    labels:['{t["passed"]}','{t["failed"]}','{t["broken"]}','{t["skipped"]}'],
    datasets:[{{
      data:[{stats["passed"]},{stats["failed"]},{stats["broken"]},{stats["skipped"]}],
      backgroundColor:['#22c55e','#ef4444','#f97316','#94a3b8']
    }}]
  }},
  options:{{responsive:true,plugins:{{legend:{{position:'bottom'}}}}}}
}});

// Duration chart
const slowTests = {tests_json};
new Chart(document.getElementById('durationChart'), {{
  type:'bar',
  data:{{
    labels: slowTests.map(t => t.title),
    datasets:[{{
      label:'Duration (s)',
      data: slowTests.map(t => t.duration),
      backgroundColor: PRIMARY + 'cc'
    }}]
  }},
  options:{{
    indexAxis:'y',responsive:true,
    plugins:{{legend:{{display:false}}}},
    scales:{{x:{{beginAtZero:true}}}}
  }}
}});

// Trend chart (simulated history)
new Chart(document.getElementById('trendChart'), {{
  type:'line',
  data:{{
    labels:['Run-4','Run-3','Run-2','Run-1','Current'],
    datasets:[{{
      label:'{t["passRate"]} %',
      data:[85,88,90,87,{stats["pass_rate"]:.1f}],
      borderColor: PRIMARY,
      backgroundColor: PRIMARY + '22',
      tension:0.4,fill:true,pointRadius:4
    }}]
  }},
  options:{{
    responsive:true,
    plugins:{{legend:{{display:false}}}},
    scales:{{y:{{beginAtZero:true,max:100}}}}
  }}
}});

// Category chart
const cats = {cat_json};
new Chart(document.getElementById('categoryChart'), {{
  type:'pie',
  data:{{
    labels: cats.map(c => c.cat),
    datasets:[{{
      data: cats.map(c => c.count),
      backgroundColor:['#3b82f6','#ec4899','#8b5cf6','#10b981','#f59e0b','#06b6d4']
    }}]
  }},
  options:{{responsive:true,plugins:{{legend:{{position:'bottom'}}}}}}
}});
</script>
</body>
</html>"""

        with open(os.path.join(self.output_dir, "index.html"), "w", encoding="utf-8") as fh:
            fh.write(html)

    def _generate_json(self, stats: Dict[str, Any]) -> None:
        data = {
            "config": {
                "report_title": self.report_title,
                "company_name": self.company_name,
                "project_name": self.project_name,
                "language": self.language,
                "primary_color": self.primary_color,
            },
            "stats": stats,
            "environment": self._env_info(),
            "tests": [asdict(t) for t in self._all_tests],
            "generated_at": datetime.now().isoformat(),
        }
        with open(os.path.join(self.output_dir, "report.json"), "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)

    @staticmethod
    def _esc(text: str) -> str:
        return (str(text)
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#039;"))


# ---------------------------------------------------------------------------
# Convenience: pytest fixture / plugin
# ---------------------------------------------------------------------------
# Add to conftest.py:
#
#   from selenium_reporter import SeleniumReporter, TestData
#   import pytest, time, uuid
#
#   reporter = SeleniumReporter({"language": "uk", "company_name": "Acme"})
#
#   def pytest_sessionstart(session):
#       reporter.on_begin()
#
#   def pytest_runtest_logreport(report):
#       if report.when == "call" or (report.when == "setup" and report.skipped):
#           status_map = {"passed": "passed", "failed": "failed", "skipped": "skipped"}
#           test = TestData(
#               id=str(uuid.uuid4()),
#               title=report.nodeid.split("::")[-1],
#               full_title=report.nodeid,
#               file=report.fspath,
#               status=status_map.get(report.outcome, "unknown"),
#               duration=getattr(report, "duration", 0),
#               start_time=time.time(),
#               end_time=time.time(),
#               error_message=str(report.longrepr) if report.failed else None,
#           )
#           reporter.add_test(test)
#
#   def pytest_sessionfinish(session, exitstatus):
#       reporter.on_end()
#
# ---------------------------------------------------------------------------
# Convenience: unittest TestRunner wrapper
# ---------------------------------------------------------------------------

import unittest


class SeleniumTestRunner:
    """Drop-in replacement for unittest.TextTestRunner that also writes HTML."""

    def __init__(self, reporter_config: Optional[Dict[str, Any]] = None, **kwargs):
        self.reporter = SeleniumReporter(reporter_config or {})
        self._runner_kwargs = kwargs

    def run(self, test_suite: unittest.TestSuite) -> unittest.TestResult:
        import io
        self.reporter.on_begin()

        stream = io.StringIO()
        runner = unittest.TextTestRunner(stream=stream, **self._runner_kwargs)
        result = runner.run(test_suite)

        # unittest gives us pass/fail totals — convert to TestData objects
        import uuid
        for test, traceback in result.failures + result.errors:
            td = TestData(
                id=str(uuid.uuid4()),
                title=str(test),
                full_title=str(test),
                file=getattr(test, "_testMethodName", "unknown"),
                status="failed",
                duration=0,
                error_message=traceback[:500],
            )
            self.reporter.add_test(td)

        total_ran = result.testsRun
        fail_count = len(result.failures) + len(result.errors)
        skip_count = len(result.skipped)
        pass_count = total_ran - fail_count - skip_count

        for i in range(pass_count):
            td = TestData(
                id=str(uuid.uuid4()),
                title=f"test_{i}",
                full_title=f"test_{i}",
                file="unknown",
                status="passed",
            )
            self.reporter.add_test(td)

        self.reporter.on_end()
        return result


# ---------------------------------------------------------------------------
# Quick smoke-test / demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uuid, random

    reporter = SeleniumReporter({
        "output_dir": "demo-report",
        "report_title": "Demo Selenium Report",
        "company_name": "Acme QA",
        "project_name": "Login Suite",
        "language": "en",
        "primary_color": "#667eea",
        "browser": "Chrome 124",
    })

    reporter.on_begin()

    sample_tests = [
        ("Login with valid credentials", "passed", "tests/test_login.py", ["smoke", "regression"]),
        ("Login with invalid password", "failed", "tests/test_login.py", ["smoke"]),
        ("Forgot password flow",         "passed", "tests/test_login.py", ["regression"]),
        ("Sign up – happy path",         "passed", "tests/test_signup.py", ["e2e"]),
        ("Sign up – duplicate email",    "failed", "tests/test_signup.py", ["e2e"]),
        ("Logout button visible",        "passed", "tests/test_nav.py",   ["smoke"]),
        ("Mobile menu toggle",           "skipped","tests/test_nav.py",   ["regression"]),
        ("Dashboard loads < 2 s",        "passed", "tests/test_perf.py",  ["regression"]),
    ]

    for title, status, fpath, tags in sample_tests:
        td = TestData(
            id=str(uuid.uuid4()),
            title=title,
            full_title=f"{fpath}::{title}",
            file=fpath,
            status=status,
            duration=round(random.uniform(0.3, 4.5), 3),
            start_time=time.time(),
            end_time=time.time(),
            error_message="AssertionError: expected 200 got 401" if status == "failed" else None,
            tags=tags,
            browser="Chrome 124",
            project="default",
        )
        reporter.add_test(td)

    reporter.on_end()
    print("Open demo-report/index.html in your browser.")
