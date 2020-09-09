# ipautil

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/aktsk/ipautil/blob/master/LICENSE)

`ipautil` is a useful utility for mobile security testing.
It is a wrapper for `codesign` commands.
I've only checked it works on macOS.

## Installation
Since `ipautil` is implemented in Python, it can be installed with the pip command, which is a Python package management system.

```
$ pip install git+ssh://git@github.com/aktsk/ipautil.git
```

Also, place `~/ipautil.json` containing the sign information necessary for signing IPA in your home directory.

```
{
    "entitlements-plist": "/hoge/entitlements.plist",
    "embedded-mobileprovision": "/fuga/embedded.mobileprovision"
}
```

## Usage
The command outputs are displayed in color. You can use a function with subcommands.

### subcommands
Most of the subcommands are assigned with alias, which is useful.

### decode
`decode` subcommand make the IPA decode.

```
$ ipautil decode sample.ipa
```

### build
`build` subcommand make the IPA build.
It also sign the IPA by codesign before the build is complete.

```
$ ipautil build Payload
```

### sign
`sign` subcommand make the IPA sign by codesign.

```
$ ipautil sign sample.ipa
```

## License
MIT License
