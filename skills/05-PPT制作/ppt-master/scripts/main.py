#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


SKILL_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_DIR = SKILL_ROOT / "scripts"


def _py():
    return sys.executable or "python"


def _run(command, cwd, env):
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result


def _script(name):
    return str((SCRIPT_DIR / name).resolve())


def _resolve_user_path(path, cwd):
    path_obj = Path(path)
    if path_obj.is_absolute():
        return str(path_obj)
    return str((Path(cwd) / path_obj).resolve())


def _artifact_from_args(argv):
    artifacts = []
    for idx, item in enumerate(argv):
        if item in ("-o", "--output") and idx + 1 < len(argv):
            artifacts.append(argv[idx + 1])
    return artifacts


def _export_pipeline(project_path, env, include_notes=True, output=None):
    commands = []
    project_path = str(Path(project_path).resolve())
    notes_path = Path(project_path) / "notes" / "total.md"
    if include_notes and notes_path.exists():
        commands.append([_py(), _script("total_md_split.py"), str(project_path)])
    # finalize_svg.py prepares svg_final, which is the only supported export source.
    commands.append([_py(), _script("finalize_svg.py"), str(project_path)])

    pptx_cmd = [_py(), _script("svg_to_pptx.py"), str(project_path), "-s", "final"]
    if output:
        pptx_cmd.extend(["-o", str(output)])
    if not include_notes or not notes_path.exists():
        pptx_cmd.append("--no-notes")
    commands.append(pptx_cmd)

    last = None
    for cmd in commands:
        last = _run(cmd, cwd=str(SKILL_ROOT), env=env)
        if last.returncode != 0:
            break
    return last, commands


