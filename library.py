import networkx

from collections import defaultdict

from bingraphvis import *
from bingraphvis.angr import *
from bingraphvis.angr.x86 import *



def render_content(self, c):
    void(c)
    return

class AngrAsm(Content):
    def __init__(self, project):
        super(AngrAsm, self).__init__('asm', ['addr', 'mnemonic', 'operands'])
        self.project = project



    def gen_render(self, n):
        node = n.obj

        #CFG
        if type(node).__name__ == 'CFGNode' or type(node).__name__ == 'CFGNodeA' or type(node).__name__ == 'CFGENode':
            is_syscall = node.is_syscall
            is_simprocedure = node.is_simprocedure
            addr = node.addr
            size = None
            max_size = node.size

        if is_simprocedure or is_syscall:
            return None
        try:
            insns = self.project.factory.block(addr=addr, size=max_size, num_inst=size).capstone.insns
        except Exception as e:
            print(e)
            #TODO add logging
            insns = []

        data = []
        for ins in insns:
            data.append({
                'addr': {
                    'content': "0x%08x:\t" % ins.address,
                    'align': 'LEFT'
                },
                'mnemonic': {
                    'content': ins.mnemonic,
                    'align': 'LEFT'
                },
                'operands': {
                    'content': ins.op_str,
                    'align': 'LEFT'
                },
                '_ins': ins,
                '_addr': ins.address,
            })

        loop = False
        lens = 0
        lenp = 0
        for x in node.predecessors:
            if node.function_address != x.function_address:
                    continue
            if x.addr >= node.addr:
                loop = True
            lenp += 1
        for x in node.successors:
            if node.function_address != x.function_address:
                    continue
            lens += 1

        if lenp >= 2 and loop:
            n.fillcolor = 'blue'
            n.style = "filled"
        elif lens == 0:
            n.fillcolor = 'red'
            n.style = "filled"
        elif lens == 1:
            n.fillcolor = 'green'
            n.style = "filled"
        else:
            n.fillcolor = 'yellow'
            n.style = "filled"


def plot_cfg(cfg, fname, format="png", state=None, asminst=False, vexinst=False, func_addr=None, remove_imports=True, remove_path_terminator=True, remove_simprocedures=False, debug_info=False, comments=True, color_depth=False):
    vis = AngrVisFactory().default_cfg_pipeline(cfg, asminst=asminst, vexinst=vexinst, comments=comments)
    project = cfg.project
    if remove_imports:
        vis.add_transformer(AngrRemoveImports(cfg.project))
    if remove_simprocedures:
        vis.add_transformer(AngrRemoveSimProcedures())
    if func_addr:
        vis.add_transformer(AngrFilterNodes(lambda node: node.obj.function_address in func_addr and func_addr[node.obj.function_address]))
    vis.add_clusterer(ColorDepthClusterer(palette='greens'))
    vis.add_content(AngrAsm(project))
    if project.arch.name in ('ARM', 'ARMEL', 'ARMHF'):
        vis.add_edge_annotator(AngrColorEdgesAsmArm())
    elif project.arch.name in ('X86', 'AMD64'):
        vis.add_edge_annotator(AngrColorEdgesAsmX86())
    else:
        vis.add_edge_annotator(AngrColorEdgesVex())
    vis.set_output(DotOutput(fname, format=format))
    vis.process(cfg.graph)
