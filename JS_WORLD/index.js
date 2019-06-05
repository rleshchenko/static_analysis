const http = require('http');
const url = require('url');
const JsValidator = require('./JsValidator');

http.createServer((request, response) => {
    const folders = url.parse(request.url, true).query.folders;

    const jsValidator = new JsValidator({
        dir: folders,
        extensions: ['.js', '.ts'],
        matcher: [
            /['"][^\s,$]([a-zA-Z0-9\s])(?!.*_).*?['"]/g,
            /['"][^ng,ui]([a-zA-Z0-9\s]).*?['"]/g,
            /['"][A-Z]([a-zA-Z0-9\s]).*?['"]/g,
        ],
    });

    const data = jsValidator.init();
    response.writeHead(200, {'Content-Type': 'application/json; charset=utf-8'});
    response.end(JSON.stringify(data));
}).listen(8124, '127.0.0.1');
