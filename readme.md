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
  - `brlapi.cp3**-amd64.pyd`
  - `brlapi-*.dll`

To get these files, you can extract them from the build artifact produced by [GitHub Actions in de brlTTY repository](https://github.com/brltty/brltty/actions).

#### Building from source

If BRLTTY doesn't have a public release compatible with NVDA's python version, you must build it from source.

The GitHub actions workflow in the above mentioned repository can be adapted according to what's necessary to build a proper version.

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

### M4

M4 is necessary to compile liblouis tables containing macros.

1. From [here](https://gnuwin32.sourceforge.net/packages/m4.htm), download the "Binaries" and "Dependencies" zip files
1. From the "Binaries" zip, extract the file `m4.exe` from `bin`
1. From the "Dependencies" zip, extract the `regex2.dll` file from `bin`

### symbols

1. Download the latest [`dump_syms.exe`](https://github.com/mozilla/gecko-dev/blob/master/toolkit/crashreporter/google-breakpad/src/tools/windows/binaries/dump_syms.exe) ([last known version](https://github.com/mozilla/gecko-dev/blob/b0e9d95a41068be0f41f30e632ef93ab5999767a/toolkit/crashreporter/google-breakpad/src/tools/windows/binaries/dump_syms.exe))
1. Replace `dump_syms.exe`
