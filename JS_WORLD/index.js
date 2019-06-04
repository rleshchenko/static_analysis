const http = require('http');
const url = require('url');
const JsValidator = require('./JsValidator');

http.createServer((request, response) => {
    const folder = url.parse(request.url, true).query.folder;

    const jsValidator = new JsValidator({
        dir: folder,
        extensions: ['.js', '.ts'],
        matcher: [
            /['"][^\s,$]([a-zA-Z0-9\s])(?!.*_).*?['"]/g,
            /['"][^ng,ui]([a-zA-Z0-9\s]).*?['"]/g,
            /['"][A-Z]([a-zA-Z0-9\s]).*?['"]/g,
        ],
    });

    const data = jsValidator.init();

    response.write(JSON.stringify(data));
}).listen(8124, '127.0.0.1');
