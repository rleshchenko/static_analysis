class ReportFile:

    def execute(self, results):

        for item in results:
        """Renders result in the console"""
        print ('Total strings count: ' + str(results[0]) + ' \n')
        print ('Untranslated strings count: ' + str(results[1]) + ' \n')