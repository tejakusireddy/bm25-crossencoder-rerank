def to_file(self, filename=None, write_style=True):
        
        out = zipwrap.Zippier(filename, "w")
        out.write("mimetype", self.mime_type)
        for p in self._pictures:
            out.write("Pictures/%s" % p.internal_name, p.get_data())
        out.write("content.xml", self.to_xml())
        if write_style:
            out.write("styles.xml", self.styles_xml())
        out.write("meta.xml", self.meta_xml())
        out.write("settings.xml", self.settings_xml())
        out.write("META-INF/manifest.xml", self.manifest_xml(out))
        return out