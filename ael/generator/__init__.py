import ael.generator.js as js
import ael.generator.c as c
import ael.generator.llvm as llvm

generate = {
    'js': js.generate,
    'c': c.generate,
    'llvm': llvm.generate}
