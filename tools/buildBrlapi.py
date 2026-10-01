# A part of NonVisual Desktop Access (NVDA)
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Build NVDA's BrlAPI binding against the local CPython ABI using MSVC.

The BrlAPI DLL retains its upstream ABI. Only the Python binding is rebuilt.
Generated sources stay under build/brlapi314; the upstream checkout is unchanged.
"""

import argparse
import shutil
import struct
import subprocess
import sys
import sysconfig
from pathlib import Path

import pefile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--brltty", type=Path, required=True, help="BRLTTY source checkout")
args = parser.parse_args()
if (
	sys.platform != "win32"
	or sys.version_info[:2] != (3, 14)
	or struct.calcsize("P") != 8
	or sysconfig.get_config_var("Py_GIL_DISABLED")
):
	raise RuntimeError("Build this binding with standard CPython 3.14 x64")
ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = args.brltty.resolve()
upstreamCommit = subprocess.check_output(["git", "-C", str(UPSTREAM), "rev-parse", "HEAD"], text=True).strip()
if upstreamCommit != "06e44da90784505fc5d2869f75f02160d6855d03":
	raise RuntimeError("Use BRLTTY commit 06e44da90784505fc5d2869f75f02160d6855d03 for this build recipe")
OUT = ROOT / "build" / "brlapi314"
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "Programs").mkdir(exist_ok=True)
AWK = Path(r"C:\Program Files\Git\usr\bin\awk.exe")
DLL = ROOT / "python" / "brlapi-0.8.dll"


def run(*args, cwd=OUT):
	subprocess.run([str(arg) for arg in args], cwd=cwd, check=True)


def write(name, content):
	(OUT / name).write_text(content, encoding="utf-8", newline="\n")


header = (UPSTREAM / "Programs" / "brlapi.h.in").read_text(encoding="utf-8")
for name, value in {
	"BRLAPI_WIN32": "1",
	"BRLAPI_RELEASE": '"0.8.7"',
	"BRLAPI_MAJOR": "0",
	"BRLAPI_MINOR": "8",
	"BRLAPI_REVISION": "7",
}.items():
	header = header.replace(f"#undef {name}\n", f"#define {name} {value}\n")
start = header.index("#ifdef _MSC_VER")
end = header.index("#else /* _MSC_VER */", start)
header = (
	header[:start]
	+ """#ifdef _MSC_VER
#include <stdint.h>
#include <inttypes.h>
typedef SSIZE_T ssize_t;
"""
	+ header[end:]
)
write("Programs/brlapi.h", header)
for name in ("brlapi_keycodes.h", "brlapi_param.h", "brlapi_protocol.h"):
	shutil.copy2(UPSTREAM / "Programs" / name, OUT / "Programs" / name)
protocol = (OUT / "Programs" / "brlapi_protocol.h").read_text(encoding="utf-8")
write(
	"Programs/brlapi_protocol.h",
	protocol.replace("#include <unistd.h>", "#include <stddef.h>").replace(
		"#ifdef __MINGW32__", "#if defined(__MINGW32__) || defined(_MSC_VER)"
	),
)
scripts = ["-f", UPSTREAM / "Programs" / "brl_cmds.awk"]
commands = [UPSTREAM / "Headers" / "brl_cmds.h", UPSTREAM / "Headers" / "brl_custom.h"]
result = subprocess.run(
	[
		str(AWK),
		"-f",
		str(UPSTREAM / "Programs" / "brlapi_constants.awk"),
		*map(str, scripts),
		*map(str, commands),
	],
	check=True,
	capture_output=True,
)
write("Programs/brlapi_constants.h", result.stdout.decode("utf-8"))
result = subprocess.run(
	[
		str(AWK),
		"-f",
		str(UPSTREAM / "Programs" / "brlapi.awk"),
		"-f",
		str(UPSTREAM / "Bindings" / "Python" / "constants.awk"),
		*map(str, scripts),
		str(OUT / "Programs" / "brlapi.h"),
		str(OUT / "Programs" / "brlapi_keycodes.h"),
		str(OUT / "Programs" / "brlapi_param.h"),
		*map(str, commands),
	],
	check=True,
	capture_output=True,
)
write("constants.auto.pyx", result.stdout.decode("utf-8"))
for name in ("brlapi.pyx", "c_brlapi.pxd", "bindings.h"):
	shutil.copy2(UPSTREAM / "Bindings" / "Python" / name, OUT / name)
pyx = (OUT / "brlapi.pyx").read_text(encoding="utf-8")
# Establish a safe destructor state even if argument conversion raises.
pyx = pyx.replace(
	"cdef class Connection:\n",
	"cdef class Connection:\n\tdef __cinit__(self):\n\t\tself.fd = -1\n\t\tself.h = NULL\n\n",
)
# A failed open destroys the handle mutexes; never register a handler on it.
pyx = pyx.replace("\t\tc_brlapi.brlapi_protocolExceptionInit(self.h)\n", "")
pyx = pyx.replace(
	"\t\t\traise ConnectionError(self.settings.host, self.settings.auth)\n",
	"\t\t\traise ConnectionError(self.settings.host, self.settings.auth)\n"
	"\t\tc_brlapi.brlapi_protocolExceptionInit(self.h)\n",
)
pyx = pyx.replace(
	"\t\tself.h = <c_brlapi.brlapi_handle_t*> c_brlapi.malloc(c_brlapi.brlapi_getHandleSize())\n",
	"\t\tself.fd = -1\n"
	"\t\tself.h = <c_brlapi.brlapi_handle_t*> c_brlapi.malloc(c_brlapi.brlapi_getHandleSize())\n"
	"\t\tif self.h == NULL:\n\t\t\traise MemoryError()\n",
)
write("brlapi.pyx", pyx)
bindings = (UPSTREAM / "Bindings" / "Python" / "bindings.c").read_text(encoding="utf-8")
bindings = bindings.replace("#include <pthread.h>", '#include "windows_thread_compat.h"')
bindings = bindings.replace(
	"char *brlapi_protocolException(void)\n{\n",
	"static void do_brlapi_protocolExceptionInit(void);\n"
	"char *brlapi_protocolException(void)\n{\n"
	"  pthread_once(&brlapi_protocolExceptionOnce, do_brlapi_protocolExceptionInit);\n",
)
write("bindings.c", bindings)
write(
	"windows_thread_compat.h",
	"""/* Windows equivalents of the four pthread TLS/once operations used here. */
