<?php

declare(strict_types = 1);

/**
 * Class TwigValidator responsible for filtering twig default and custom nodes
 */
class TwigValidator
{
    /**
     * @var Twig_Loader_Filesystem
     */
    protected $twigFilesystem;

    /**
     * @var Twig_Environment
     */
    protected $twigEnvironment;

    /**
     * @var string
     */
    private const FILTERS_PATH = 'Assets/filters.json';

    /**
     * Array of Twig Nodes.
     *
     * @var array
     */
    private const NODES = [
        Twig_Node_If::class,
        Twig_Node_For::class,
        Twig_Node_Include::class,
        Twig_Node_Macro::class,
        Twig_Node_Print::class,
    ];

    /**
     * @param Twig_Loader_Filesystem $twigFilesystem
     * @param Twig_Environment       $twigEnvironment
     */
    public function __construct(Twig_Loader_Filesystem $twigFilesystem, Twig_Environment $twigEnvironment)
    {
        $this->twigFilesystem = $twigFilesystem;
        $this->twigEnvironment = $twigEnvironment;

        $filters = file_get_contents(self::FILTERS_PATH);
        $filters = json_decode($filters, true);

        foreach ($filters as $filter) {
            $this->twigEnvironment->addFilter(
                new Twig_SimpleFilter($filter, static function($string) {
                    return $string;
                }));
        }
    }

    public function execute(): ?string
    {
        if (!isset($_GET['elements'])) {
            return null;
        }

        $incoming = $_GET['elements'];
        $incoming = json_decode($incoming, true);

        foreach ($incoming as $key => $string) {
            $string = preg_replace("/[\n\r]/", '', $string);
            try {
                $parsedData = $this->twigEnvironment->parse($this->twigEnvironment->tokenize($string));
            } catch (Twig_Error_Syntax $e) {
                $incoming[$key] = $string;
                continue;
            }
            $node = $parsedData->getNode('body')->getNode(0);
            if ($this->checkNodes($node) === true) {
                unset($incoming[$key]);
                continue;
            }
            $incoming[$key] = $string;
        }

        return json_encode($incoming);
    }

    /**
     * @param $incomingNode
     *
     * @return bool
     */
    private function checkNodes($incomingNode): bool
    {
        $incomingNode = get_class($incomingNode);

        return in_array($incomingNode, self::NODES, true);
    }
}
