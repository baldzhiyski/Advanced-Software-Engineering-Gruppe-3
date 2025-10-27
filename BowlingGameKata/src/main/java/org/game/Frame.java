package org.game;

/**
 * Represents a single frame in a bowling game.
 * Handles strikes, spares and open frames.
 * Calculates the score for the frame.
 */

public class Frame {

    private final int firstRoll;
    private int secondRoll;
    private int thirdRoll;
    private final int MAX_PINS = 10;


    /**
     * Creates a Frame with the first roll score, used for strikes.
     *
     * @param firstRoll the score of the first roll
     */

    public Frame(int firstRoll) {
        this.firstRoll = firstRoll;
    }


    /**
     * Creates a Frame with the first and second roll scores, used for spares and open frames.
     *
     * @param firstRoll  the score of the first roll
     * @param secondRoll the score of the second roll
     */

    public Frame(int firstRoll, int secondRoll) {
        this.firstRoll = firstRoll;
        this.secondRoll = secondRoll;
    }


    /**
     * Creates a Frame with the first, second and third roll scores, used for the tenth frame.
     *
     * @param firstRoll  the score of the first roll
     * @param secondRoll the score of the second roll
     * @param thirdRoll  the score of the third roll
     */

    public Frame(int firstRoll, int secondRoll, int thirdRoll) {
        this.firstRoll = firstRoll;
        this.secondRoll = secondRoll;
        this.thirdRoll = thirdRoll;
    }


    /**
     * Determines if the frame is a spare.
     *
     * @return true if the frame is a spare, false otherwise
     */
    public boolean isSpare() {
        return firstRoll + secondRoll == MAX_PINS && secondRoll != 0;
    }


    /**
     * Determines if the frame is a strike.
     *
     * @return true if the frame is a strike, false otherwise
     */
    public boolean isStrike() {
        return firstRoll == MAX_PINS;
    }


    /**
     * Calculates the total score for the frame.
     *
     * @return the total score of the frame
     */
    public int getFrameScore() {
        return firstRoll + secondRoll + thirdRoll;
    }


    /**
     * Gets the score of the first roll.
     *
     * @return the score of the first roll
     */
    public int getFirstRoll() {
        return firstRoll;
    }


    /**
     * Gets the score of the second roll.
     *
     * @return the score of the second roll
     */
    public int getSecondRoll() {
        return secondRoll;
    }


    /**
     * Gets the score of the third roll.
     *
     * @return the score of the third roll
     */
    public int getThirdRoll() {
        return thirdRoll;
    }
}
