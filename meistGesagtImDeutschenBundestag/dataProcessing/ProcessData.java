package dataProcessing;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * This class offers methods to process data.
 * @author Raphael Walger
 *
 */
public class ProcessData {
	private static final String[] UNWANTED_WORDS = {"TOTAL"};

	/**
	 * Reads data from the file inputName in, converts the read data into an Month array, sorts the Word lists from 
	 * all months in the Month array and deletes unwanted words out of the Word lists of the months in the Month array.
	 * In short, this method calls other methods to process the data from the file where no user inputs are needed.
	 * @param inputName name of the input file
	 * @return preprocessed Month array 
	 * @throws IOException if an I/O error occurs
	 */
	protected static Month[] preProcessDataFromFile(String inputName) throws IOException {
		//get the content from the file as a list of lists of Strings
		List<List<String>> outputList = ReaderFromFile.givenCSVFile_whenBufferedReader_thenContentsAsExpected(inputName); 
				
		Month[] monthArray = convertListIntoArray(outputList); //convert outputList into a Month array
				
		monthArray = sortAllMonths(monthArray); //sort all the words from Month array per month in descending order
				
		monthArray = deleteAllUnwantedWordsFromLists(monthArray, UNWANTED_WORDS); //removes all unwanted words out of the lists
		
		return monthArray; 
	}

	/**
	 * Cuts the length of the Word lists from all months from the given Month array and writes the end result into a file.
	 * The end result is a formatted human-readable file with content sorted by month and word count in descending order. 
	 * The number of words per month, which will be shown in the file, can be set with the parameter numberOfWords.
	 * The name of the formatted human-readable file can be set with the parameter outputName.
	 * @param monthArray Month array which needs more processing
	 * @param outputName name of the file which is the end result
	 * @param numberOfWords number of words per month
	 * @throws FileNotFoundException if the given file object does not denote an existing, writable regular file and a new regular file of that name cannot be created, or if some other error occurs while opening or creating the file
	 * @throws IllegalArgumentException if outputName is empty 
	 */
	protected static void processDataWithInputFromUser(Month[] monthArray, String outputName, int numberOfWords) throws FileNotFoundException, IllegalArgumentException {
		if(outputName.isEmpty()) throw new IllegalArgumentException("error: outputName is empty");
		
		monthArray = cutLengthOfSortedListsOfWords(monthArray, numberOfWords); //short the lists of words per month
		
		monthArray = changeEmptyMonths(monthArray); //changes all words with a quantity of 0 from all Months into a message
		
		//write result into new file
		WriterToFile.givenDataArray_whenConvertToCSV_thenOutputCreated(outputName, monthArray); 
	}
	
	/**
	 * Converts a given list into an Month array.
	 * All words and their quantity per month will be stored in the returned Month array.
	 * @param outputList list with content from a file
	 * @return Month array with words and their quantity per month, the words in the months are unsorted
	 */
	private static Month[] convertListIntoArray(List<List<String>> outputList) {
		
		//the first list in the big list contains the first line, which are the months
		List<String> list = outputList.get(0); //get list of all months (this list has all months as one String)
		int lengthOfList = outputList.get(0).size(); //here it is ==1
		
		//convert the list into an array and split the first and the only entry in this small list into 
		//the months (months are separated in the String by the character ,)
		String[] monthArray = list.toArray(new String[lengthOfList])[0].split(",");
		
		int numberOfMonths = monthArray.length; //get the number of months
		
		Month[] formatedOutput = new Month[numberOfMonths]; //this Month array will contain the result
		
		for(int currentMonth=0; currentMonth < formatedOutput.length; currentMonth++) { //do the following for all months
			formatedOutput[currentMonth] = new Month(monthArray[currentMonth]); //add the month with its date into the Month array
		}
		
		//do the following for almost each word (=line from file)
		for(int lineCounter=1; lineCounter < outputList.size(); lineCounter++) { //lineCounter starts at 1 because the first line (0) contains the date from months
			List<String> currentLine = outputList.get(lineCounter); //get current line
			int lengthOfCurrentLine = outputList.get(lineCounter).size(); //here it is always ==1
			
			String[] wordAndItsQuantities = currentLine.toArray(new String[lengthOfCurrentLine]); //convert list into array
			//split the first and the only entry in this small list into the word and its quantities (quantities are separated in the String by the character ,)
			wordAndItsQuantities = wordAndItsQuantities[0].split(","); 
				
			String currentWord = wordAndItsQuantities[0]; //the first entry of the array is the word, all other entries are its quantities per month
				
			//do the following for each month (=column)
			for(int column = 1; column < wordAndItsQuantities.length; column++) { //start by 1 because wordAndItsQuantities[0] is the word itself
				int quantityOfTheWord = Integer.parseInt(wordAndItsQuantities[column]); //get the quantity of current word/line in this month
				Word wordWithQuantity = new Word(currentWord, quantityOfTheWord); //initialize Word with the word and its quantity
				
				formatedOutput[column].getAlleWoerterVomMonat().add(wordWithQuantity); //add this Word to the list of Word from the current Month(=column)
			}
		}
		
		//delete first line because it does not have any usable information (it contains an empty Month)
		formatedOutput = Arrays.copyOfRange(formatedOutput, 1, formatedOutput.length); 
		
		return formatedOutput;
	}
	
