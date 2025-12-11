# ShareQL: A domain specific language to provide rule matching in network shares exploration

<p align="center">
  A Domain Specific Language to control access to files, directories, and shares in network shares crawling
  <br>
  <img alt="PyPI" src="https://img.shields.io/pypi/v/shareql">
  <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/p0dalirius/shareql">
  <a href="https://twitter.com/intent/follow?screen_name=podalirius_" title="Follow"><img src="https://img.shields.io/twitter/follow/podalirius_?label=Podalirius&style=social"></a>
  <a href="https://www.youtube.com/c/Podalirius_?sub_confirmation=1" title="Subscribe"><img alt="YouTube Channel Subscribers" src="https://img.shields.io/youtube/channel/subscribers/UCF_x5O7CSfr82AfNVTKOv_A?style=social"></a>
</p>

## Features

- **Rule-based Access Control**: Define complex rules for share crawling to control access to files, directories, and shares
- **Flexible Conditions**: Support for multiple operators including `MATCHES`, `IN`, comparison operators, and regex patterns
- **Boolean Logic**: Combine conditions with `AND`, `OR`, `XOR`, and `NOT` operators
- **Multiple Object Types**: Rules apply to files, directories, and shares based on their properties
- **Field-based Filtering**: Filter based on element size, name, path, modification time, creation time, and more
- **Operation Control**: Control specific operations like `PROCESSING` and `EXPLORATION`
- **Syntax Highlighting**: Syntax highlighting for this langugage is provided in VSCode by the extension [shareql-vscode-ext](https://github.com/p0dalirius/shareql-vscode-ext)

## Installation

You can get the latest version from pypi:

```bash
pip install shareql
```

Or you can build it from source:

```
git clone https://github.com/p0dalirius/shareql
cd shareql
make install
```

## Language Syntax

ShareQL uses a simple but powerful syntax for defining access rules:

### Basic Rule Structure

```
ACTION [OPERATION] [IF condition]
```

- **ACTION**: `ALLOW` or `DENY`
- **OPERATION**: `ALL`, `PROCESSING`, or `EXPLORATION` (optional)
- **condition**: Boolean expression using available fields and operators

### Available Fields

**File Fields:**
- `FILE.SIZE` - File size in bytes
- `FILE.NAME` - File name
- `FILE.PATH` - Full file path
- `FILE.MODIFIED_AT` - Last modification timestamp
- `FILE.CREATED_AT` - Creation timestamp

**Directory Fields:**
- `DIRECTORY.PATH` - Full directory path
- `DIRECTORY.NAME` - Directory name
- `DIRECTORY.MODIFIED_AT` - Last modification timestamp
- `DIRECTORY.CREATED_AT` - Creation timestamp

**Share Fields:**
- `SHARE.NAME` - Share name
- `SHARE.DESCRIPTION` - Share description
- `SHARE.TYPE` - Share type

**Other Fields:**
- `DEPTH` - Directory depth level

### Operators

- `MATCHES` - String matching
- `IN` - Check if value is in a list
- `>=`, `<=`, `>`, `<`, `==` - Comparison operators
- `STARTSWITH` - String starts with pattern
- `ENDSWITH` - String ends with pattern
- `CONTAINS` - String contains pattern

### Values

- **Strings**: `"quoted string"` or `'single quoted'`
- **Numbers**: `1234`
- **Lists**: `["item1", "item2", "item3"]`
- **Regex**: `REGEX("pattern.*")`

## Examples

### Basic Rules

```shareql
# Deny all access
DENY ALL

# Allow file processing
ALLOW PROCESSING

# Deny directory exploration
DENY EXPLORATION
```

### Conditional Rules

```shareql
# Deny processing of backup files
DENY PROCESSING IF FILE.PATH MATCHES "backup"

# Allow only small files
ALLOW PROCESSING IF FILE.SIZE <= 1000

# Deny access to admin directories
DENY EXPLORATION IF DIRECTORY.NAME MATCHES "admin"
```

### Complex Conditions

```shareql
# Deny large backup files
DENY PROCESSING IF FILE.PATH MATCHES "backup" AND FILE.SIZE >= 1000

# Allow specific file types
ALLOW PROCESSING IF FILE.NAME ENDSWITH ".pdf" OR FILE.NAME ENDSWITH ".docx"

# Deny files in specific directories
DENY PROCESSING IF FILE.PATH STARTSWITH "C:/temp" AND FILE.SIZE >= 500

# Allow files not in restricted list
ALLOW PROCESSING IF NOT FILE.NAME IN ["backup.exe", "temp.dll"]
```

### Regex Patterns

```shareql
# Deny files matching regex pattern
DENY PROCESSING IF FILE.PATH MATCHES REGEX(".*\\.(zip|rar|7z)$")

# Allow files with specific naming pattern
ALLOW PROCESSING IF FILE.NAME MATCHES REGEX("^report_[0-9]{4}\\.pdf$")
```

### Nested Boolean Logic

```shareql
# Complex nested conditions
ALLOW PROCESSING IF ((FILE.PATH MATCHES "documents" AND FILE.SIZE <= 1000) OR (FILE.PATH MATCHES "images" AND FILE.SIZE <= 5000))

# Multiple directory restrictions
DENY EXPLORATION IF (DIRECTORY.NAME MATCHES "private" OR DIRECTORY.PATH MATCHES "C:/system") AND NOT DIRECTORY.MODIFIED_AT < 1670000000
```

## Usage

### Python API

```python
from shareql.grammar.parser import RuleParser
from shareql.evaluate.evaluator import RulesEvaluator

# Parse rules from text
parser = RuleParser()
rules, errors = parser.parse("""
DENY PROCESSING IF FILE.SIZE >= 1000
ALLOW EXPLORATION IF DIRECTORY.NAME MATCHES "public"
""")

# Create evaluator
evaluator = RulesEvaluator(rules)

# Evaluate against target objects
# (target_object should be a RuleObjectFile, RuleObjectDirectory, or RuleObjectShare)
rule, allowed, result = evaluator.evaluate(target_object)
```

### Example of usage

Parse and validate rules file

```bash
# Parse and validate rules file
shareql --rules rules.txt --validate
```

## Contributing

Pull requests are welcome. Feel free to open an issue if you want to add other features.