def _run_sync(inputs: dict, context=None):
    argv = [str(item) for item in inputs.get("argv", [])]
    cwd = inputs.get("cwd", str(SKILL_ROOT))
    if not os.path.isabs(cwd):
        cwd = str((SKILL_ROOT / cwd).resolve())
    env = os.environ.copy()
    env.update({str(k): str(v) for k, v in (inputs.get("env", {}) or {}).items()})

    if not argv or argv[0] in {"-h", "--help", "help"}:
        summary = (
            "ppt-master commands: "
            "init, import-sources, validate, info, export, smoke, outline-to-md, async-run, "
            "project_manager.py, finalize_svg.py, svg_to_pptx.py"
        )
        return {
            "status": "success",
            "summary": summary,
            "outputs": {"stdout": summary, "stderr": "", "returncode": 0},
            "artifacts": [],
        }

    command = argv[0]
    args = argv[1:]
    artifacts = []

    if command == "smoke":
        if args:
            project_path = _resolve_user_path(args[0], cwd)
        else:
            project_dirs = sorted((SKILL_ROOT / "projects").glob("*"))
            project_path = str(project_dirs[0].resolve()) if project_dirs else ""
            if not project_path:
                return {
                    "status": "failed",
                    "summary": "smoke requires a project_path when no local project exists",
                    "outputs": {"stdout": "", "stderr": "missing project_path", "returncode": 2},
                    "artifacts": [],
                    "error": {"message": "missing project_path"},
                }
        output = args[1] if len(args) > 1 else None
        result, pipeline = _export_pipeline(project_path, env, include_notes=True, output=output)
        if result is None:
            status = "failed"
            stdout = ""
            stderr = "export pipeline did not start"
            returncode = 1
        else:
            status = "success" if result.returncode == 0 else "failed"
            stdout = result.stdout
            stderr = result.stderr
            returncode = result.returncode
            if output:
                artifacts.append(output)
            else:
                guess = Path(project_path) / f"{Path(project_path).name}.pptx"
                artifacts.append(str(guess))
        summary = f"smoke pipeline={' | '.join(' '.join(cmd) for cmd in pipeline)} returncode={returncode}"
        return {
            "status": status,
            "summary": summary,
            "outputs": {"stdout": stdout, "stderr": stderr, "returncode": returncode},
            "artifacts": artifacts,
            "error": None if status == "success" else {"message": stderr or stdout or "smoke failed"},
        }

    if command in {"outline-to-md", "outline_import", "outline-import"}:
        result = _run([_py(), _script("outline_to_md.py"), *args], cwd=cwd, env=env)
        status = "success" if result.returncode == 0 else "failed"
        artifacts.extend(_artifact_from_args([command, *args]))
        return {
            "status": status,
            "summary": f"outline-to-md returncode={result.returncode}",
            "outputs": {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            },
            "artifacts": artifacts,
            "error": None if status == "success" else {"message": result.stderr or result.stdout or "outline-to-md failed"},
        }

    if command in {"async-run", "async_svg_runner.py", "async-svg-runner"}:
        result = _run([_py(), _script("async_svg_runner.py"), *args], cwd=cwd, env=env)
        status = "success" if result.returncode == 0 else "failed"
        return {
            "status": status,
            "summary": f"async-run returncode={result.returncode}",
            "outputs": {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            },
            "artifacts": [],
            "error": None if status == "success" else {"message": result.stderr or result.stdout or "async-run failed"},
        }

    if command == "export":
        if not args:
            return {
                "status": "failed",
                "summary": "export requires project_path",
                "outputs": {"stdout": "", "stderr": "missing project_path", "returncode": 2},
                "artifacts": [],
                "error": {"message": "missing project_path"},
            }
        project_path = _resolve_user_path(args[0], cwd)
        output = None
        if "-o" in args:
            idx = args.index("-o")
            if idx + 1 < len(args):
                output = args[idx + 1]
        elif "--output" in args:
            idx = args.index("--output")
            if idx + 1 < len(args):
                output = args[idx + 1]
        result, pipeline = _export_pipeline(project_path, env, include_notes=True, output=output)
        status = "success" if result and result.returncode == 0 else "failed"
        stdout = "" if result is None else result.stdout
        stderr = "" if result is None else result.stderr
        returncode = 1 if result is None else result.returncode
        if output:
            artifacts.append(output)
        summary = f"export pipeline={' | '.join(' '.join(cmd) for cmd in pipeline)} returncode={returncode}"
        return {
            "status": status,
            "summary": summary,
            "outputs": {"stdout": stdout, "stderr": stderr, "returncode": returncode},
            "artifacts": artifacts,
            "error": None if status == "success" else {"message": stderr or stdout or "export failed"},
        }

    if command in {"project_manager.py", "project-manager"}:
        result = _run([_py(), _script("project_manager.py"), *args], cwd=cwd, env=env)
    elif command in {"finalize_svg.py", "finalize-svg"}:
        result = _run([_py(), _script("finalize_svg.py"), *args], cwd=cwd, env=env)
    elif command in {"svg_to_pptx.py", "svg-to-pptx"}:
        result = _run([_py(), _script("svg_to_pptx.py"), *args], cwd=cwd, env=env)
    elif command in {"total_md_split.py", "notes-split"}:
        result = _run([_py(), _script("total_md_split.py"), *args], cwd=cwd, env=env)
    elif command in {"validate", "info", "init", "import-sources"}:
        result = _run([_py(), _script("project_manager.py"), command, *args], cwd=cwd, env=env)
    else:
        result = _run([_py(), _script(command), *args], cwd=cwd, env=env)

    status = "success" if result.returncode == 0 else "failed"
    artifacts.extend(_artifact_from_args([command, *args]))
    return {
        "status": status,
        "summary": f"command={command} returncode={result.returncode}",
        "outputs": {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        },
        "artifacts": artifacts,
        "error": None if status == "success" else {"message": result.stderr or result.stdout or "command failed"},
    }


async def run(inputs: dict, context=None):
    # Keep the packaged skill async-compatible while preserving the original sync router.
    return _run_sync(inputs, context=context)


if __name__ == "__main__":
    payload = {"argv": sys.argv[1:]}
    print(json.dumps(_run_sync(payload), ensure_ascii=False, indent=2))
