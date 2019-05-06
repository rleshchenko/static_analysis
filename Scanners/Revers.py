from Full import Full

class Revers(Full):
    mode = 'revers'

    def print_results(self, results):
        """Renders result in the console"""
        print ('Total strings count: ' + str(results[0]) + ' \n')
        print ('Translated strings count: ' + str(results[1]) + ' \n')

    def write_results(self, results):
        """Renders result to the file"""
        file = open('report.txt', 'w')
        file.write('Total strings count: ' + str(results[0]) + ' \n')

        file.write('Translated strings count: ' + str(results[1]) + ' \n')
        file.close()