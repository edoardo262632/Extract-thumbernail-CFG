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


        # Added code to the library class to render the blocks
        loop = False
        lens = 0
        lenp = 0
        # Examinate all the predecessor inside the function to control if a loop could be present
        for x in node.predecessors:
            if node.function_address != x.function_address:
                    continue
            if x.addr >= node.addr:
                loop = True
            lenp += 1
        # Count the successor inside the same function
        for x in node.successors:
            if node.function_address != x.function_address:
                    continue
            lens += 1
        # Retrives the loops that start from the exit condition after the loop block
        if lens > 1 and not loop:
            for x in node.successors:
                if node.function_address == x.function_address:
                    if node.addr > x.addr:
                        loop = True
                        
        if insns[len(insns)-1].mnemonic == "ret":
            n.fillcolor = 'black'
            n.style = "filled"
        elif lenp > 1 and loop:
            #Color of the loop
            n.fillcolor = 'blue'
            n.style = "filled"
        elif lens == 1:
            #Color of transition blocks
            n.fillcolor = 'green'
            n.style = "filled"
        elif lens > 1:
            #Color of block if blocks
            n.fillcolor = 'yellow'
            n.style = "filled"
        elif insns[len(insns)-1].mnemonic == "call":
            n.fillcolor = 'red'
            n.style = "filled"
        else:
            n.fillcolor = 'purple'
            n.style = "filled"


#Library function needed to call our implementation of the class AngrAsm and to color the graph
def plot_cfg(cfg, fname, format="png", func_addr=None):
    vis = AngrVisFactory().default_cfg_pipeline(cfg, asminst=False, vexinst=False, comments=False)
    project = cfg.project
    # Remove the imports from the graph
    vis.add_transformer(AngrRemoveImports(cfg.project))

    #Select only the node of the graph related to the analyzed function
    vis.add_transformer(AngrFilterNodes(lambda node: node.obj.function_address in func_addr and func_addr[node.obj.function_address]))

    #Add a member of the customized class
    vis.add_content(AngrAsm(project))
    if project.arch.name in ('ARM', 'ARMEL', 'ARMHF'):
        vis.add_edge_annotator(AngrColorEdgesAsmArm())
    elif project.arch.name in ('X86', 'AMD64'):
        vis.add_edge_annotator(AngrColorEdgesAsmX86())
    else:
        vis.add_edge_annotator(AngrColorEdgesVex())
    vis.set_output(DotOutput(fname, format=format))
    vis.process(cfg.graph)
