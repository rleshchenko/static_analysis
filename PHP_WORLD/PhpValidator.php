<?php

/**
 * Class PhpValidator
 */
class PhpValidator
{
    public function execute()
    {
        $params = $_GET;
        $result = [];
        if (isset($params['folders'])) {
            $folders = explode(',', $params['folders']);

            try {
                foreach ($folders as $folder) {
                    $result = $this->aggregateResult($result, $folder, $params['mode']);
                }
                if ($params['mode'] === 'reverse' || $params['mode'] === 'count') {
                    $result = $this->getResultStringsCount($result);
                }
            } catch (Throwable $e) {
            } finally {
                echo json_encode([$result]);
            }
        }
    }

    /**
     * @param string $dir
     * @param array  $results
     *
     * @return array
     */
    private function getDirContents(string $dir, &$results = []): array
    {
        $files = [];
        $arrayData = [];

        if (is_dir($dir)) {
            $files = scandir($dir);
        }

        foreach ($files as $key => $value) {
            $path = realpath($dir . DIRECTORY_SEPARATOR . $value);

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

                $results[] = [
                    $path,
                    !empty($data) ? $arrayData : [],
                ];
            } else if ($value !== '.' && $value !== '..' && $value !== '.DS_Store') {
                $this->getDirContents($path, $results);
            }
        }

        return $results;
    }

    /**
     * @param string $dir
     * @param array  $results
     *
     * @return array
     */
    private function getDirContentsReverse(string $dir, &$results = []): array
    {
        $files = [];
        $arrayData = [];

        if (is_dir($dir)) {
            $files = scandir($dir);
        }

        foreach ($files as $key => $value) {
            $path = realpath($dir . DIRECTORY_SEPARATOR . $value);

            if (!is_dir($path) && strpos($path, '.php')) {

                $data = array_filter(
                    array_map(
                        'trim',
                        preg_grep("/\b(\w*this->i18n->\w*)\b/",
                            file($path)
                        )
                    )
                );

                foreach ($data as $stringNumber => $stringValue) {
                    $arrayData[] = [$stringNumber, $stringValue];
                }
                $results[] = [
                    $path,
                    !empty($data) ? $arrayData : [],
                ];
            } else if ($value !== '.' && $value !== '..' && $value !== '.DS_Store') {
                $this->getDirContentsReverse($path, $results);
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

    /**
     * @param array  $result
     * @param string $folder
     * @param string $mode
     *
     * @return array
     */
    private function aggregateResult(array $result, string $folder, string $mode): array
    {
        if ($mode === 'reverse') {
            if (empty($result)) {
                return $this->getDirContentsReverse($folder);
            }
            $data = $this->getDirContentsReverse($folder);
        } else {
            if (empty($result)) {
                return $this->getDirContents($folder);
            }
            $data = $this->getDirContents($folder);
        }

        return array_merge($result, $data);
    }
}
