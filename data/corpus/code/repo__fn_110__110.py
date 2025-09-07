function readFile(path, fileName) {
  return new Promise((resolve, reject) => {
    fs.readFile(`${path}/${fileName}`, 'utf8', (err, content) => {
      if (err) {
        return reject(err)
      }

      return resolve(content)
    })
  })
}