	/**
	 * Sorts the words from a given Month array per month in descending order (from highest to lowest quantity).
	 * @param notSortedMonths Month array, which months need to be sorted
	 * @return Month array with sorted months
	 */
	private static Month[] sortAllMonths(Month[] notSortedMonths) {

		for(Month m : notSortedMonths) { //does the following for each Month in the Month array
			m.getAlleWoerterVomMonat().sort(null); //Sorts the lists of words. It uses the compareTo method in the class Word.
		}
		
		return notSortedMonths;
	}
	
	/**
	 * Removes the unwanted word in the lists of the months of the Month array.
	 * @param monthArr Month array which months may contain the unwanted word in their lists
	 * @param unwantedWord String which is unwanted
	 * @return Month array with months which contain only wanted words in their lists
	 */
	private static Month[] deleteTheUnwantedWordFromLists(Month[] monthArr, String unwantedWord){
		
		for(Month currentMonth : monthArr) { //does the following for each Month from the given Month array
			ArrayList<Word> newWordListForCurrentMonth = new ArrayList<Word>(); //this list will contain all words without the unwanted word
			for(Word currentWord : currentMonth.getAlleWoerterVomMonat()) { //does the following for each Word in the Word list of the current Month
				
				if(!currentWord.getWort().equals(unwantedWord)) { //if currentWord is not the same as wordWhichNeedsToBeRemoved
					newWordListForCurrentMonth.add(currentWord); //add currentWord to the new list
				}
			}
			
			currentMonth.setAlleWoerterVomMonat(newWordListForCurrentMonth); //replace old Word list with unwanted word with new Word list
		}
		
		return monthArr;
	}
	
	/**
	 * Removes all unwanted words in the lists of the months of the Month array.
	 * @param monthArr Month array which months may contain the unwanted words in their lists
	 * @param unwantedWords String array which contains the unwanted words
	 * @return Month array with months which contain only wanted words in their lists
	 */
	private static Month[] deleteAllUnwantedWordsFromLists(Month[] monthArr, String[] unwantedWords) {
		
		for(String word : unwantedWords) { //do the following for each String from the given String array 
			monthArr = deleteTheUnwantedWordFromLists(monthArr, word); //delete the current word from all Word lists
		}
		
		return monthArr;
	}

