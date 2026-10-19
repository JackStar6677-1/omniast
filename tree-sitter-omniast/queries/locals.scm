;; Scopes and Local variable resolution for OmniAST
(module_definition) @scope
(entity_definition) @scope
(listener_definition) @scope
(sentinel_definition) @scope
(machine_definition) @scope
(block) @scope

(field_definition name: (identifier) @definition.var)
(named_argument name: (identifier) @definition.parameter)
(identifier) @reference
