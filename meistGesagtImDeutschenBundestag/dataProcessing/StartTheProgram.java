package dataProcessing;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;

/**
 * Contains the main method and starts the program which counts and sorts words in a month.
 * @author Raphael Walger
 *
 */
public class StartTheProgram {

	/**
	 * This method starts the program which counts and sorts words in a month. 
	 * Furthermore it retrieves information from the user and displays text on the terminal.
	 * @param args not used
	 */
	public static void main(String[] args) {
		System.out.println("Mithilfe dieses Programmes kann man die Top n der gesagten (nicht aussortierten)"); 
		System.out.println("Woerterstaemme im deutschen Bundestag pro Monat herausfinden.");
		System.out.println();
		System.out.println("--------Hinweise--------");
		System.out.println("Die Ergebnisse dieses Programmes werden in die Output-Datei geschrieben.");
		System.out.println("Die Output-Datei wird eine CSV-Datei sein.");
		System.out.println("Die Output-Datei wird im Ordner results sein.");
		System.out.println("------------------------");
	    System.out.println("");
	    
	    String inputDateiName = "data/output_raw.csv"; //this file contains the data which will be processed
	    Month[] allMonths = {}; //array which will contain the data from input file
	    try {
	    	allMonths = ProcessData.preProcessDataFromFile(inputDateiName); //preprocesses the data from the file and writes it into a Month array
		} catch (IOException eIO) {
			eIO.printStackTrace();
		}
	    
	    //get number of words in the Word list from a Month 
	    int numberOfWordInLists = allMonths[0].getAlleWoerterVomMonat().size(); //It does not matter from which list the size is taken from, because all lists have the same size.
	    		
	    //get input data from user
	    System.out.print("Wie soll die Output-Datei heissen?: ");
		Scanner in = new Scanner(System.in);
		String outputDateiName = in.nextLine();
	    System.out.println("");
	    System.out.print("Wie viele Wortstaemme pro Monat sollen ausgegeben werden? (Max. "+numberOfWordInLists+"): ");
		int anzahlWoerter = in.nextInt();
	    in.close();
		
	    System.out.println("Eingaben erhalten.");
	    System.out.println("");

	    outputDateiName = "results/" + outputDateiName + ".csv"; //because this file needs to be a CSV file
	    
		try {
			ProcessData.processDataWithInputFromUser(allMonths, outputDateiName, anzahlWoerter); //process Month array with input from user
		} catch (FileNotFoundException eFNF) {
			eFNF.printStackTrace();
		}

	}

}
