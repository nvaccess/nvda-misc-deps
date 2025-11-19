Misc-deps is a collection of various static dependencies used by [NVDA](https://github.com/nvaccess/nvda).

See also [NVDA git submodules documentation](https://github.com/nvaccess/nvda/blob/master/projectDocs/dev/createDevEnvironment.md#git-submodules) for context.

# Updating contents

## include

### Adobe Acrobat Access

1. Download the latest [Adobe Acrobat SDK](https://developer.adobe.com/console/servicesandapis)
1. Extract the zip
1. Copy the file from `Adobe\Acrobat DC SDK\Version 1\AccessibilitySupport\AcrobatAccess.idl`

### iSimpleDOM

ISimpleDOM interfaces for gecko / firefox.

Update from [here](https://github.com/mozilla/gecko-dev/tree/master/accessible/interfaces/msaa).
The `moz.build` file is not required, but can be used to inform updates to [our build script](..\nvdaHelper\ISimpleDOM_sconscript).

Changes may require build script changes.

## python

### brlapi

Used for BrlTTY.

To get the necessary files, you can extract them from a build artifact produced by [GitHub Actions in the NV Access fork of the brlTTY repository](https://github.com/nvaccess/brltty/actions).

The following files should be updated:

* `brlapi.cp3xx-amd64.pyd`
  * Note: 3xx should be the actual Python version, e.g. 313)
  * This file resides in the folder `python/Brlapi-0.8.x-py3.xx-win-amd64.egg`
  * You don't need `brlapi.py`
* `brlapi-*.dll`
  * This file resides in the `bin` folder in the artifact

#### Building from source

If BRLTTY doesn't have a public release compatible with NVDA's python version, you must build it from source.

Note: The GitHub actions workflow in the above mentioned repository can be adapted according to what's necessary to build a proper version.
For example, you can change the python version to your needs.

Below is a short build reference to get you started locally if desired:

1. Install Python x64 and ensure it is on your PATH.
  * Install Python build dependencies: `setuptools` and `cython`.
1. Install [MSYS2](https://www.msys2.org/) (UCRT64) and update all packages.
  * Install build tools and libraries: `autoconf`, `automake`, `make`, `awk`, `bison`, `git`, `groff`, `m4`, `patch`, `tcl`, `pdcurses`, `icu`, `libiconv`, `toolchain`, `libusb`.
1. Clone the [BRLTTY repository](https://github.com/brltty/brltty).
1. Open MSYS2 UCRT64 shell and go to the repository.
1. Apply any patches if needed (`Windows/affinity.patch`).
1. Run `./autogen`.
1. Run `./cfg-windows --prefix=/ --enable-relocatable-install --with-usb-package=winusb`.
1. Build BRLTTY with `make`.
1. Isolate `brlapi.cp313-win_amd64.pyd` and `brlapi-*.dll` from the build to the `python` folder in this repository.
  * The `pyd` file resides in `Bindings/Python/dist`.
  * The `dll` file resides in `programs`.

## lilli.dll

Braille display driver dll for the [Lilli display from MDV](https://www.mdvbologna.it/).
For updates, contact [info@mdvbologna.it](mailto:info@mdvbologna.it).

## tools

### gettext

1. Download the latest "static" 32bit zip for Windows from [here](https://mlocati.github.io/articles/gettext-iconv-windows.html)
1. Extract the zip
1. Update the following files from `bin`
    - `msgfmt.exe`
    - `xgettext.exe`

### M4

M4 is necessary to compile liblouis tables containing macros.

1. From [here](https://gnuwin32.sourceforge.net/packages/m4.htm), download the "Binaries" and "Dependencies" zip files
1. From the "Binaries" zip, extract the file `m4.exe` from `bin`
1. From the "Dependencies" zip, extract the `regex2.dll` file from `bin`
