package dataProcessing;

/**
 * This class represents a Word.
 * It contains the word and its quantity, so how often it was said.
 * @author Raphael Walger
 *
 */
public class Word implements Comparable<Word>{

	private String wort; //word
	private int anzahl; //Quantity of the word
	
	/**
	 * Creates a word with its quantity.
	 * @param wort the word
	 * @param anzahl quantity of this word, how often it was said
	 */
	public Word(String wort, int anzahl) {
		this.wort=wort;
		this.anzahl=anzahl;
	}
	
	@Override
	/**
	 * This method returns the opposite result of what is specified in the interface Comparable.
	 */
	public int compareTo(Word w) {
		if (this.anzahl > w.anzahl) { //if this word has more quantity than given word w
			return -1;
		} else if (this.anzahl == w.anzahl) { //if both words have the same quantity
		    return 0;
		} else { //if this word has less quantity than given word w
		    return 1;
		}
	}
	
	@Override
	public String toString() {
		return "|"+wort+": "+anzahl+"| ";
	}
	
	/**
	 * Returns the quantity of this word.
	 * @return quantity of this word
	 */
	public int getAnzahl(){
		return this.anzahl;
	}
	
	/**
	 * Returns this word.
	 * @return this word
	 */
	public String getWort() {
		return this.wort;
	}
	
}