#include <windows.h>
#include <stdlib.h>
typedef INIT_ONCE pthread_once_t;
typedef DWORD pthread_key_t;
#define PTHREAD_ONCE_INIT INIT_ONCE_STATIC_INIT
static VOID CALLBACK exceptionFree(PVOID value) { free(value); }
static int pthread_key_create(pthread_key_t *key, void (*destructor)(void *)) {
    *key = FlsAlloc(exceptionFree);
    return *key == FLS_OUT_OF_INDEXES ? -1 : 0;
}
static void *pthread_getspecific(pthread_key_t key) { return FlsGetValue(key); }
static int pthread_setspecific(pthread_key_t key, const void *value) {
    return FlsSetValue(key, (void *)value) ? 0 : -1;
}
static BOOL CALLBACK initializeException(PINIT_ONCE once, PVOID fn, PVOID *context) {
    ((void (*)(void))fn)();
    return TRUE;
}
static int pthread_once(pthread_once_t *once, void (*fn)(void)) {
    return InitOnceExecuteOnce(once, initializeException, (PVOID)fn, NULL) ? 0 : -1;
}
""",
)
binary = pefile.PE(str(DLL))
exports = [symbol.name.decode("ascii") for symbol in binary.DIRECTORY_ENTRY_EXPORT.symbols if symbol.name]
write("brlapi.def", 'LIBRARY "brlapi-0.8.dll"\nEXPORTS\n' + "\n".join(exports) + "\n")
binary.close()
vswhere = Path(r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe")
vs = subprocess.check_output(
	[
		str(vswhere),
		"-latest",
		"-products",
		"*",
		"-requires",
		"Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
		"-property",
		"installationPath",
	],
	text=True,
).strip()
if not vs:
	vs = r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools"
vcvars = Path(vs) / "VC" / "Auxiliary" / "Build" / "vcvars64.bat"
if not vcvars.is_file():
	raise RuntimeError(f"MSVC initialization script not found: {vcvars}")
write(
	"build-import.bat",
	f'@echo off\ncall "{vcvars}" >nul\nif errorlevel 1 exit /b 1\nlib.exe /nologo /def:brlapi.def /out:brlapi.lib /machine:x64\n',
)
run("cmd.exe", "/d", "/c", "build-import.bat")
run(sys.executable, "-m", "cython", "-3", "-X", "embedsignature=True", "-o", "brlapi.auto.c", "brlapi.pyx")
write(
	"setup.py",
	"""from setuptools import setup, Extension
setup(name="Brlapi", version="0.8.7", ext_modules=[Extension(
    "brlapi", sources=["brlapi.auto.c", "bindings.c"],
    include_dirs=[".", "Programs"], library_dirs=["."], libraries=["brlapi"],
    define_macros=[("WINDOWS", "1")], extra_compile_args=["/std:c11"],
)])
""",
)
run(sys.executable, "setup.py", "build_ext", "--inplace")
built = next(OUT.glob("brlapi.cp314-win_amd64.pyd"))
shutil.copy2(built, ROOT / "python" / built.name)
print(f"Built and installed {built.name}")
