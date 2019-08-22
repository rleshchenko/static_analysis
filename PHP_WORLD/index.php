<?php

require_once __DIR__ . '/../vendor/autoload.php';
include 'PhpValidator.php';
include 'TwigParser.php';

$routes = explode('/', $_SERVER['REQUEST_URI']);
$routes = explode('?', $routes[2]);
$controller = $routes[0];

switch ($controller) {
    case 'phpvalidator':
        $validator = new PhpValidator();
        break;
    case 'twigvalidator':
        $validator = new TwigParser(new Twig_Loader_Filesystem(), new Twig_Environment());
        break;
}

return $validator->execute();
