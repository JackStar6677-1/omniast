;; Syntax Highlighting Queries for OmniAST / GraphLang

;; Keywords & Declarations
[
  "module"
  "entity"
  "listener"
  "sentinel"
  "machine"
  "pipeline"
  "service"
] @keyword.declaration

[
  "on"
  "priority"
  "guard"
  "cancel"
  "route"
  "notify"
  "alert"
  "log"
  "if"
  "else"
] @keyword

[
  "primary"
  "unique"
  "required"
  "default"
  "max"
  "persist"
] @keyword.modifier

;; Literals
(string_literal) @string
(number_literal) @number
(duration_literal) @number.duration
(unit_literal) @number.unit
(boolean_literal) @boolean

;; Types
(type_identifier) @type
(entity_definition name: (identifier) @type.definition)
(module_definition name: (identifier) @namespace)

;; Functions and Calls
(function_call function: (identifier) @function.call)
(function_call function: (field_access field: (identifier) @function.call))
(on_event_clause trigger: (identifier) @function.method)

;; Properties & Fields
(property_assignment key: (identifier) @property)
(field_definition name: (identifier) @variable.member)
(field_access field: (identifier) @variable.member)
(named_argument name: (identifier) @variable.parameter)

;; Operators
[
  "="
  "->"
  ":"
  "+"
  "-"
  "*"
  "/"
  "=="
  "!="
  "<"
  "<="
  ">"
  ">="
  "&&"
  "||"
  "!"
] @operator

;; Punctuation
["(" ")" "{" "}" "[" "]" "<" ">"] @punctuation.bracket
["," "."] @punctuation.delimiter

;; Comments
(comment) @comment
