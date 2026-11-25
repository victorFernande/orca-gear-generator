# Build and test dependency lookup

The smoke harness and geometry tests previously added both the running Python
ABI directory and Orca's `cp312` package directory to `sys.path`. On a machine
with Python 3.14 and Orca's Python 3.12 NumPy installed, this could select the
wrong compiled NumPy extension and fail before testing any geometry.

Only the running interpreter's `cpXY` directory is now eligible. Python 3.12
still uses `cp312`; other interpreters retain their own NumPy installation.
This change affects build/test tooling and does not modify plugin geometry,
runtime UI, bundles or the release version.

All 26 Python tests passed locally with `-B -W error` on Python 3.12 and 3.14
after the change; before it, Python 3.14 failed during NumPy import.

The bundle already compresses its offline UI and language data losslessly.
No geometry quality reduction or additional runtime dependency was introduced.
Native Windows review covered page/dock helix changes, STL/3MF exports and
import of the exported pair onto the OrcaSlicer bed. An Arrange action was
required after importing the two STLs as separate objects.
