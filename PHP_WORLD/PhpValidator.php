<?php

/**
 * Class PhpValidator
 */
class PhpValidator
{
    /**
     * @var array
     */
    private $incomingResult;

    public function execute()
    {
        $params = $_GET;
        $result = [];
        if (isset($params['folders'])) {
            $folders = explode(',', $params['folders']);

            try {
                foreach ($folders as $folder) {
                    if(empty($this->incomingResult)){
                        $this->incomingResult = $this->getDirContents($folder);
                    }else{
                        $result = $this->getDirContents($folder);
                        $this->incomingResult = array_merge($this->incomingResult, $result);
                    }
                }
                if (isset($params['mode'])) {
                    $result = $this->getResultStringsCount($result);
                }
            } catch (Throwable $e) {
            } finally {
                echo json_encode([$this->incomingResult]);
            }
        }
    }

    /**
     * @param       $dir
     * @param array $results
     *
     * @return array
     */
    private function getDirContents($dir, &$results = []): array
    {
        $files = [];
        $arrayData = [];

        if (is_dir($dir)) {
            $files = scandir($dir);
        }

        foreach ($files as $key => $value) {
            $path = realpath($dir.DIRECTORY_SEPARATOR.$value);

            if (!is_dir($path) && strpos($path, '.php')) {

                $data = array_filter(
                    array_map(
                        'trim',
                        preg_grep('/^(?=.*([\'"]).+?\1)(?!.*_)(?!^[$].*).*/',
                            file($path)
                        )
                    )
                );
                $data = preg_grep("#'\p{Lu}#u", $data);
                $data = preg_grep("/\b(\w*this->i18n->translate\w*)\b/", $data, PREG_GREP_INVERT);
                $data = preg_grep("/\b(\w*this->i18n->noTranslate\w*)\b/", $data, PREG_GREP_INVERT);
                $data = preg_grep("/\b(\w*case '\w*)\b/", $data, PREG_GREP_INVERT);
                $data = preg_grep("/((['\"]).[a-z]*)([A-Z]*?)([A-Z][a-z]+)/", $data, PREG_GREP_INVERT); // camelCase with '

                foreach ($data as $stringNumber => $stringValue) {
                    $arrayData[] = [$stringNumber, $stringValue];
                }
                if (!empty($data)) {

                    $results[] = [
                        $path,
                        $arrayData,
                    ];
                }
            } else if ($value !== '.' && $value !== '..' && $value !== '.DS_Store') {
                $this->getDirContents($path, $results);
            }
        }

        return $results;
    }

    /**
     * @param array $result
     *
     * @return array
     */
    private function getResultStringsCount(array $result): array
    {
        $wholeStringsInFile = 0;
        $untranslatedStrings = 0;

        foreach ($result as $item) {
            $wholeStringsInFile += count(file($item[0])) + 1;
            $untranslatedStrings += count($item[1]);
        }

        return [
            $wholeStringsInFile,
            $untranslatedStrings,
        ];
    }
}
