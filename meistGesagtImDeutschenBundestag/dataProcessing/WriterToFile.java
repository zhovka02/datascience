/*
MIT License

Copyright (c) 2017 Eugen Paraschiv

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
package dataProcessing;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * This Class writes data into a new file.
 * Methods written by Eugen Paraschiv. 
 * Class created and methods modified by Raphael Walger.
 * @author Eugen Paraschiv, Raphael Walger
 *
 */
public class WriterToFile {

	/**
	 * Converts a given String array into the format csv and returns it as a single String.
	 * @param data String array which needs to get formatted
	 * @return String which is the formatted String array
	 */
	private String convertToCSV(String[] data) {
        return Stream.of(data)
            .map(this::escapeSpecialCharacters)
            .collect(Collectors.joining(","));
    }

	/**
	 * Escapes special characters in the given String.
	 * @param data String, which may contain characters that need to be escaped
	 * @return String where special characters are escaped.
	 */
    private String escapeSpecialCharacters(String data) {
        String escapedData = data.replaceAll("\\R", " ");
        if (data.contains(",") || data.contains("\"") || data.contains("'")) {
            data = data.replace("\"", "\"\"");
            escapedData = "\"" + data + "\"";
        }
        return escapedData;
    }
    
    /**
     * Writes a Month array into a new file with the given name. 
     * @param filename name of the new file
     * @param allMonths Month array which will be written into the new file
     * @throws FileNotFoundException if the given file object does not denote an existing, writable regular file and a new regular file of that name cannot be created, or if some other error occurs while opening or creating the file
     */
    protected static void givenDataArray_whenConvertToCSV_thenOutputCreated(String filename, Month[] allMonths) throws FileNotFoundException {
    	WriterToFile wrToFile = new WriterToFile();
    	
    	System.out.println("Writing...");
		
		List<String[]> dataLines = ProcessData.formatMonthArrayToArrayList(allMonths);
		
		File csvOutputFile = new File(filename);
	    try (PrintWriter pw = new PrintWriter(csvOutputFile)) {
	        dataLines.stream()
	          .map(wrToFile::convertToCSV)
	          .forEach(pw::println);
	    }
	    
	    System.out.println("Finished writing into file: "+ filename);
    }
}
