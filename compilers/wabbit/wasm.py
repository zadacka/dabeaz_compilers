# wasm.py
#
# This file emits Wasm code from IR code.  To do this, you must first
# work through the Wasm encoding example found in Docs/codegen.html.
# Take the code from that example and copy it in here.  You will then
# adapt it to work with Wabbit.
#
# Specific changes/extensions you will need to address:
#
# 1. Floating point operations.
# 2. Comparisons and relations.
# 3. Support for local variables (load/store).
# 4. Control flow (if, while, etc.)
# 5. Additional runtime functions (_printf, _printb).
# 6. Memory management (eventually)
#
# Most of the hard work of encoding should have been completed in the
# Docs/codegen.html example.  You'll mostly be adding support for more
# opcodes and patching things up to bridge IR Code with the Wasm
# encoder.  



