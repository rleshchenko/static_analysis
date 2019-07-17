<?php

/**
 * TODO move logic to python
 * Class PhpValidator
 */
class PhpValidator
{

    const STATS_MODE = 'stats';

    public function execute()
    {
        $params = $_GET;
        if (isset($params['folders'])) {
            $folders = explode(',', $params['folders']);

            try {
                if ($params['mode'] != static::STATS_MODE) {
                    $result = $this->getUntranslatedReport($folders);
                } else {
                    $result = $this->prepareStatsReport($folders);
                }
                echo json_encode($result);

            } catch (Throwable $e) {
                echo $e->getMessage();
            }
        }
    }

    private function prepareStatsReport($folders)
    {
        $translatedReport = $this->getTranslatedReport($folders);
        $untranslatedReport = $this->getUntranslatedReport($folders);
        return [
            'total_strings_count'        => $untranslatedReport['stats']['total_strings_count'],
            'untranslated_entries_count' => $untranslatedReport['stats']['entries_count'],
            'translated_entries_count'   => $translatedReport['stats']['entries_count']
        ];

    }

    private function getTranslatedReport($folders)
    {
        $results = [];
        foreach ($folders as $folder) {
            $results = $this->getDirContentsTranslated($folder, $results);
        }
        $stats = $this->getResultStringsCount($results);
        return [
            'stats' => $stats,
            'report' => $results
        ];
    }

    private function getUntranslatedReport(array $folders)
    {
        $results = [];
        foreach ($folders as $folder) {
            $results = $this->getDirContentsUntranslated($folder, $results);
        }
        $stats = $this->getResultStringsCount($results);
        return [
            'stats' => $stats,
            'report' => $results
        ];
    }

    /**
     * @param string $dir
     * @param array  $results
     *
     * @return array
     */
    private function getDirContentsUntranslated(string $dir, &$results = []): array
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
                    $arrayData[] = [
                        'line_number' => $stringNumber,
                        'line_value'  => $stringValue
                    ];
                }
                if (!empty($data)) {
                    $results[] = [
                        'file_path' => $path,
                        'entries' => $arrayData
                    ];
                }

            } else if ($value !== '.' && $value !== '..' && $value !== '.DS_Store') {
                $this->getDirContentsUntranslated($path, $results);
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
    private function getDirContentsTranslated(string $dir, &$results = []): array
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
                    $arrayData[] = [
                        'line_number' => $stringNumber,
                        'line_value' => $stringValue
                    ];
                }
                if (!empty($data)) {
                    $results[] = [
                        'file_path' => $path,
                        'entries' => $arrayData
                    ];
                }
            } else if ($value !== '.' && $value !== '..' && $value !== '.DS_Store') {
                $this->getDirContentsTranslated($path, $results);
            }
        }

        return $results;
    }

    /**
     * @param array $report
     *
     * @return array
     */
    private function getResultStringsCount(array $report): array
    {
        $wholeStringsInFile = 0;
        $entries = 0;

        foreach ($report as $item) {
            $wholeStringsInFile += count(file($item['file_path'])) + 1;
            $entries += count($item['entries']);
        }

        return [
            'total_strings_count' => $wholeStringsInFile,
            'entries_count' => $entries,
        ];
    }
}
