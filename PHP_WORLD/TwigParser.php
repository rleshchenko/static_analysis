<?php
declare(strict_types = 1);

/**
 * Class TwigParser
 */
class TwigParser
{
    /**
     * @var Twig_Loader_Filesystem
     */
    protected $twigFilesystem;

    /**
     * @var Twig_Environment
     */
    protected $twigEnvironment;

    private const NODES = [
        Twig_Node_If::class,
        Twig_Node_For::class,
        Twig_Node_Include::class,
        Twig_Node_Macro::class,
        Twig_Node_Print::class,
    ];

    public function __construct(Twig_Loader_Filesystem $twigFilesystem, Twig_Environment $twigEnvironment)
    {
        $this->twigFilesystem = $twigFilesystem;
        $this->twigEnvironment = $twigEnvironment;

        $filters = json_decode(file_get_contents('Assets/filters.json'), true);

        foreach ($filters as $filter) {
            $this->twigEnvironment->addFilter(new Twig_SimpleFilter($filter, static function($string) {
                return $string;
            }));
        }
    }

    public function execute(): void
    {
        $incoming = $_GET['elements'];
        $incoming = json_decode($incoming, true);

        if (isset($incoming)) {
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
                } else {
                    $incoming[$key] = $string;
                }
            }
        }

        echo json_encode($incoming);
    }

    /**
     * @param $incomingNode
     *
     * @return bool
     */
    private function checkNodes($incomingNode): bool
    {
        foreach (self::NODES as $twigNode) {
            if ($incomingNode instanceof $twigNode) {
                return true;
            }
        }

        return false;
    }
}
