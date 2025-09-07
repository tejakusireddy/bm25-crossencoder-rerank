def get_manager_cmd(self):
        """"""
        cmd = os.path.abspath(os.path.join(os.path.dirname(__file__), "server", "notebook_daemon.py"))
        assert os.path.exists(cmd)
        return cmd