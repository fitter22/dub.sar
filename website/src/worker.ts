const PYODIDE_INDEX = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";

interface LoadMessage {
  type: "load";
}

interface RunMessage {
  type: "run";
  id: number;
  source: string;
  backend: string;
  stdin: string;
}

type Inbound = LoadMessage | RunMessage;

interface PyodideLike {
  loadPackage: (name: string) => Promise<unknown>;
  runPythonAsync: (code: string) => Promise<unknown>;
  globals: {
    set: (name: string, value: string) => void;
  };
  runPython: (code: string) => string;
}

const scope = globalThis as unknown as {
  location: { origin: string };
  onmessage: ((event: MessageEvent<Inbound>) => void) | null;
  postMessage: (message: unknown) => void;
};

let pyodide: PyodideLike | null = null;
let loading: Promise<void> | null = null;

async function ensureRuntime(): Promise<void> {
  if (pyodide) {
    return;
  }
  if (!loading) {
    loading = (async () => {
      const moduleUrl = `${PYODIDE_INDEX}pyodide.mjs`;
      const pyodideModule = (await import(/* @vite-ignore */ moduleUrl)) as {
        loadPyodide: (options: { indexURL: string }) => Promise<PyodideLike>;
      };
      const runtime = await pyodideModule.loadPyodide({ indexURL: PYODIDE_INDEX });
      const manifestUrl = new URL("/runtime/manifest.json", scope.location.origin).href;
      const manifest = (await (await fetch(manifestUrl)).json()) as { wheel: string };
      const wheelUrl = new URL(`/runtime/${manifest.wheel}`, scope.location.origin).href;
      const runnerUrl = new URL("/runtime/runner.py", scope.location.origin).href;
      await runtime.loadPackage("micropip");
      runtime.globals.set("wheel_url", wheelUrl);
      await runtime.runPythonAsync("import micropip\nawait micropip.install(wheel_url)\n");
      const runner = await (await fetch(runnerUrl)).text();
      runtime.runPython(runner);
      pyodide = runtime;
    })().catch((error: unknown) => {
      loading = null;
      throw error;
    });
  }
  await loading;
}

scope.onmessage = (event: MessageEvent<Inbound>) => {
  const message = event.data;
  if (message.type === "load") {
    ensureRuntime()
      .then(() => {
        const version = pyodide?.runPython("__import__('dubsar').__version__") ?? "";
        scope.postMessage({ type: "ready", version });
      })
      .catch((error: unknown) => {
        scope.postMessage({
          type: "ready-error",
          message: error instanceof Error ? error.message : String(error),
        });
      });
    return;
  }
  ensureRuntime()
    .then(() => {
      if (!pyodide) {
        throw new Error("The runtime did not load.");
      }
      pyodide.globals.set("source_text", message.source);
      pyodide.globals.set("backend_name", message.backend);
      pyodide.globals.set("stdin_text", message.stdin);
      const started = Date.now();
      const raw = pyodide.runPython("execute(source_text, backend_name, stdin_text)");
      const payload = JSON.parse(String(raw)) as Record<string, unknown>;
      scope.postMessage({
        type: "result",
        id: message.id,
        elapsedMs: Date.now() - started,
        ...payload,
      });
    })
    .catch((error: unknown) => {
      scope.postMessage({
        type: "result",
        id: message.id,
        ok: false,
        errorType: "InternalError",
        diagnostic: error instanceof Error ? error.message : String(error),
      });
    });
};
