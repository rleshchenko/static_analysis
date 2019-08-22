<?php

// @codingStandardsIgnoreStart
class TranslateTokenParserClass extends Twig_TokenParser
// @codingStandardsIgnoreEnd
{
    protected $name;
    protected $nodes;

    /**
     * @param Twig_Token $token
     *
     * @return TranslateNodeClass|Twig_NodeInterface
     * @throws Twig_Error_Syntax
     */
    public function parse(Twig_Token $token)
    {
        $lineNumber = $token->getLine();
        $stream = $this->parser->getStream();
        $data = [
            'count' => null,
            'plural' => null,
            'context' => null,
        ];
        if (!$stream->test(Twig_Token::BLOCK_END_TYPE)) {
            $body = $this->parser->getExpressionParser()->parseExpression();
        } else {
            $stream->expect(Twig_Token::BLOCK_END_TYPE);
            $body = $this->parser->subparse([$this, 'decideForFork']);
            $data = $this->parseDataFromString($stream, $data);
        }
        $stream->expect(Twig_Token::BLOCK_END_TYPE);
        $this->checkTransString($body, $lineNumber);
        $data['body'] = $body;
        return new TranslateNodeClass($data, [], $lineNumber, $this->getTag());
    }

    /**
     * @param Twig_TokenStream $stream
     * @param array            $data
     *
     * @return array
     * @throws Twig_Error_Syntax
     */
    private function parseDataFromString(Twig_TokenStream $stream, array $data): array
    {
        $nextParam = $stream->next()->getValue();
        switch ($nextParam) {
            case 'plural':
                $data = $this->parsePlural($stream, $data);
                break;
            case 'context':
                $data = $this->parseContext($stream, $data);
                break;
        }
        return $data;
    }

    /**
     * @param Twig_TokenStream $stream
     * @param array            $data
     *
     * @return array
     * @throws Twig_Error_Syntax
     */
    private function parsePlural(Twig_TokenStream $stream, array $data): array
    {
        $data['count'] = $this->parser->getExpressionParser()->parseExpression();
        $stream->expect(Twig_Token::BLOCK_END_TYPE);
        $data['plural'] = $this->parser->subparse([$this, 'decideForFork']);
        $next = $stream->next()->getValue();
        if ('context' === $next) {
            $data = $this->parseContext($stream, $data);
        }
        return $data;
    }

    /**
     * @param Twig_TokenStream $stream
     * @param array            $data
     *
     * @return array
     * @throws Twig_Error_Syntax
     */
    private function parseContext(Twig_TokenStream $stream, array $data): array
    {
        $stream->expect(Twig_Token::BLOCK_END_TYPE);
        $data['context'] = $this->parser->subparse([$this, 'decideForEnd'], true);
        return $data;
    }

    /**
     * @param $node
     *
     * @return bool
     */
    private function checkNodeIsCorrectInstance($node): bool
    {
        return $node instanceof Twig_Node_Text || ($node instanceof Twig_Node_Print && $node->getNode('expr') instanceof Twig_Node_Expression_Name);
    }

    /**
     * @param Twig_Node $body
     * @param int       $lineNumber
     *
     * @throws Twig_Error_Syntax
     */
    protected function checkTransString(Twig_Node $body, int $lineNumber)
    {
        foreach ($body as $node) {
            if ($this->checkNodeIsCorrectInstance($node)) {
                continue;
            }
            throw new Twig_Error_Syntax(sprintf('The text to be translated with "translate" can only contain references to simple variables'), $lineNumber);
        }
    }

    /**
     * @return string
     */
    public function getTag(): string
    {
        return 'translate';
    }

    /**
     * @param Twig_Token $token
     *
     * @return bool
     */
    public function decideForFork(Twig_Token $token): bool
    {
        return $token->test(['plural', 'context', 'endtranslate']);
    }

    /**
     * @param Twig_Token $token
     *
     * @return bool
     */
    public function decideForEnd(Twig_Token $token): bool
    {
        return $token->test('endtranslate');
    }
}
