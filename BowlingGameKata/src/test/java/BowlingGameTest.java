import org.game.BowlingGame;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class BowlingGameTest {

    private BowlingGame game;

    /*
     * Test setup and cases
     */

    @BeforeEach
    public void setUp() {
        game = new BowlingGame();
    }

    @Test
    public void zeroScoreWhenNoPins() {
        rollZeroes(20);
        assertEquals(0, game.score());
    }

    @Test
    public void negativeScoreNotAllowed() {
        assertThrows(IllegalArgumentException.class, () -> {
            game.roll(-1);
        });
    }

    @Test
    public void invalidRollAboveTenNotAllowed() {
        assertThrows(IllegalArgumentException.class, () -> {
            game.roll(11);
        });
    }

    @Test
    public void onePinKnockedDown() {
        game.roll(1);
        rollZeroes(19);
        assertEquals(1, game.score());
    }

    @Test
    public void spareFollowedByThree() {
        game.roll(5);
        game.roll(5);
        game.roll(3);
        rollZeroes(17);
        assertEquals(16, game.score());
    }

    @Test
    public void noSpareButTensInTwoRolls() {
        game.roll(0);
        game.roll(4);
        game.roll(6);
        game.roll(3);
        rollZeroes(16);
        assertEquals(13, game.score());
    }

    @Test
    public void twoSparesInARow() {
        game.roll(7);
        game.roll(3);
        game.roll(4);
        game.roll(6);
        game.roll(5);
        rollZeroes(15);
        assertEquals(34, game.score());
    }

    @Test
    public void firstFrameStrike() {
        game.roll(10);
        game.roll(3);
        game.roll(6);
        rollZeroes(16);
        assertEquals(28, game.score());
    }

    @Test
    public void twoStrikesInARow() {
        game.roll(10);
        game.roll(10);
        game.roll(4);
        game.roll(2);
        rollZeroes(14);
        assertEquals(46, game.score());
    }

    @Test
    public void perfectGame() {
        rollMany(12, 10);
        assertEquals(300, game.score());
    }

    @Test
    public void allSparesWithFivePins() {
        rollMany(21, 5);
        assertEquals(150, game.score());
    }

    @Test
    public void tooManyRollsNotAllowed() {
        rollMany(20, 4);
        assertThrows(IllegalStateException.class, () -> {
            game.roll(4);
        });
    }

    @Test
    public void tenthFrameSpareAllowsExtraRoll() {
        rollMany(18, 4);
        game.roll(5);
        game.roll(5);
        game.roll(7);
        assertEquals(89, game.score());
    }

    @Test
    public void unfinishedGameScore() {
        game.roll(10);
        game.roll(7);
        game.roll(2);
        assertEquals(28, game.score());
    }

    @Test
    public void invalidTenthFrameRollNotAllowed() {
        rollMany(18, 4);
        game.roll(3);
        game.roll(6);
        assertThrows(IllegalStateException.class, () -> {
            game.roll(5);
        });
    }

    /*
     * Private helper methods
     */

    private void rollMany(int n, int pins) {
        for (int i = 0; i < n; i++) {
            game.roll(pins);
        }
    }

    private void rollZeroes(int n) {
        rollMany(n, 0);
    }
}
