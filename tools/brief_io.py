"""Bounded, unambiguous brief loading and private atomic record writes."""
import json
import os
from pathlib import Path
import tempfile

MAX_BRIEF_BYTES = 1024 * 1024


class BriefError(ValueError):
    pass


def checked_path(path):
    path = Path(path).absolute()
    for part in (path, *path.parents):
        if part.is_symlink() or getattr(part, "is_junction", lambda: False)():
            raise BriefError("Brief paths must not contain symbolic links or junctions")
    return path


def load_brief(path):
    import yaml
    from jsonschema import Draft202012Validator

    class Loader(yaml.SafeLoader):
        def compose_node(self, parent, index):
            if self.check_event(yaml.AliasEvent):
                raise BriefError("YAML aliases are not accepted in compliance briefs")
            return super().compose_node(parent, index)

        def construct_mapping(self, node, deep=False):
            self.flatten_mapping(node)
            result = {}
            for key_node, value_node in node.value:
                key = self.construct_object(key_node, deep=deep)
                if not isinstance(key, (str, int, float, bool, type(None))):
                    raise BriefError("Brief mapping keys must be scalar values")
                if key in result:
                    raise BriefError("Duplicate YAML keys are not accepted")
                result[key] = self.construct_object(value_node, deep=deep)
            return result

    with checked_path(path).open("rb") as source:
        raw = source.read(MAX_BRIEF_BYTES + 1)
    if len(raw) > MAX_BRIEF_BYTES:
        raise BriefError("Brief exceeds the 1 MiB size limit")
    try:
        brief = yaml.load(raw.decode("utf-8"), Loader=Loader)
        if isinstance(brief, dict) and "trace" not in brief:
            raise BriefError("Brief has no trace; certainty cannot be derived")
        schema = json.loads((Path(__file__).resolve().parent.parent / "schema/compliance.schema.json").read_text(encoding="utf-8"))
        error = next(Draft202012Validator(schema).iter_errors(brief), None)
        if error:
            # Validation exceptions often include the entire sensitive instance.
            raise BriefError("Brief does not match schema/compliance.schema.json")
    except (yaml.YAMLError, UnicodeError, RecursionError) as exc:
        raise BriefError("Brief contains invalid or excessively nested YAML") from exc
    return brief


def write_brief(path, brief):
    import yaml
    path = checked_path(path)
    fd, temporary = tempfile.mkstemp(prefix=".compliance-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as output:
            output.write(yaml.safe_dump(brief, sort_keys=False))
            output.flush()
            os.fsync(output.fileno())
        checked_path(path)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)
