# Neovim Support for OmniAST / GraphLang

OmniAST integrates natively with Neovim using `nvim-treesitter`.

## Installation & Setup

1. Copy or symlink `queries/omniast/highlights.scm` to your Neovim config runtimepath:
   ```bash
   mkdir -p ~/.config/nvim/queries/omniast
   cp queries/omniast/highlights.scm ~/.config/nvim/queries/omniast/
   ```

2. Register the OmniAST parser in your `init.lua`:
   ```lua
   local parser_config = require("nvim-treesitter.parsers").get_parser_configs()
   parser_config.omniast = {
     install_info = {
       url = "https://github.com/JackStar6677-1/omniast",
       files = { "tree-sitter-omniast/src/parser.c" },
       branch = "main",
     },
     filetype = "omniast",
   }

   vim.filetype.add({
     extension = {
       omni = "omniast",
       omniast = "omniast",
       glang = "omniast",
     },
   })
   ```

3. Enjoy real-time, high-precision AST highlighting, folding, and indentation!
