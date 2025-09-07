function list(scriptModule, agent, msg, cb) {
    const servers = [];
    const scripts = [];
    const idMap = agent.idMap;

    for (const sid in idMap) {
        if (idMap.hasOwnProperty(sid)) {
            servers.push(sid);
        }
    }

    fs.readdir(scriptModule.root, (err, filenames) => {
        if (err) {
            filenames = [];
        }
        for (let i = 0, l = filenames.length; i < l; i++) {
            scripts.push(filenames[i]);
        }

        cb(null, {
            servers: servers,
            scripts: scripts
        });
    });
}