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

### mathPlayer

Project has been abandoned, updates are unlikely.
This will be abandoned in NVDA in favour of MathCAT, once MathCAT contains all functionality of MathPlayer. 

## python

### ftdi2

Needed for papenmeier displays.
Should be replaced with [pyftdi](https://github.com/eblot/pyftdi) as a pip dependency.
This will require a significant rewrite of the papenmeier display driver.

### brlapi

Used for BrlTTY.

This requires updating the following files:
  - `brlapi.cp311-win32.pyd` from `brltty-win-X.X-0-libusb\Python\Lib\site-packages\brlapi.cp11-win32.pyd`
  - `libgcc_s_dw2-1.dll` from `brltty-win-X.X-0-libusb\bin\libgcc_s_dw2-1.dll`
  - `brlapi-*.dll` from `brltty-win-X.X-0-libusb\brltty-win-6.6-0-libusb\bin\brlapi-*.dll`

To get `brltty-win-X.X-0-libusb` you must either build it from source or download it from the [BrlTTY website](https://brltty.app/download.html) (not the 1.0 variant).

#### Building from source

If BRLTTY doesn't have a public release compatible with NVDA's python version, you must build it from source.

Use the following steps to build a version of the brlapi Python extension that is compatible with a particular version of Python:

1. Download [mingw-get](https://sourceforge.net/projects/mingw/files/latest/download)
1. Open the setup and choose "Install"
1. Ensure support for the graphical interface is enabled, and choose "Continue"
1. After the installation, choose "Continue" again
1. In the tree view that is shown, select "Basic setup"
1. Select the following mingw packages. Note that you might require object navigation and mouse routing to do this. You can select a package by right clicking it and choose "Mark for installation":
	- mingw-developer-toolkit	
	- mingw32-base
	- mingw32-gcc-g++
	- msys-base
1. Open the installation menu from the menu bar and choose "Apply changes"
1. Close mingw-get after installation
1. Checkout [the BRLTTY repository](https://github.com/brltty/brltty)
1. Start msys1 as administrator: `"C:\MinGW\msys\1.0\msys.bat"`
1. Move to the BRLTTY repository with the `cd` command
1. Run `Windows/winsetup`. ***Important note:** This script installs several packages to your C drive. Investigate the winsetup script for more details*
1. Restart msys1 and go back to the repository.
1. Run `./autogen`
1. Run `Windows/mkwin ./`
1. When the build has finished, there will be a zip file in the repository, e.g. "brltty-win-*-libusb.zip"
1. Extract the zip.
1. Update the following files
    - `brlapi.cp311-win32.pyd` from `brltty-win-X.X-0-libusb\Python\Lib\site-packages\brlapi.cp11-win32.pyd`
    - `libgcc_s_dw2-1.dll` from `brltty-win-X.X-0-libusb\bin\libgcc_s_dw2-1.dll`
    - `brlapi-*.dll` from `brltty-win-X.X-0-libusb\brltty-win-6.6-0-libusb\bin\brlapi-*.dll`

### txt2tags

Used to generate and format NVDA documentation.
Will be abandoned soon in favour of markdown formatting.

## lilli.dll

A braille display driver dll.
Update process unknown.

## tools

### gettext

1. Download the latest "static" 32bit zip for Windows from [here](https://mlocati.github.io/articles/gettext-iconv-windows.html)
1. Extract the zip
1. Update the following files from `bin`
    - `msgfmt.exe`
    - `xgettext.exe`

### symbols

1. Download the latest [`dump_syms.exe`](https://github.com/mozilla/gecko-dev/blob/master/toolkit/crashreporter/google-breakpad/src/tools/windows/binaries/dump_syms.exe) ([last known version](https://github.com/mozilla/gecko-dev/blob/b0e9d95a41068be0f41f30e632ef93ab5999767a/toolkit/crashreporter/google-breakpad/src/tools/windows/binaries/dump_syms.exe))
1. Replace `dump_syms.exe`
