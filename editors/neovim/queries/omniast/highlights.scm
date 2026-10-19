;; Neovim Treesitter queries for OmniAST / GraphLang
;; Place in your runtimepath: queries/omniast/highlights.scm

[
  "module"
  "entity"
  "listener"
  "sentinel"
  "machine"
  "pipeline"
  "service"
] @keyword.function

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
] @type.qualifier

(string_literal) @string
(number_literal) @number
(duration_literal) @number.float
(unit_literal) @number.float
(boolean_literal) @boolean

(type_identifier) @type
(entity_definition name: (identifier) @type.definition)
(module_definition name: (identifier) @namespace)

(function_call function: (identifier) @function.call)
(function_call function: (field_access field: (identifier) @function.call))
(on_event_clause trigger: (identifier) @function.method)

(property_assignment key: (identifier) @property)
(field_definition name: (identifier) @variable.member)
(field_access field: (identifier) @variable.member)
(named_argument name: (identifier) @variable.parameter)

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

["(" ")" "{" "}" "[" "]" "<" ">"] @punctuation.bracket
["," "."] @punctuation.delimiter

(comment) @comment
