def upload(self, tool: Tool) -> bool:
        
        return self.__installation.build.upload(tool.image)