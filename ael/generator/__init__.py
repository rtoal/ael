from ael.generator.js import generate_js
from ael.generator.c import generate_c
from ael.generator.llvm import generate_llvm

generate = {
    'js': generate_js,
    'c': generate_c,
    'llvm': generate_llvm}
