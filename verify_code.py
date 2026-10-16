"""Check that the published scripts contain the same code as the scripts as run.

Before publication, a few docstrings were edited, six scripts were renamed from their
working names to English names (PROVENANCE.md maps them), one log message was reworded,
and the one absolute default path hard-coded in src/paths.py (a Google Drive folder used
on Colab) was replaced by the variable INTERNAL_WORK_ROOT_DEFAULT, which the module reads
from the environment variable MOVEMENTGNN_WORK_ROOT in one added statement.

This script computes, for each script listed in CODE_AST_SHA256, the sha256 of its syntax
tree with those parts normalized:
  - docstrings are dropped;
  - the added module-level statement INTERNAL_<NAME> = __import__("os").environ.get(..., ...)
    is dropped;
  - an f-string that starts with {INTERNAL_<NAME>} has that field replaced by the fixed
    text <root>, and an f-string with no interpolated expression counts as the plain string;
  - a plain string becomes a fixed placeholder when it has four or more words or names a
    .md note; an f-string whose literal text meets the same test keeps only its
    interpolated expressions, in order;
  - a variable whose name starts with INTERNAL_ becomes a fixed name.
Everything else (all other names, calls, operators, numbers, short strings such as keys,
labels and relative data paths, and the expressions inside every f-string) enters the
digest, so any change to executable code fails the check. Comments are not part of the
syntax tree.

CODE_AST_SHA256 lists the digest of each file AS RUN, computed before publication with
Python 3.11. The tree layout differs between Python versions, so run this with Python 3.11.

Usage (from the repository root):  python3.11 verify_code.py
"""
import ast
import hashlib
import pathlib
import sys

PLACEHOLDER = "<text>"
ROOT_TOKEN = "<root>"
NEUTRAL_PREFIX = "INTERNAL_"
NEUTRAL_NAME = "INTERNAL_NAME"


def is_free_text(s):
    return len(s.split()) >= 4 or ".md" in s


def _is_neutral_name(node):
    return isinstance(node, ast.Name) and node.id.startswith(NEUTRAL_PREFIX)


def _is_env_statement(stmt):
    if not (isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and _is_neutral_name(stmt.targets[0])):
        return False
    v = stmt.value
    return (isinstance(v, ast.Call) and isinstance(v.func, ast.Attribute) and v.func.attr == "get"
            and isinstance(v.func.value, ast.Attribute) and v.func.value.attr == "environ"
            and isinstance(v.func.value.value, ast.Call) and isinstance(v.func.value.value.func, ast.Name)
            and v.func.value.value.func.id == "__import__"
            and len(v.args) == 2 and all(isinstance(a, ast.Constant) and isinstance(a.value, str) for a in v.args))


def drop_docstrings_and_env(tree):
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.body:
            b = n.body[0]
            if isinstance(b, ast.Expr) and isinstance(getattr(b, "value", None), ast.Constant) \
                    and isinstance(b.value.value, str):
                n.body = n.body[1:] or [ast.Pass()]
    tree.body = [s for s in tree.body if not _is_env_statement(s)] or [ast.Pass()]
    return tree


class RootField(ast.NodeTransformer):
    """{INTERNAL_<NAME>} at the start of an f-string becomes the text <root>; an f-string
    without interpolated expressions becomes the plain string."""

    def visit_JoinedStr(self, node):
        self.generic_visit(node)
        vals = list(node.values)
        if vals and isinstance(vals[0], ast.FormattedValue) and _is_neutral_name(vals[0].value) \
                and vals[0].conversion == -1 and vals[0].format_spec is None:
            vals = vals[1:]
            if vals and isinstance(vals[0], ast.Constant):
                vals[0] = ast.Constant(value=ROOT_TOKEN + vals[0].value)
            else:
                vals.insert(0, ast.Constant(value=ROOT_TOKEN))
        node.values = vals
        if all(isinstance(v, ast.Constant) for v in vals):
            return ast.Constant(value="".join(v.value for v in vals))
        return node


class Mask(ast.NodeTransformer):
    free_text = staticmethod(is_free_text)

    def visit_JoinedStr(self, node):
        text = "".join(v.value if isinstance(v, ast.Constant) else "X" for v in node.values)
        if self.free_text(text):
            node.values = [v for v in node.values if not isinstance(v, ast.Constant)]
        return self.generic_visit(node)

    def visit_FormattedValue(self, node):
        node.value = self.visit(node.value)
        return node

    def visit_Name(self, node):
        if node.id.startswith(NEUTRAL_PREFIX):
            node.id = NEUTRAL_NAME
        return node

    def visit_Constant(self, node):
        if isinstance(node.value, str) and self.free_text(node.value):
            return ast.Constant(value=PLACEHOLDER)
        return node


def code_sha256(path):
    tree = ast.parse(pathlib.Path(path).read_text(encoding="utf-8"))
    tree = drop_docstrings_and_env(tree)
    tree = RootField().visit(tree)
    tree = Mask().visit(tree)
    return hashlib.sha256(ast.dump(tree, include_attributes=False).encode("utf-8")).hexdigest()


def file_sha256(path):
    return code_sha256(path)


def main():
    if sys.version_info[:2] != (3, 11):
        print(f"warning: digests were computed with Python 3.11; this is {sys.version.split()[0]}")
    root = pathlib.Path(__file__).resolve().parent
    expected = {}
    for line in (root / "CODE_AST_SHA256").read_text().splitlines():
        if line.strip():
            digest, rel = line.split(None, 1)
            expected[rel.strip()] = digest
    bad = 0
    for rel, digest in sorted(expected.items()):
        ok = file_sha256(root / rel) == digest
        bad += not ok
        if not ok:
            print(f"MISMATCH {rel}")
    print(f"{len(expected) - bad}/{len(expected)} files: code identical to the original")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
