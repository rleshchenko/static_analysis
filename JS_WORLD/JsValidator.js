const fs = require('fs');
const path = require('path');

class JsValidator {
    constructor(options) {
        this._options = options;
    }

    init() {
        const files = this._getFiles(this._options.dir);

        return this._getResult(files);
    }

    _getFiles(dir) {
        const files = fs.readdirSync(dir, {
            encoding: 'utf8',
            withFileTypes: true,
        });

        let filesArray = [];

        files.forEach((file) => {
            const { name } = file;
            const resolvePath = path.resolve(dir, name);
            const stat = fs.statSync(resolvePath);

            if (stat && stat.isDirectory()) {
                filesArray = [ ...filesArray, ...this._getFiles(resolvePath) ];
            } else {
                if (this._checkFile(name)) {
                    filesArray.push(resolvePath);
                }
            }
        });

        return filesArray;
    }

    _checkFile(file) {
        return !!this._options.extensions.filter(extension => file.indexOf(extension) !== -1).length;
    }

    _getResult(files) {
        let result = [];

        files.forEach((file) => {
            const data = fs.readFileSync(file).toString().split('\n');

            result = [ ...result, [ file, this._getStrings(data) ] ];
        });

        result = result.filter(elem => elem[1] !== undefined);

        return result;
    }

    _getStrings(data) {
        let strings = [];

        data.forEach((string, index) => {
            if (string.indexOf('gettextCatalog.getString') !== -1) {
                return;
            }

            let matchString = [];

            this._options.matcher.filter(regex => {
                matchString = string.match(regex);
            });

            if (matchString == null) {
                return;
            }

            matchString.forEach(string => {
                strings = [ ...strings, [ index, string ] ];
            });
        });

        if (!strings.length) {
            return;
        }

        return strings;
    }
}

module.exports = JsValidator;
