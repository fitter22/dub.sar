import type { EditorView } from "@codemirror/view";

import { createEditor, editorText, revealPosition, setEditorText } from "./editor";

interface ExampleEntry {
  id: string;
  title: string;
  difficulty: string;
  mode: "scholar" | "tablet" | "mixed";
  concept: string;
  purpose: string;
  source: string;
}

interface RunResult {
  type: "result";
  id: number;
  ok?: boolean;
  output?: string[];
  diagnostic?: string;
  version?: string;
  line?: number | null;
  col?: number | null;
  errorType?: string;
  elapsedMs?: number;
}

const RUN_LIMIT_MS = 8000;

function required<T extends Element>(element: T | null, id: string): T {
  if (!element) {
    throw new Error(`Playground markup is incomplete (${id})`);
  }
  return element;
}

const editorHost = required(document.querySelector<HTMLElement>("#editor"), "editor");
const output = required(document.querySelector<HTMLElement>("#output"), "output");
const status = required(document.querySelector<HTMLElement>("#status"), "status");
const blurb = required(document.querySelector<HTMLElement>("#blurb"), "blurb");
const exampleSelect = required(document.querySelector<HTMLSelectElement>("#example"), "example");
const modeSelect = required(document.querySelector<HTMLSelectElement>("#mode"), "mode");
const levelSelect = required(document.querySelector<HTMLSelectElement>("#level"), "level");
const backendSelect = required(document.querySelector<HTMLSelectElement>("#backend"), "backend");
const stdinBox = required(document.querySelector<HTMLTextAreaElement>("#stdin"), "stdin");
const runButton = required(document.querySelector<HTMLButtonElement>("#run"), "run");
const resetButton = required(document.querySelector<HTMLButtonElement>("#reset"), "reset");
const versionLabel = required(document.querySelector<HTMLElement>("#version"), "version");

let catalog: ExampleEntry[] = [];
let worker: Worker | null = null;
let requestId = 0;
let runtimeReady = false;
let activeRequest = 0;
let runTimer = 0;
let pendingRun = false;
let baselineSource = "";

function scrollToPlayground(): void {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.querySelector("#playground")?.scrollIntoView({
    behavior: reduce ? "auto" : "smooth",
  });
}

function loadSource(source: string): void {
  baselineSource = source;
  setEditorText(editor, source);
}

const editor: EditorView = createEditor(editorHost, () => {
  void runTablet();
});

function setStatus(text: string): void {
  status.textContent = text;
}

function filteredExamples(): ExampleEntry[] {
  const mode = modeSelect.value;
  const level = levelSelect.value;
  return catalog.filter((entry) => {
    const modeOk = mode === "all" || entry.mode === mode;
    const levelOk = level === "all" || entry.difficulty === level;
    return modeOk && levelOk;
  });
}

function showBlurb(entry: ExampleEntry | undefined): void {
  if (!entry) {
    blurb.textContent = "";
    return;
  }
  const concept = entry.concept ? `${entry.concept}. ` : "";
  blurb.textContent = `${concept}${entry.purpose}`;
}

function renderExamples(preferredId?: string): void {
  const entries = filteredExamples();
  const previous = preferredId ?? exampleSelect.value;
  exampleSelect.replaceChildren();
  for (const entry of entries) {
    const option = document.createElement("option");
    option.value = entry.id;
    option.textContent = entry.title;
    exampleSelect.append(option);
  }
  const chosen = entries.find((entry) => entry.id === previous) ?? entries[0];
  if (!chosen) {
    showBlurb(undefined);
    return;
  }
  exampleSelect.value = chosen.id;
  loadSource(chosen.source);
  showBlurb(chosen);
}

function ensureWorker(): Worker {
  if (worker) {
    return worker;
  }
  const next = new Worker(new URL("./worker.ts", import.meta.url), { type: "module" });
  next.addEventListener("message", (event: MessageEvent<RunResult | { type: string; version?: string; message?: string }>) => {
    const data = event.data;
    if (data.type === "ready") {
      runtimeReady = true;
      const version = "version" in data ? data.version : "";
      versionLabel.textContent = version ? `DUB.SAR ${version}` : "DUB.SAR";
      setStatus("Runtime ready. This tablet runs in your browser.");
      runButton.disabled = false;
      if (pendingRun) {
        runTablet();
      }
      return;
    }
    if (data.type === "ready-error") {
      runtimeReady = false;
      pendingRun = false;
      runButton.disabled = false;
      setStatus("message" in data && data.message ? data.message : "The runtime failed to load.");
      return;
    }
    if (data.type !== "result" || !("id" in data) || data.id !== activeRequest) {
      return;
    }
    window.clearTimeout(runTimer);
    runButton.disabled = false;
    showResult(data as RunResult);
  });
  worker = next;
  return next;
}

