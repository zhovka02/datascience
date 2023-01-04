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

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * This Class writes data into a new file.
 * Method written by Eugen Paraschiv. 
 * Class created and method modified by Raphael Walger.
 * @author Eugen Paraschiv, Raphael Walger
 *
 */
public class ReaderFromFile {
	
	/**
	 * Reads the content from the file fileName and returns the content in a list of Strings.
	 * @param fileName name of the file which will be read
	 * @return content of file as a list of lists of Strings
	 * @throws IOException if an I/O error occurs
	 */
	protected static List<List<String>> givenCSVFile_whenBufferedReader_thenContentsAsExpected(String fileName) throws IOException {
		//this list contains all lines which are separated into list
		//one line is store in a list, this list has only one entry which is the line
		//all in all: this is a list of lists which contain only one entry each
        List<List<String>> text = new ArrayList<List<String>>();
       
        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) { //try to read content from file
            String line = "";
            while ((line = br.readLine()) != null) { //as long as there is a new line in the file 
                String[] values = line.split(", "); //ad all words, which are separated by a comma, to a String array
                text.add(Arrays.asList(values)); //add the String array into the list
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        return text; //return the list
	}
}
