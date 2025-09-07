def get_html_content(self):
        

        # Extract full element node content (including subelements)
        html_content = ''
        if hasattr(self, 'xml_element'):
            xml = self.xml_element
            content_list = ["" if xml.text is None else xml.text]

            def to_string(xml):
                if isinstance(xml, _Comment):
                    return str(xml)
                else:
                    return ElementTree.tostring(xml).decode('utf-8')

            content_list += [to_string(e) for e in xml.getchildren()]

            full_xml_content = "".join(content_list)

            # Parse tags to generate HTML valid content
            first_regex = r'html:'
            second_regex = r' xmlns:html=(["\'])(?:(?=(\\?))\2.)*?\1'
            html_content = re.sub(first_regex, '',
                                  re.sub(second_regex, '', full_xml_content))

        return html_content