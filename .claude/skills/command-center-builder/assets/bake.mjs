#!/usr/bin/env node
/*
 * Command Center — data baker (REFERENCE IMPLEMENTATION: every <PLACEHOLDER> below is
 * remapped to the student's own base — see PLACEHOLDERS.md; pull their schema fresh).
 * Runs at build time (Cloudflare, or locally). Reads the student's Airtable
 * base with a read-only PAT from env, aggregates, and writes data.json next to
 * index.html. The token is NEVER written into the output — only computed numbers are.
 *
 * Env: AIRTABLE_TOKEN  (Airtable Personal Access Token, scope data.records:read on YOUR base only)
 * Run: node command-center/bake.mjs
 */
import { writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const BASE = "<YOUR_AIRTABLE_BASE_ID>"; // starts with app — from the base URL, airtable.com/<this>/...
const TOKEN = process.env.AIRTABLE_TOKEN;
if (!TOKEN) { console.error("Missing AIRTABLE_TOKEN env var"); process.exit(1); }

const TABLES = {
  units:    { id: "<TBL_UNITS>", f: { occ:"<FLD_UNITS_OCC>", rent:"<FLD_UNITS_RENT>", arch:"<FLD_UNITS_ARCH>" } },
  payments: { id: "<TBL_RENT_PAYMENTS>", f: { status:"<FLD_RENT_PAYMENTS_STATUS>", due:"<FLD_RENT_PAYMENTS_DUE>", paid:"<FLD_RENT_PAYMENTS_PAID>", datePaid:"<FLD_RENT_PAYMENTS_DATEPAID>", tenant:"<FLD_RENT_PAYMENTS_TENANT>" } },
  leases:   { id: "<TBL_LEASES>", f: { status:"<FLD_LEASES_STATUS>", exp:"<FLD_LEASES_EXP>", ltrId:"<FLD_LEASES_LTRID>", plans:"<FLD_LEASES_PLANS>", arch:"<FLD_LEASES_ARCH>" } },
  tasks:    { id: "<TBL_TASKS>", f: { title:"<FLD_TASKS_TITLE>", status:"<FLD_TASKS_STATUS>", due:"<FLD_TASKS_DUE>", pl:"<FLD_TASKS_PL>", imm:"<FLD_TASKS_IMM>" } },
  mail:     { id: "<TBL_MAIL>", f: { received:"<FLD_MAIL_RECEIVED>", status:"<FLD_MAIL_STATUS>" } },
  maint:    { id: "<TBL_MAINTENANCE>", f: { status:"<FLD_MAINTENANCE_STATUS>", completed:"<FLD_MAINTENANCE_COMPLETED>", desc:"<FLD_MAINTENANCE_DESC>" } },
  kpi:      { id: "<TBL_MONTHLY_KPI>", f: { month:"<FLD_MONTHLY_KPI_MONTH>", occ:"<FLD_MONTHLY_KPI_OCC>", coll:"<FLD_MONTHLY_KPI_COLL>", occU:"<FLD_MONTHLY_KPI_OCCU>", vacU:"<FLD_MONTHLY_KPI_VACU>", tot:"<FLD_MONTHLY_KPI_TOT>", roll:"<FLD_MONTHLY_KPI_ROLL>", due:"<FLD_MONTHLY_KPI_DUE>", col:"<FLD_MONTHLY_KPI_COL>", notes:"<FLD_MONTHLY_KPI_NOTES>" } },
};

async function fetchAll(tableId) {
  const out = [];
  let offset;
  do {
    const url = new URL(`https://api.airtable.com/v0/${BASE}/${tableId}`);
    url.searchParams.set("pageSize", "100");
    url.searchParams.set("returnFieldsByFieldId", "true");
    if (offset) url.searchParams.set("offset", offset);
    const res = await fetch(url, { headers: { Authorization: `Bearer ${TOKEN}` } });
    if (!res.ok) throw new Error(`Airtable ${tableId} ${res.status}: ${await res.text()}`);
    const j = await res.json();
    out.push(...j.records);
    offset = j.offset;
  } while (offset);
  return out;
}

// ---- helpers ----
const sel = v => v == null ? null : (typeof v === "string" ? v : (v.name ?? null));
const num = v => { if (Array.isArray(v)) v = v[0]; return Number(v) || 0; };
const isArchived = v => v != null && JSON.stringify(v).includes('"Yes"') || v === "Yes";
const iso = d => d.toISOString().slice(0, 10);
const addDays = (d, n) => { const x = new Date(d); x.setUTCDate(x.getUTCDate() + n); return x; };

// "today" in America/New_York
const nowET = new Date(new Date().toLocaleString("en-US", { timeZone: "America/New_York" }));
const TODAY = iso(nowET);
const dow = nowET.getDay(); // Sun=0 Mon=1
const WSTART = iso(addDays(new Date(TODAY + "T00:00:00Z"), dow === 1 ? -3 : -1));
const IN90 = iso(addDays(new Date(TODAY + "T00:00:00Z"), 90));

function fld(rec, table, key) { return rec.fields[TABLES[table].f[key]]; }

const [units, payments, leases, tasks, mail, maint, kpi] = await Promise.all(
  ["units","payments","leases","tasks","mail","maint","kpi"].map(k => fetchAll(TABLES[k].id))
);

// ---- occupancy (exclude archived-from-property and NA) ----
let occupied = 0, vacant = 0, active = 0, rentroll = 0;
for (const r of units) {
  if (isArchived(fld(r,"units","arch"))) continue;
  const occ = sel(fld(r,"units","occ"));
  if (occ !== "Occupied" && occ !== "Vacant") continue;
  active++;
  if (occ === "Occupied") { occupied++; rentroll += num(fld(r,"units","rent")); }
  else vacant++;
}
const occRate = active ? occupied / active : null;

// ---- overdue balance ----
let overdue = 0;
for (const r of payments) {
  const st = sel(fld(r,"payments","status"));
  if (st === "Delinquent" || st === "Partial") overdue += num(fld(r,"payments","due")) - num(fld(r,"payments","paid"));
}
if (overdue < 0) overdue = 0;

// ---- lease expirations next 90d (current leases) ----
const leaseRows = [];
for (const r of leases) {
  if (sel(fld(r,"leases","status")) !== "Current") continue;
  const exp = fld(r,"leases","exp");
  if (!exp || exp < TODAY || exp > IN90) continue;
  const days = Math.round((Date.parse(exp+"T00:00:00Z") - Date.parse(TODAY+"T00:00:00Z")) / 86400000);
  const name = (fld(r,"leases","ltrId") || "").toString().replace(/\s+/g," ").trim() || "(lease)";
  leaseRows.push({ id: name, expiration: exp, days, intention: sel(fld(r,"leases","plans")) });
}
leaseRows.sort((a,b)=>a.expiration.localeCompare(b.expiration));

// ---- wins since window ----
const wins = [];
for (const r of leases) if (sel(fld(r,"leases","status"))==="Current" && r.createdTime && r.createdTime.slice(0,10) >= WSTART)
  wins.push({ icon:"[+]", text:`New lease: ${(fld(r,"leases","ltrId")||"").toString().replace(/\s+/g," ").trim()}` });
for (const r of payments) if (sel(fld(r,"payments","status"))==="Paid" && fld(r,"payments","datePaid") && fld(r,"payments","datePaid") >= WSTART)
  wins.push({ icon:"[$]", text:`Rent received: ${fld(r,"payments","tenant")||"tenant"} ${fld(r,"payments","paid")?"$"+num(fld(r,"payments","paid")).toLocaleString():""}`.trim() });
for (const r of maint) if (sel(fld(r,"maint","status"))==="Completed" && fld(r,"maint","completed") && fld(r,"maint","completed") >= WSTART)
  wins.push({ icon:"[OK]", text:`Maintenance resolved: ${fld(r,"maint","desc")||"item"}` });
const winsTotal = wins.length;

// ---- mail ----
let mailNew=0, mailReview=0;
for (const r of mail) {
  const rec = fld(r,"mail","received");
  if (rec && rec >= WSTART) mailNew++;
  const st = sel(fld(r,"mail","status"));
  if (st === "Review" || st === "Needs Review") mailReview++;
}

// ---- maintenance open ----
const maintOpen = maint.filter(r => sel(fld(r,"maint","status")) === "Open").length;

// ---- tasks (attention-scoped) ----
const DONE = ["complete","archived","done"];
let openCount = 0; const attention = [];
for (const r of tasks) {
  const st = (sel(fld(r,"tasks","status")) || "");
  const low = st.toLowerCase();
  if (DONE.some(m => low.includes(m))) continue;
  if (low.includes("parking lot")) continue;
  openCount++;
  const due = fld(r,"tasks","due") || null;
  const pl = fld(r,"tasks","pl");
  const imm = !!fld(r,"tasks","imm");
  if (imm || due || (pl != null && pl < 100))
    attention.push({ title: fld(r,"tasks","title") || "(untitled)", due, pl: (pl != null ? pl : 999), imm });
}
const rank = t => [ t.imm?0:1, !t.due?3:(t.due<TODAY?0:(t.due===TODAY?1:2)), t.due||"9999", t.pl ];
attention.sort((a,b)=>{ const ra=rank(a),rb=rank(b); for(let i=0;i<ra.length;i++){ if(ra[i]<rb[i])return -1; if(ra[i]>rb[i])return 1; } return 0; });
const taskRows = attention.slice(0,6).map(t => ({ title:t.title, due:t.due, priority: t.imm?"Immediate":(t.pl<100?("P"+t.pl):"") }));

// ---- trends (kpi) ----
const months = kpi.map(r => ({
  month: fld(r,"kpi","month") || null,
  occ: fld(r,"kpi","occ") ?? null, coll: fld(r,"kpi","coll") ?? null,
  due: fld(r,"kpi","due"), col: fld(r,"kpi","col"), notes: fld(r,"kpi","notes") || "",
})).filter(m => m.month && !/placeholder|seed/i.test(m.notes||"")).sort((a,b)=>a.month.localeCompare(b.month));
// Placeholder/seed months are excluded so only real data charts. Rent & collection
// charts are omitted from the payload entirely until real payment data is captured.
const withOcc = months.filter(m=>m.occ!=null).map(m=>({m:m.month, v:+(m.occ*100).toFixed(1)}));

const stamp = nowET.toLocaleString("en-US",{weekday:"long",month:"short",day:"numeric",year:"numeric",hour:"numeric",minute:"2-digit"}) + " ET";
const PAYLOAD = {
  snapshot: new Date().toISOString(),
  snapLabel: stamp,
  windowStart: WSTART,
  daily: {
    kpis: { vacant, occupancyRate: occRate, overdueBalance: overdue, leasesExpiring90: leaseRows.length },
    wins: wins.slice(0,6), winsTotal,
    mail: { newItems: mailNew, needsReview: mailReview },
    maintOpen,
    tasks: taskRows, taskTotal: attention.length, taskBacklog: openCount,
    leases: leaseRows,
  },
  trends: {
    current: { active, occupied, vacant, occupancyRate: occRate, rentRoll: rentroll },
    withOcc,
  },
};

const __dirname = dirname(fileURLToPath(import.meta.url));
writeFileSync(join(__dirname, "public", "data.json"), JSON.stringify(PAYLOAD));
console.log(`Baked data.json — ${units.length} units, ${leases.length} leases, ${tasks.length} tasks, occupancy ${occRate==null?"-":Math.round(occRate*100)+"%"}, ${leaseRows.length} leases expiring 90d.`);
