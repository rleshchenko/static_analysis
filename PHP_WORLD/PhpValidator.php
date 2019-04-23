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
                    $result = $this->getDirContents($folder);
                }
            } catch (Throwable $e) {
            } finally {
                echo json_encode([$result]);
            }
        }
    }

    /**
     * @param $dir
     * @param array $results
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

                foreach ($data as $stringNumber => $stringValue) {
                    $arrayData[] = [$stringNumber, $stringValue];
                }
                if (!empty($data)) {

                    $results[] = [
                        $path,
                        $arrayData
                    ];
                }
            } else if ($value !== '.' && $value !== '..') {
                $this->getDirContents($path, $results);
            }
        }

        return $results;
    }
}