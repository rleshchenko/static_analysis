<?php

// @codingStandardsIgnoreStart
class TranslateNodeClass extends Twig_Node
// @codingStandardsIgnoreEnd
{
    /**
     * Interspire_Template_Node_Translate constructor.
     *
     * @param array  $nodes
     * @param array  $attributes
     * @param int    $lineNumber
     * @param string $tag
     */
    public function __construct(array $nodes, array $attributes, int $lineNumber, string $tag)
    {
        parent::__construct($nodes, $attributes, $lineNumber, $tag);
    }

    /**
     * @param Twig_Compiler $compiler
     *
     * @return void
     */
    public function compile(Twig_Compiler $compiler)
    {
        $messagePlural = null;
        $compiler->addDebugInfo($this);
        $body = $this->getNode('body');
        list($message, $variables) = $this->compileString($body);
        if (null !== $plural = $this->getNode('plural')) {
            list($messagePlural, $variablesPlural) = $this->compileString($this->getNode('plural'));
            $variables = array_merge($variables, $variablesPlural);
        }
        if (null !== $context = $this->getNode('context')) {
            $context = trim($context->getAttribute('data'));
        }
        $function = $this->checkFunction($plural, $context);
        if ($variables) {
            $compiler->write(sprintf('echo strtr( %s(', $function));
        } else {
            $compiler->write(sprintf('echo %s(', $function));
        }
        $this->checkAndRewriteWithContext($compiler, $context);
        $compiler->subcompile($message);
        $this->checkAndRewritePlural($compiler, $plural, $messagePlural);
        if ($variables) {
            $compiler->raw('), [');
            $this->writeReplacedVariables($compiler, $variables);
            $compiler->raw("]");
        }
        $compiler->raw(");\n");
    }

    /**
     * @param Twig_Node $body A Twig_Node instance
     *
     * @return array
     */
    protected function compileString(Twig_Node $body)
    {
        if ($this->checkBodyInstance($body)) {
            return [$body, []];
        }
        $variables = [];
        $message = '';
        if (count($body) > 0) {
            foreach ($body as $node) {
                if (get_class($node) === 'Twig_Node' && $node->getNode(0) instanceof Twig_Node_SetTemp) {
                    $node = $node->getNode(1);
                }
                if ($node instanceof Twig_Node_Print) {
                    $twig_Node = $node->getNode('expr');
                    while ($twig_Node instanceof Twig_Node_Expression_Filter) {
                        $twig_Node = $twig_Node->getNode('node');
                    }
                    $message .= sprintf('%%%s%%', $twig_Node->getAttribute('name'));
                    $variables[] = new Twig_Node_Expression_Name($twig_Node->getAttribute('name'), $twig_Node->getTemplateLine());
                } else {
                    $message .= $node->getAttribute('data');
                }
            }
        } else {
            $message = $body->getAttribute('data');
        }
        return [new Twig_Node([new Twig_Node_Expression_Constant(trim($message), $body->getTemplateLine())]), $variables];
    }

    /**
     * @param Twig_Node $body
     *
     * @return bool
     */
    private function checkBodyInstance(Twig_Node $body): bool
    {
        return $body instanceof Twig_Node_Expression_Name || $body instanceof Twig_Node_Expression_Constant || $body instanceof Twig_Node_Expression_TempName;
    }

    /**
     * @param null|Twig_Node_Text $plural
     * @param null|Twig_Node_Text $context
     *
     * @return string
     */
    private function checkFunction($plural = null, $context = null): string
    {
        if (null !== $context && null !== $plural) {
            $function = 'np__';
        } elseif (null !== $context) {
            $function = 'p__';
        } elseif (null !== $plural) {
            $function = 'n__';
        } else {
            $function = '__';
        }
        return $function;
    }

    /**
     * @param Twig_Compiler $compiler
     * @param null|string   $context
     */
    private function checkAndRewriteWithContext(Twig_Compiler $compiler, $context)
    {
        if (null !== $context) {
            $compiler
                ->string($context)
                ->raw(', ');
        }
    }

    /**
     * @param Twig_Compiler $compiler
     * @param               $plural
     * @param               $messagePlural
     */
    private function checkAndRewritePlural(Twig_Compiler $compiler, $plural, $messagePlural)
    {
        if (null !== $plural) {
            $compiler
                ->raw(', ')
                ->subcompile($messagePlural)
                ->raw(', abs(')
                ->subcompile($this->getNode('count'))
                ->raw(')');
        }
    }

    /**
     * @param Twig_Compiler $compiler
     * @param array         $variables
     *
     * @return void
     */
    private function writeReplacedVariables(Twig_Compiler $compiler, array $variables)
    {
        foreach ($variables as $var) {
            if ('count' === $var->getAttribute('name')) {
                $compiler
                    ->string('%count%')
                    ->raw(' => abs(')
                    ->subcompile($this->getNode('count'))
                    ->raw('), ');
            } else {
                $compiler
                    ->string('%' . $var->getAttribute('name') . '%')
                    ->raw(' => ')
                    ->subcompile($var)
                    ->raw(', ');
            }
        }
    }
}
