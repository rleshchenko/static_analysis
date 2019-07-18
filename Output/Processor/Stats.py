class Stats:
    def execute(self, results):
        return [
            'Total parsed strings count:' + str(results.get_total_count()) + '\n',
            'Total translated phrases count:' + str(results.get_translated_count()) + '\n',
            'Total untranslated elements count:' + str(results.get_untranslated_count()) + '\n'
        ]
