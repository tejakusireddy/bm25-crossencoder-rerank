def depart_heading(self, _):
        
        assert isinstance(self.current_node, nodes.title)
        # The title node has a tree of text nodes, use the whole thing to
        # determine the section id and names
        text = self.current_node.astext()
        if self.translate_section_name:
            text = self.translate_section_name(text)
        name = nodes.fully_normalize_name(text)
        section = self.current_node.parent
        section['names'].append(name)
        self.document.note_implicit_target(section, section)
        self.current_node = section