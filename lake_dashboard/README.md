# Lake monitoring prototype: dashboard

Read-only dashboard for the four-channel lake prototype (pH, water temperature, TDS/EC, water level), built to the *Lake Monitoring System: Sensor Engineering Review* of 12 October 2026.

**The dashboard ships with no data.** It reads everything (sensors, controllers, readings, calibrations, flags) from a read-only data API backed by MySQL. Until that API is configured it shows "Not connected". The API contract, including how MySQL types are handled, is in [dashboard/API.md](dashboard/API.md).

## Requirements

- Node.js 20 or later (developed on Node 26). No npm dependencies to install.

## Run it

The folder name ends with a space (`lake_monitoring `), so quote the path:

```sh
cd "/Users/nawdddep/Desktop/lake_monitoring "
npm start          # serves the dashboard on http://127.0.0.1:8080/
npm test           # rendering and guardrail tests (use test fixtures only)

node dashboard/serve.mjs --port 9000 --host 127.0.0.1   # other port or host
```

## Connect the data API

Edit `dashboard/config.json`:

```json
{ "apiBase": "http://localhost:3000/api" }
```

Then restart `npm start` (the server adds the API origin to the page's Content-Security-Policy) and reload the page. The dashboard calls `GET {apiBase}/snapshot?from=…&to=…`.

## Configuration: `dashboard/config.json`

| Key | Default | Meaning |
|---|---|---|
| `apiBase` | `null` | Data API base URL, e.g. `/api` or `http://localhost:3000/api`. `null` means not connected. |
| `loginPath` | `null` | Where to send the browser when the API returns 401 |
| `refreshSeconds` | `60` | Refresh interval |
| `requestTimeoutSeconds` | `15` | How long to wait for the API before showing "Could not reach the data API" |
| `timezone` / `timezoneLabel` | `Asia/Kolkata` / `IST` | Display zone. Storage and export stay UTC. |
| `samplingMinutes` | `10` | Expected sampling interval (vendor default; actual is unconfirmed) |
| `gapFactor` | `2.5` | A gap is silence longer than `gapFactor × samplingMinutes` |
| `defaultRange` | `7d` | Initial time range |

No credentials belong in this file. It is served to the browser.

## Pages

| # | Page | What it shows |
|---|---|---|
| 1 | Overview | Four tiles with last value, age, all quality flags beside the number, and a 24 h sparkline. Attention banner, evidence counts, measurement-cycle summary, and the scope sentence. |
| 2 | Trends | 1 h to 90 days. Raw and corrected series, calibration markers, gaps as hatched bands, flag strip. Bad-severity points are left out of lines and listed under each chart. |
| 3 | Water chemistry | EC raw and compensated, *Estimated TDS (from conductivity)* with its factor, and water temperature on one time axis. A table gives the temperature reading and its age for every compensation. |
| 4 | Lake level | Distance and elevation vs datum, the configuration in force, and "No datum configured: distance only" when absent. |
| 5 | Calibration and QA | Latest calibration per sensor and days since it, plus the acceptance-test grid. |
| 6 | Data quality | Cycle completeness, clock behaviour per controller, longest gaps, and flag counts per sensor and day. |
| 7 | Registry and evidence | Every sensor with model, evidence status, vendor claim beside plausibility limits, and unknown fields. Sensors not installed are marked; the not-measured list is included. |
| 8 | Export | CSV with raw and corrected values, units, calibration version, flags and `is_synthetic`. |

Clicking any underlined number opens its source row (reading ID, sensor, timestamp, calibration version). Hovering a chart shows every series at that time, with its flags.

## Layout

```
dashboard/
  index.html, css/app.css, config.json, serve.mjs, API.md
  js/app.js               routing, refresh, hover, source dialog, CSV download
  js/data.js              data API client
  js/lib/                 format, model (incl. MySQL type handling), chart (SVG), source-row helpers
  js/pages/               one module per page; render(model, ui) returns HTML
tests/dashboard.test.mjs
tests/fixtures/seed.json  test input only (planned seed rows); not served
ASSUMPTIONS.md
```

See [ASSUMPTIONS.md](ASSUMPTIONS.md) for what is unverified and the decisions taken on defaults.