function bootRuntime(): void {
  if (runtimeReady || worker) {
    return;
  }
  setStatus("Loading the WebAssembly runtime. The first visit fetches it once.");
  runButton.disabled = true;
  ensureWorker().postMessage({ type: "load" });
}

function showResult(result: RunResult): void {
  output.replaceChildren();
  if (result.ok && result.output) {
    const pre = document.createElement("pre");
    pre.textContent = result.output.join("\n") || "(The tablet inscribed nothing.)";
    output.append(pre);
    const elapsed = result.elapsedMs !== undefined ? ` in ${result.elapsedMs} ms` : "";
    setStatus(`Inscribed${elapsed}.`);
    return;
  }
  const pre = document.createElement("pre");
  pre.className = "diagnostic";
  pre.textContent = result.diagnostic || "The tablet failed.";
  output.append(pre);
  if (result.line) {
    revealPosition(editor, result.line, result.col ?? 1);
  }
  setStatus(result.errorType === "TimeLimit" ? "Stopped at the time limit." : "The tablet reported an error.");
}

function stopForTimeLimit(): void {
  worker?.terminate();
  worker = null;
  runtimeReady = false;
  versionLabel.textContent = "Runtime reset";
  runButton.disabled = false;
  showResult({
    type: "result",
    id: activeRequest,
    ok: false,
    errorType: "TimeLimit",
    diagnostic:
      "Execution stopped. This tablet exceeded the browser time limit, so the runtime was reset.",
  });
}

function runTablet(): void {
  if (!runtimeReady) {
    pendingRun = true;
    bootRuntime();
    setStatus("Loading the WebAssembly runtime. The tablet will run when it is ready.");
    return;
  }
  pendingRun = false;
  requestId += 1;
  activeRequest = requestId;
  runButton.disabled = true;
  setStatus("Inscribing…");
  output.replaceChildren();
  window.clearTimeout(runTimer);
  runTimer = window.setTimeout(stopForTimeLimit, RUN_LIMIT_MS);
  ensureWorker().postMessage({
    type: "run",
    id: activeRequest,
    source: editorText(editor),
    backend: backendSelect.value,
    stdin: stdinBox.value,
  });
}

document.querySelector("#try")?.addEventListener("click", () => {
  scrollToPlayground();
  bootRuntime();
  editor.focus();
});

document.querySelectorAll<HTMLButtonElement>("[data-load]").forEach((button) => {
  button.addEventListener("click", () => {
    const sourceNode = document.getElementById(button.dataset.load ?? "");
    if (!sourceNode) {
      return;
    }
    loadSource(sourceNode.textContent ?? "");
    showBlurb(undefined);
    blurb.textContent = "A demonstration tablet. It is not a transliteration of the other column.";
    scrollToPlayground();
    bootRuntime();
  });
});

modeSelect.addEventListener("change", () => renderExamples());
levelSelect.addEventListener("change", () => renderExamples());
exampleSelect.addEventListener("change", () => {
  const entry = catalog.find((item) => item.id === exampleSelect.value);
  if (entry) {
    loadSource(entry.source);
    showBlurb(entry);
  }
});
runButton.addEventListener("click", () => {
  runTablet();
});
resetButton.addEventListener("click", () => {
  setEditorText(editor, baselineSource);
  output.replaceChildren();
  setStatus("The editor was restored to the loaded tablet.");
});

const playground = document.querySelector("#playground");
if (playground) {
  const observer = new IntersectionObserver(
    (entries) => {
      if (entries.some((entry) => entry.isIntersecting)) {
        bootRuntime();
        observer.disconnect();
      }
    },
    { rootMargin: "200px" },
  );
  observer.observe(playground);
}

void fetch("/catalog.json")
  .then((response) => response.json())
  .then((entries: ExampleEntry[]) => {
    catalog = entries;
    renderExamples("first_tablet_scholar");
  })
  .catch(() => {
    setStatus("The example catalog could not be loaded. Run npm run prepare-assets in website/.");
  });
