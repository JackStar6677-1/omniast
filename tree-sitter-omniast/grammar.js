/**
 * Tree-sitter grammar definition for OmniAST / GraphLang (.omni, .omniast)
 * Designed for AI agents, language servers, and high-performance AST parsing.
 */

module.exports = grammar({
  name: 'omniast',

  extras: $ => [
    /\s/,
    $.comment,
  ],

  rules: {
    source_file: $ => repeat($._definition),

    _definition: $ => choice(
      $.module_definition,
      $.entity_definition,
      $.listener_definition,
      $.sentinel_definition,
      $.machine_definition,
      $.pipeline_definition,
      $.service_definition
    ),

    comment: $ => choice(
      seq('#', /.*/),
      seq('//', /.*/),
      seq('/*', /[^*]*\*+([^/*][^*]*\*+)*/, '/')
    ),

    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_]*/,
    qualified_identifier: $ => seq($.identifier, repeat(seq('.', $.identifier))),

    string_literal: $ => choice(
      seq('"', repeat(choice(/[^"\\]/, seq('\\', /./))), '"'),
      seq("'", repeat(choice(/[^'\\]/, seq('\\', /./))), "'")
    ),

    number_literal: $ => /\d+(\.\d+)?/,
    duration_literal: $ => /\d+[smhdw]/,
    unit_literal: $ => seq(/\d+(\.\d+)?/, choice('J', 'J/s', 'B', 'KB', 'MB', 'GB', 'TB', 'ops', 'req/s', 'tps')),
    boolean_literal: $ => choice('true', 'false'),

    type_identifier: $ => choice(
      'string',
      'int',
      'long',
      'float',
      'double',
      'decimal',
      'boolean',
      'uuid',
      'item',
      'location',
      'actor',
      'entity',
      'event',
      'duration',
      seq('list', '<', $.type_identifier, '>'),
      seq('map', '<', $.type_identifier, ',', $.type_identifier, '>'),
      $.identifier
    ),

    // Module
    module_definition: $ => seq(
      'module',
      field('name', $.identifier),
      field('body', $.module_body)
    ),

    module_body: $ => seq(
      '{',
      repeat(choice(
        $.property_assignment,
        $._definition
      )),
      '}'
    ),

    property_assignment: $ => seq(
      field('key', $.identifier),
      ':',
      field('value', $._expression)
    ),

    // Entity
    entity_definition: $ => seq(
      'entity',
      field('name', $.identifier),
      optional(seq(':', field('supertype', $.identifier))),
      field('body', $.entity_body)
    ),

    entity_body: $ => seq(
      '{',
      repeat(choice(
        $.field_definition,
        $.property_assignment
      )),
      '}'
    ),

    field_definition: $ => seq(
      field('name', $.identifier),
      ':',
      field('type', $.type_identifier),
      repeat($.field_modifier)
    ),

    field_modifier: $ => choice(
      'primary',
      'unique',
      'required',
      seq('default', '(', $._expression, ')'),
      seq('max', '(', $.number_literal, ')'),
      seq('persist', ':', $.function_call)
    ),

    // Listener
    listener_definition: $ => seq(
      'listener',
      field('name', $.identifier),
      'on',
      field('event', $.qualified_identifier),
      optional(seq('priority', '(', field('priority', $.identifier), ')')),
      field('body', $.block)
    ),

    // Sentinel (Autonomous SRE Watcher)
    sentinel_definition: $ => seq(
      'sentinel',
      field('name', $.identifier),
      field('body', $.sentinel_body)
    ),

    sentinel_body: $ => seq(
      '{',
      repeat(choice(
        $.property_assignment,
        $.on_event_clause
      )),
      '}'
    ),

    on_event_clause: $ => seq(
      'on',
      field('trigger', $.identifier),
      optional(seq('(', field('argument', $.identifier), ')')),
      field('body', $.block)
    ),

    // Machine / Industrial Actor
    machine_definition: $ => seq(
      'machine',
      field('name', $.identifier),
      optional(seq(':', field('trait', $.identifier))),
      field('body', $.machine_body)
    ),

    machine_body: $ => seq(
      '{',
      repeat(choice(
        $.property_assignment,
        $.on_event_clause
      )),
      '}'
    ),

    // Pipeline / Distributed Stream
    pipeline_definition: $ => seq(
      'pipeline',
      field('name', $.identifier),
      field('body', $.block)
    ),

    // Service / Microservice
    service_definition: $ => seq(
      'service',
      field('name', $.identifier),
      field('body', $.block)
    ),

    // Blocks & Statements
    block: $ => seq(
      '{',
      repeat($._statement),
      '}'
    ),

    _statement: $ => choice(
      $.guard_statement,
      $.cancel_statement,
      $.route_statement,
      $.notify_statement,
      $.alert_statement,
      $.log_statement,
      $.if_statement,
      $.assignment_statement,
      $.expression_statement
    ),

    guard_statement: $ => seq(
      'guard',
      field('condition', $._expression)
    ),

    cancel_statement: $ => 'cancel',

    route_statement: $ => seq(
      'route',
      field('source', $._expression),
      '->',
      field('destination', $._expression),
      optional(seq(',', 'max', '=', $._expression))
    ),

    notify_statement: $ => seq(
      'notify',
      field('target', $.qualified_identifier),
      ',',
      field('message', $._expression)
    ),

    alert_statement: $ => seq(
      'alert',
      '(',
      sepBy(',', $.named_argument),
      ')'
    ),

    log_statement: $ => seq(
      'log',
      field('message', $._expression)
    ),

    if_statement: $ => seq(
      'if',
      field('condition', $._expression),
      field('consequence', $.block),
      optional(seq('else', field('alternative', choice($.if_statement, $.block))))
    ),

    assignment_statement: $ => seq(
      field('left', choice($.identifier, $.field_access)),
      '=',
      field('right', $._expression)
    ),

    expression_statement: $ => $._expression,

    // Expressions
    _expression: $ => choice(
      $.identifier,
      $.qualified_identifier,
      $.string_literal,
      $.number_literal,
      $.duration_literal,
      $.unit_literal,
      $.boolean_literal,
      $.array_literal,
      $.field_access,
      $.function_call,
      $.binary_expression,
      $.unary_expression,
      $.parenthesized_expression
    ),

    array_literal: $ => seq(
      '[',
      sepBy(',', $._expression),
      ']'
    ),

    field_access: $ => seq(
      field('object', $._expression),
      '.',
      field('field', $.identifier)
    ),

    function_call: $ => seq(
      field('function', choice($.identifier, $.qualified_identifier, $.field_access)),
      '(',
      optional(sepBy(',', choice($._expression, $.named_argument))),
      ')'
    ),

    named_argument: $ => seq(
      field('name', $.identifier),
      '=',
      field('value', $._expression)
    ),

    binary_expression: $ => prec.left(1, seq(
      field('left', $._expression),
      field('operator', choice('+', '-', '*', '/', '==', '!=', '<', '<=', '>', '>=', '&&', '||')),
      field('right', $._expression)
    )),

    unary_expression: $ => prec(2, seq(
      field('operator', choice('!', '-')),
      field('argument', $._expression)
    )),

    parenthesized_expression: $ => seq('(', $._expression, ')')
  }
});

function sepBy(sep, rule) {
  return optional(sepBy1(sep, rule));
}

function sepBy1(sep, rule) {
  return seq(rule, repeat(seq(sep, rule)));
}
