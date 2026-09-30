import { closeBrackets, closeBracketsKeymap } from "@codemirror/autocomplete";
import {
  defaultKeymap,
  history,
  historyKeymap,
  indentWithTab,
} from "@codemirror/commands";
import {
  HighlightStyle,
  bracketMatching,
  indentOnInput,
  indentUnit,
  syntaxHighlighting,
} from "@codemirror/language";
import { EditorState, type Extension } from "@codemirror/state";
import { EditorView, keymap, lineNumbers } from "@codemirror/view";
import { tags } from "@lezer/highlight";

import { dubsarLanguage } from "./language";

const tabletHighlight = HighlightStyle.define([
  { tag: tags.keyword, color: "#e7c98a" },
  { tag: tags.comment, color: "#8d7b68", fontStyle: "italic" },
  { tag: tags.string, color: "#d7efe4" },
  { tag: tags.number, color: "#f2d2b3" },
  { tag: tags.variableName, color: "#f6f1e7" },
]);

const tabletTheme = EditorView.theme(
  {
    "&": {
      backgroundColor: "#1a140f",
      color: "#f6f1e7",
      height: "100%",
    },
    ".cm-content": {
      fontFamily: '"Noto Sans", "Noto Sans Cuneiform", sans-serif',
      fontSize: "15px",
      lineHeight: "1.55",
      caretColor: "#e7c98a",
      padding: "12px 0",
    },
    ".cm-gutters": {
      backgroundColor: "#241c16",
      color: "#8d7b68",
      border: "none",
    },
    ".cm-activeLine": { backgroundColor: "rgba(231, 201, 138, 0.08)" },
    ".cm-activeLineGutter": { backgroundColor: "transparent" },
    "&.cm-focused": { outline: "none" },
    ".cm-selectionBackground, &.cm-focused .cm-selectionBackground": {
      backgroundColor: "rgba(35, 78, 112, 0.55)",
    },
  },
  { dark: true },
);

export function createEditor(parent: HTMLElement, onRun: () => void): EditorView {
  const extensions: Extension[] = [
    lineNumbers(),
    history(),
    indentOnInput(),
    bracketMatching(),
    closeBrackets(),
    dubsarLanguage,
    syntaxHighlighting(tabletHighlight),
    tabletTheme,
    EditorView.lineWrapping,
    keymap.of([
      { key: "Mod-Enter", run: () => (onRun(), true) },
      indentWithTab,
      ...closeBracketsKeymap,
      ...defaultKeymap,
      ...historyKeymap,
    ]),
    EditorState.tabSize.of(4),
    indentUnit.of("    "),
  ];
  return new EditorView({
    parent,
    state: EditorState.create({ doc: "", extensions }),
  });
}

export function editorText(view: EditorView): string {
  return view.state.doc.toString();
}

export function setEditorText(view: EditorView, source: string): void {
  const text = source.replace(/^\n/, "").replace(/\s+$/, "\n");
  view.dispatch({
    changes: { from: 0, to: view.state.doc.length, insert: text },
  });
}

export function revealPosition(view: EditorView, line: number, col: number): void {
  if (!Number.isFinite(line) || line < 1) {
    return;
  }
  const lineInfo = view.state.doc.line(Math.min(line, view.state.doc.lines));
  const anchor = Math.min(lineInfo.from + Math.max(col - 1, 0), lineInfo.to);
  view.dispatch({
    selection: { anchor },
    scrollIntoView: true,
  });
  view.focus();
}
