package dataProcessing;

import java.util.ArrayList;

/**
 * This class represents a Month. 
 * It contains its date and a list of Word.
 * @author Raphael Walger
 *
 */
public class Month {
	private String monatDatum; //date of the month
	private ArrayList<Word> alleWoerterVomMonat; //all words from this month
	
	/**
	 * Creates a Month with empty list. Gets String parameter like this: 2015-08
	 * @param monatDatum in the following format: JJJJ-MM
	 */
	public Month(String monatDatum) {
		this.monatDatum=monatDatum;
		this.alleWoerterVomMonat = new ArrayList<>();
	}
	
	/**
	 * Creates a  Month with said words in this Month. 
	 * alleWoerterVomMonat is a list of Word which contains all said words in this month.
	 * @param monatDatum in the following format: JJJJ-MM
	 * @param alleWoerterVomMonat all said words in this month
	 */
	public Month(String monatDatum, ArrayList<Word> alleWoerterVomMonat) {
		this.monatDatum=monatDatum;
		this.alleWoerterVomMonat=alleWoerterVomMonat;
	}
	
	@Override
	public String toString() {
		String string = "<Monat: "+monatDatum+" <> ";
		
		for(Word s : alleWoerterVomMonat) {
			string = string + s.toString();
		}
		
		return string+">";
	}
	
	/**
	 * Returns the date of the month.
	 * @return date of the month
	 */
	public String getMonatDatum() {
		return this.monatDatum;
	}
	
	/**
	 * Returns all said words from this month.
	 * @return all said words from this month
	 */
	public ArrayList<Word> getAlleWoerterVomMonat(){
		return this.alleWoerterVomMonat;
	}
	
	/**
	 * Sets the list of all words from this month to arrListW.
	 * @param arrListW the new list
	 * @throws IllegalArgumentException if arrListW is null
	 */
	public void setAlleWoerterVomMonat(ArrayList<Word> arrListW) throws IllegalArgumentException{
		if(arrListW==null) throw new IllegalArgumentException("error: arrListW is null");
		this.alleWoerterVomMonat = arrListW;
	}
}
