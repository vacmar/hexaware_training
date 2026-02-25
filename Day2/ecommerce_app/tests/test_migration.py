import subprocess
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

ALEMBIC_INI = os.path.join(PROJECT_ROOT, "alembic.ini")

def test_alembic_upgrade():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-c",
            ALEMBIC_INI,  # 👈 explicitly pass config
            "upgrade",
            "head",
        ],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0


def test_alembic_downgrade():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-c",
            ALEMBIC_INI,  # 👈 explicitly pass config
            "downgrade",
            "-1",
        ],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    print(result.stdout)
    print(result.stderr)

    # Pass if either successful or no migrations to downgrade
    assert result.returncode == 0 or "didn't produce 1 migrations" in result.stdout