	/**
	 * Cuts the list of words in a month from given Month array.
	 * @param m Month array
	 * @param numberOfWordsWhichWillBeLeftInLists number of words which will be left in lists of words in a month
	 * @return Month array with smaller lists of words per month
	 * @throws IllegalArgumentException if numberOfWordsWhichWillBeLeftInLists is 0, negative or is bigger than the quantity of words in a month
	 */
	private static Month[] cutLengthOfSortedListsOfWords(Month[] m, int numberOfWordsWhichWillBeLeftInLists) throws IllegalArgumentException{
		//if numberOfWordsWhichWillBeLeftInLists is bigger than the quantity of words in a month
		if(m[0].getAlleWoerterVomMonat().size() < numberOfWordsWhichWillBeLeftInLists) { 
			throw new IllegalArgumentException("error: numberOfWordsWhichWillBeLeftInLists is too big");
		}

		if(numberOfWordsWhichWillBeLeftInLists==0) { 
			throw new IllegalArgumentException("error: numberOfWordsWhichWillBeLeftInLists is 0");
		}
		if(numberOfWordsWhichWillBeLeftInLists < 0) { 
			throw new IllegalArgumentException("error: numberOfWordsWhichWillBeLeftInLists is negative");
		}
		
		Month[] monthsWithCuttedWordLists = new Month[m.length]; //create array which will hold the result
		
		for(int i=0; i < m.length; i++) { //do the following for all months in Month array
			//initialize the list of words and cut its length
			List<Word> subListOfWordsOfCurrentMonth = m[i].getAlleWoerterVomMonat().subList(0, numberOfWordsWhichWillBeLeftInLists);
			
			//initialize the new months with now shorter list of words
			Month monthWithShorterWordLists = new Month(m[i].getMonatDatum(), new ArrayList<Word>(subListOfWordsOfCurrentMonth));
			
			//add the new month into the Month array
			monthsWithCuttedWordLists[i] = monthWithShorterWordLists;
		}
		
		return monthsWithCuttedWordLists; 
	}
	
	/**
	 * Changes the Word list from a month if the first word from the Word list has a quantity of 0, because this means that 
	 * all other words in the Word list have a quantity of 0 too. 
	 * This is only true if the Month array monthArr was previously sorted in a descending order. 
	 * @param monthArr Month array which may contain months with a Word list full of words with have the quantity of 0
	 * @return Month array which has all Word lists, were all words had a quantity of 0, replaced by a message
	 */
	private static Month[] changeEmptyMonths(Month[] monthArr) {
		
		//if there were no words said in this month this Word will be displayed in the result file
		Word noInformationMessage = new Word("kein Wort wurde mehr als 0 mal gesagt", 0); 
		
		for(Month currentMonth : monthArr) { //does the following for each Month in the Month array
			if(currentMonth.getAlleWoerterVomMonat().get(0).getAnzahl() == 0) { //if the quantity of the first word in the Word list from this Month equals 0
				currentMonth.getAlleWoerterVomMonat().clear();  //delete all words from the Word list of the current Month
				currentMonth.getAlleWoerterVomMonat().add(noInformationMessage); //add Word with message into the Word list of the current Month
			}
		}
		
		return monthArr;
	}

	/**
	 * Formats the given Month array back into an list so that the result is readable by a human.
	 * @param mArr Month array which needs to be correctly formated
	 * @return list of Strings which has the content of mArr
	 */
	protected static List<String[]> formatMonthArrayToArrayList(Month[] mArr) {
		List<String[]> list = new ArrayList<>(); //list which will contain the result
		
		String[] emptyLine = {}; //used for formatting
		
		for(int currentMonth=0; currentMonth < mArr.length; currentMonth++) { //do the following for all months in Month array
			String[] monatDatum = {mArr[currentMonth].getMonatDatum()}; //get current date of the month
			
			//create new String array which will contain all words from current month
			int sizeOfWordList = mArr[currentMonth].getAlleWoerterVomMonat().size();
			String[] alleWoerterDiesesMonats = new String[sizeOfWordList]; 
			
			//create new String array which will contain all quantities from the words from current month
			String[] alleAnzahlenDiesesMonats = new String[sizeOfWordList];
			
			for(int currentWord=0; currentWord < mArr[currentMonth].getAlleWoerterVomMonat().size(); currentWord++) { //do the following for each word from current month
				
				String oneWordFromList = mArr[currentMonth].getAlleWoerterVomMonat().get(currentWord).getWort(); //get one word from list 
				alleWoerterDiesesMonats[currentWord] = oneWordFromList; 										 //and add it to the String array
				
				String quantityOfOneWordFromList = Integer.toString(mArr[currentMonth].getAlleWoerterVomMonat().get(currentWord).getAnzahl()); //get the quantity of current Word
				alleAnzahlenDiesesMonats[currentWord] = quantityOfOneWordFromList; 															   //and add it to another String array 
			}

			//add final formatted month into the list, one entry in the list equals one line in the file
			list.add(monatDatum);
			list.add(alleWoerterDiesesMonats);
			list.add(alleAnzahlenDiesesMonats);
			list.add(emptyLine);
			list.add(emptyLine);
		}
		
		return list;
	}
}
