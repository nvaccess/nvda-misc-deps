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
The following files are required: ISimpleDOM.idl, ISimpleDOMNode.idl, iSimpleDOMDocument.idl and iSimpleDOMText.idl.

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

1. Download the latest `brltty-win-X.X-libusb.zip` from the [BrlTTY website](https://brltty.app/download.html) (not the 1.0 variant).
This is the 32bit version.
1. Extract the zip.
1. Update the following files
    - `brlapi.cp38-win32.pyd` from `brltty-win-X.X-0-libusb\Python\Lib\site-packages\brlapi.cp38-win32.pyd`
    - `libgcc_s_dw2-1.dll` from `brltty-win-X.X-0-libusb\bin\libgcc_s_dw2-1.dll`
    - `brlapi-0.8.dll` from `brltty-win-X.X-0-libusb\brltty-win-6.6-0-libusb\bin\brlapi-0.8.dll`

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
