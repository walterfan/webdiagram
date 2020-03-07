from portal import logger
from jinja2 import Template
import os
import re

from graphviz import Source

dir_path = os.path.dirname(os.path.realpath(__file__))


def parse_node_desc(node_desc, lhs='(', rhs=')'):
    node_desc = node_desc.strip()
    pos1 = node_desc.find(lhs)
    if pos1 > 0:
        node_name = node_desc[:pos1]
        node_attr = node_desc[pos1 + 1:].rstrip(rhs)
        if '=' in node_attr:
            pass
        else:
            node_attr = 'label="{}"'.format(node_attr.strip('" '))
    else:
        node_name = node_desc
        node_attr = ""

    print("name={}, attr={}".format(node_name, node_attr))
    return node_name, node_attr


def node_set_desc(node_set):
    node_desc_list = []

    for node_desc in node_set:
        if '(' in node_desc:
            node_name, node_attr = parse_node_desc(node_desc)
        else:
            node_name, node_attr = parse_node_desc(node_desc, '[', ']')

        if node_attr:
            node_desc_list.append('\t{}[{}];'.format(node_name, node_attr))
        elif node_name.lower().startswith('is') or node_name.lower().startswith('if'):
            node_desc_list.append('\t{}[shape = "diamond", style = ""];'.format(node_name))
        elif node_name.lower() == 'start':
            node_desc_list.append('\t{}[shape = "circle", style = filled, color = lightgrey];'.format(node_name))
        elif node_name.lower() == 'end':
            node_desc_list.append('\t{}[shape = "circle", style = filled, color = lightgrey];'.format(node_name))

    return '\n'.join(node_desc_list)


class Painter(object):
    def __init__(self, diagram_name, directed=True):
        super().__init__()
        self.name = diagram_name
        self.path = ""
        self.content = None
        self.directed = False
        self.separator = '->'
        self.tplName = None

        self.set_directed(directed)

    def set_directed(self, direction):
        self.directed = direction
        if self.directed:
            self.separator = '->'
            self.tplName = dir_path + "/../templates/digraph.j2"
        else:
            self.separator = '--'
            self.tplName = dir_path + "/../templates/graph.j2"

    def dot_to_png(self, dot_content, png_file, **kwargs):
        logger.info("dot_to_png from {} to {}".format(dot_content, png_file))
        basename = png_file[:-4]
        with open(basename + '.txt', "w") as fp:
            fp.write(dot_content)
        src = Source(dot_content)
        file_path = src.render(filename=basename, format='png')
        return os.path.basename(file_path)

    def draw_graph(self, script):

        logger.info("script: {}, sep: {}".format(script, self.separator))
        title = ""

        node_set = set()
        node_list = []
        for line in script.strip().split('\n'):
            line = line.strip("; \t\r\n")
            if len(line) == 0:
                continue

            if line.startswith('title'):
                title = line.replace('title', '').strip(': ')

            if line.startswith('node'):
                node_set.add(line.replace('node', '').strip(': '))

            if self.separator not in line:
                continue
            logger.info("process line: {}".format(line))
            arr = line.split(self.separator)
            for node_desc in arr:
                pos = node_desc.find('[')
                if pos > 0:
                    node_desc = node_desc[:pos]

                node_set.add(node_desc.strip("; "))
            line = re.sub(r'\([^-]*\)', '', line)
            line = line.replace('cond=', 'label=')
            line = line.replace('\'', '"')
            node_list.append('\t{};'.format(line))

        parameters = {'diagram_name': title or "",
                      'diagram_desc': node_set_desc(node_set),
                      'diagram_content': '\n'.join(node_list)}

        with open(self.tplName, "r") as tpl_file:
            template = Template(tpl_file.read())
            dot_content = template.render(parameters)
            if self.name and self.name.endswith(".png"):
                png_file = "{}/{}".format(self.path, self.name)
                return self.dot_to_png(dot_content, png_file)
            else:
                self.content = dot_content.replace('\n', '')
                return ""

    def draw_uml(self, script_content):

        script_file = "{}/{}".format(self.path, self.name)
        if script_file.endswith(".png"):
            script_file = script_file[:-4] + ".txt"

        with open(script_file, "w") as fp:
            fp.write("@startuml\n{}\n@enduml\n".format(script_content.replace('\r\n', '\n')))

        logger.info("draw %s" % script_file)
        cmd = "java -jar plantuml.jar %s" % script_file
        logger.info("execute {}".format(cmd))
        os.system(cmd)
        return os.path.basename(script_file)[:-4] + ".png"
