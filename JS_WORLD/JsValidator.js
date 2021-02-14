const fs = require('fs');
const path = require('path');

/**
 * JsValidator class
 */
class JsValidator {
    /**
     * @param {object} options
     */
    constructor(options) {
        this._options = options;
    }

    /**
     * @return {Array} filesArray
     */
    init() {
        const files = this._getFiles(this._options.dir);

        return [this._getResult(files)];
    }

    /**
     * @param {String} dir
     * @return {Array} filesArray
     * @private
     */
    _getFiles(dir) {
        const files = fs.readdirSync(dir, {
            encoding: 'utf8',
        });

        let filesArray = [];

        files.forEach((file) => {
            const resolvePath = path.resolve(dir, file);
            const stat = fs.statSync(resolvePath);

            if (stat && stat.isDirectory()) {
                filesArray = filesArray.concat(this._getFiles(resolvePath));

                return;
            }

            if (this._checkFile(file)) {
                filesArray.push(resolvePath);
            }
        });

        return filesArray;
    }

    /**
     * @param {String} file
     * @return {boolean}
     * @private
     */
    _checkFile(file) {
        const result = this._options.extensions.indexOf(path.extname(file));

        if (file.indexOf('.spec') !== -1) {
            return false;
        }

        return result !== -1;
    }

    /**
     * @param {Array} files
     * @return {Array} result
     * @private
     */
    _getResult(files) {
        let result = [];

        files.forEach((file) => {
            const data = fs.readFileSync(file).toString().split('\n');

            result.push([
                file,
                this._getStrings(data),
            ]);
        });

        result = result.filter((elem) => elem[1].length);

        return result;
    }

    /**
     * @param {Array} data
     * @return {Array} strings
     * @private
     */
    _getStrings(data) {
        const strings = [];

        let matchString = [];

        data.forEach((string, index) => {
            if (string.indexOf('gettextCatalog.getString') !== -1) {
                return;
            }

            this._options.matcher.filter((regex) => {
                matchString = string.match(regex);
            });

            if (matchString === null) {
                return;
            }

            matchString.forEach((string) => {
                strings.push([
                    index,
                    string,
                ]);
            });
        });

        if (!strings.length) {
            return [];
        }

        return strings;
    }
}

module.exports = JsValidator;
