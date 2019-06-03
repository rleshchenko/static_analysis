const fs = require('fs');
const path = require('path');

const dir = '/Users/roman.krasinskyi/Work/cloud-dev-vm/bcappvm/codebases/microapps/ng-shipments/src/app';

const init = (dir) => {
  let filesList = [];

  fs.readdir(dir, {
    encoding: 'utf8',
    withFileTypes: true,
  }, (err, files) => {
    if (err) {
      throw err;
    }

    let pending = files.length;

    if (!pending) {
      return filesList;
    }

    files.forEach((file) => {
      const { name } = file;
      const resolvePath = path.resolve(dir, name);

      fs.stat(resolvePath, (err, stat) => {
        if (stat && stat.isDirectory()) {
          init(resolvePath, (err, result) => {
            if (err) {
              throw err;
            }

            filesList = filesList.concat(result);

            if (!--pending) {
              return filesList;
            }
          });
        } else {
          if (name.indexOf('js') !== -1 || name.indexOf('ts') !== -1) {
            fs.readFile(resolvePath, (err, data) => {
              if (err) {
                throw err;
              }

              const arr = [];
              let dataArray = data.toString().split('\n');

              dataArray.forEach((string, index) => {
                if (string.indexOf('gettextCatalog') !== -1) {
                  return;
                }

                let array =  string.match(/['"][^\s,$]([a-zA-Z0-9\s])(?!.*_).*?['"]/g);

                if (array === null) {
                  return;
                }

                array.forEach(elem => {
                  const tmp = elem.match(/['"][^ng,ui]([a-zA-Z0-9\s]).*?['"]/g);

                  if (tmp === null) {
                    return;
                  }

                  tmp.forEach(elem => {
                    const tmp = elem.match(/['"][A-Z]([a-zA-Z0-9\s]).*?['"]/g);

                    if (tmp === null) {
                      return;
                    }

                    arr.push(`${index+1}. ${tmp}`);
                  });
                });
              });

              if (!arr.length) {
                return;
              }

              fs.appendFileSync('report.txt', resolvePath, (err) => {
                if (err) {
                  throw err;
                }
              });

              fs.appendFileSync('report.txt', `\n\t${arr.join(',\n\t')}\n`, (err) => {
                if (err) {
                  throw err;
                }
              });
            });
          }

          if (!--pending) {
            return filesList;
          }
        }
      });
    });
  });
};

fs.readFile('report.txt', (err) => {
  if (err) {
    init(dir);

    return;
  }

  fs.unlink('report.txt', (err) => {
    if (err) {
      throw err;
    }

    console.log('File \'report.txt\' deleted successfully!');

    init(dir);
  });
});
