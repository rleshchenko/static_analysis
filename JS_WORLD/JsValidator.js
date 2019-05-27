const fs = require('fs');
const path = require('path');
const esprima = require('esprima');

const dir = '/Users/roman.krasinskyi/Work/cloud-dev-vm/bcappvm/codebases/microapps/ng-shipments/src/app/create/create-details';

// function walkJs(node, fn) {
//   fn(node);
//
//   for (var key in node) {
//     var obj = node[key];
//
//     if (typeof obj === 'object') {
//       walkJs(obj, fn);
//     }
//   }
// }
//
// var binaryExpressionWalkJs = function (node) {
//   var res = '';
//
//   if (node.type === "Literal") {
//     res = node.value;
//   }
//
//   if (node.type === 'BinaryExpression' && node.operator === '+') {
//     res += binaryExpressionWalkJs(node.left);
//     res += binaryExpressionWalkJs(node.right);
//   }
//   return res;
// };

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

              let results = data.toString().match(new RegExp(/^(?=.*(['"]).+?\1)(?!.*_)(?!.*[$].*).*/gm));
              // results = data.toString().match(new RegExp(''));

              console.log(resolvePath);
              console.log(results);
              console.log();

              // const syntax = esprima.parse(data.toString(), {
              //   tolerant: true
              // });

              // walkJs(syntax, function (node) {
              //   if (node === null
              //       || node.callee === undefined
              //       || node.callee.object === undefined
              //       || node.arguments === null
              //       || !node.arguments.length) {
              //     return;
              //   }
              //
              //   if (node.callee.object.name !== undefined) {
              //     console.log(node.arguments);
              //     return;
              //   }
              //
              //   // if (node !== null &&
              //   //     node.type === 'CallExpression' &&
              //   //     node.callee.object.name !== 'gettextCatalog' &&
              //   //     node["arguments"] !== null &&
              //   //     node["arguments"].length) {
              //
              //     const arg = node["arguments"][0];
              //     let str;
              //
              //     switch (arg.type) {
              //       case 'Literal':
              //         str = arg.value;
              //         break;
              //       case 'BinaryExpression':
              //         str = binaryExpressionWalkJs(arg);
              //     }
              //
              //     if (str) {
              //       // console.log(node);
              //       // console.log(node.callee.object.name);
              //       // console.log();
              //       // console.log(str === 'USPS Other' ? node : '');
              //       // console.log();
              //     }
              //   // }
              // });
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

init(dir);
