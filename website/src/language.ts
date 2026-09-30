import { StreamLanguage } from "@codemirror/language";

const KEYWORDS = new Set([
  "problem",
  "result",
  "recipe",
  "procedure",
  "when",
  "else",
  "consider",
  "from",
  "through",
  "to",
  "retain",
  "return",
  "output",
  "inscribe",
  "ask",
  "input",
  "empty",
  "none",
  "not",
  "and",
  "or",
  "is",
  "lesser",
  "greater",
  "equal",
  "than",
  "of",
  "add",
  "subtract",
  "multiply",
  "divide",
  "square",
  "square-root",
  "floor",
  "ceil",
  "nearest",
  "absolute",
  "convert",
  "take",
  "consult",
  "working",
  "tablet",
  "append",
  "put",
  "determine",
  "apply",
]);

export const dubsarLanguage = StreamLanguage.define({
  token(stream) {
    if (stream.eatSpace()) {
      return null;
    }
    if (stream.match(/^(#|𒑰)/)) {
      stream.skipToEnd();
      return "comment";
    }
    if (stream.match(/^"(?:\\.|[^"\\])*"/)) {
      return "string";
    }
    if (stream.match(/^-?\d+(?:;\d+(?:,\d+)*)?/)) {
      return "number";
    }
    if (stream.match(/^[\p{Script=Cuneiform}]+/u)) {
      return "keyword";
    }
    if (stream.match(/^[\p{L}\p{N}_-]+/u)) {
      const word = stream.current().toLowerCase();
      return KEYWORDS.has(word) ? "keyword" : "variableName";
    }
    stream.next();
    return null;
  },
});
