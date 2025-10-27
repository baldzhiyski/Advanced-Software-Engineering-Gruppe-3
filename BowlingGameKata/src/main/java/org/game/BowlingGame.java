package org.game;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents a bowling game.
 * Handles rolls and calculates the total score.
 */
public class BowlingGame {

    private final List<Integer> rolls = new ArrayList<>();
    private final List<Frame> frames = new ArrayList<>();
    private static final int MAX_FRAMES = 10;
    private static final int STRIKE_PINS = 10;

    /**
     * Records a roll in the game.
     *
     * @param pins the number of pins knocked down in the roll
     * @throws IllegalArgumentException if pins is less than 0 or greater than 10
     * @throws IllegalStateException    if no more rolls are allowed in the 10th frame
     */
    public void roll(int pins) {
        if (pins < 0 || pins > STRIKE_PINS) {
            throw new IllegalArgumentException("Pins must be between 0 and 10");
        }
        if (isGameOver()) {
            throw new IllegalStateException("No more rolls allowed in the 10th frame");
        }
        rolls.add(pins);
    }


    /**
     * Calculates the total score of the game by creating frames and applying bonuses.
     *
     * @return the total score
     */
    public int score() {
        createFrames();
        int bonus = calculateBonus();
        return calculateTotalScore(bonus);
    }


    /**
     * Calculates the total score including bonuses.
     *
     * @param bonus the total bonus score from strikes and spares
     * @return the total score
     */
    private int calculateTotalScore(int bonus) {
        int frameScore = frames.stream().mapToInt(Frame::getFrameScore).sum();
        return frameScore + bonus;
    }


    /**
     * Calculates the total bonus score from strikes and spares.
     *
     * @return the total bonus score
     */
    private int calculateBonus() {
        int bonus = 0;
        for (int j = 0; j < frames.size(); j++) {
            Frame currentFrame = frames.get(j);

            if (currentFrame.isSpare()) {
                bonus += calculateSpareBonus(j);
            } else if (currentFrame.isStrike()) {
                bonus += calculateStrikeBonus(j);
                }
        }
        return bonus;
    }


    /**
     * Calculates the bonus for a strike frame.
     *
     * @param frameIndex the index of the strike frame
     * @return the strike bonus score
     */
    private int calculateStrikeBonus(int frameIndex) {
        if (!isNextFrameAvailable(frameIndex)) {
            return 0;
        }

        Frame nextFrame = frames.get(frameIndex + 1);
        int bonus = nextFrame.getFirstRoll();

        if (nextFrame.isStrike() && isFrameAvailable(frameIndex + 2)) {
            bonus += frames.get(frameIndex + 2).getFirstRoll();
        } else {
            bonus += nextFrame.getSecondRoll();
        }

        return bonus;
    }


    /**
     * Calculates the bonus for a spare frame.
     *
     * @param frameIndex the index of the spare frame
     * @return the spare bonus score
     */
    private int calculateSpareBonus(int frameIndex) {
        if (isNextFrameAvailable(frameIndex)) {
            return frames.get(frameIndex + 1).getFirstRoll();
        }
        return 0;
    }


    /**
     * Checks if the next frame is available.
     *
     * @param frameIndex the current frame index
     * @return true if the next frame exists, false otherwise
     */
    private boolean isNextFrameAvailable(int frameIndex) {
        return frameIndex + 1 < frames.size();
    }


    /**
     * Checks if the specified frame is available.
     *
     * @param frameIndex the frame index to check
     * @return true if the frame exists, false otherwise
     */
    private boolean isFrameAvailable(int frameIndex) {
        return frameIndex < frames.size();
    }

    private void createFrames() {
        for (int i = 0; i < rolls.size(); i++) {

            if (isTenthFrame()) {
                createTenthFrame(i);
                break;
            }
            if (isStrikeRoll(i)) { // Strike
                frames.add(new Frame(STRIKE_PINS));
            } else {
                frames.add(new Frame(rolls.get(i), rolls.get(i + 1)));
                i++;
            }

        }
    }

    private boolean isStrikeRoll(int rollIndex) {
        return rolls.get(rollIndex) == STRIKE_PINS;
    }

    private void createTenthFrame(int startIndex) {
        int firstRoll = rolls.get(startIndex);
        int secondRoll = rolls.get(startIndex + 1);
        int thirdRoll = 0;
        if (startIndex + 2 < rolls.size()) {
            thirdRoll = rolls.get(startIndex + 2);
        }
        frames.add(new Frame(firstRoll, secondRoll, thirdRoll));

    }

    private boolean isTenthFrame() {
        return frames.size() == 9;
    }

    private boolean isGameOver() {
        int currentFrame = calculateCurrentFrame();

        if (currentFrame < MAX_FRAMES - 1) {
            return false;
        }

        return isTenthFrameComplete();
    }

    private int calculateCurrentFrame() {
        int frame = 0;
        int rollIndex = 0;

        while (frame < MAX_FRAMES - 1 && rollIndex < rolls.size()) {
            if (isStrikeRoll(rollIndex)) {
                rollIndex++;
            } else {
                rollIndex += 2;
            }
            frame++;
        }

        return frame;
    }

    private boolean isTenthFrameComplete() {
        int tenthFrameStartIndex = findTenthFrameStartIndex();
        int rollsInTenth = rolls.size() - tenthFrameStartIndex;

        if (rollsInTenth < 2) {
            return false;
        }

        int firstRoll = rolls.get(tenthFrameStartIndex);
        int secondRoll = rolls.get(tenthFrameStartIndex + 1);
        boolean deservesThirdRoll = (firstRoll == STRIKE_PINS) || (firstRoll + secondRoll == STRIKE_PINS);

        return deservesThirdRoll ? rollsInTenth >= 3 : true;
    }

    private int findTenthFrameStartIndex() {
        int rollIndex = 0;
        for (int frame = 0; frame < MAX_FRAMES - 1 && rollIndex < rolls.size(); frame++) {
            rollIndex += isStrikeRoll(rollIndex) ? 1 : 2;
        }
        return rollIndex;
    }
}
