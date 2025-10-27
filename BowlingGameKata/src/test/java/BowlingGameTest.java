import org.game.BowlingGame;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class BowlingGameTest {

    @Test
    public void zeroScoreWhenNoPins() {
        BowlingGame game = new BowlingGame();
        for (int i = 0; i < 20; i++) {
            game.roll(0);
        }
        assertEquals(0, game.score());
    }

    @Test
    public void negativeScoreNotAllowed() {
        BowlingGame game = new BowlingGame();
            assertThrows(IllegalArgumentException.class, () -> {
            game.roll(-1);
        });
    }

    @Test
    public void invalidRollAboveTenNotAllowed() {
        BowlingGame game = new BowlingGame();
        assertThrows(IllegalArgumentException.class, () -> {
            game.roll(11);
        });
    }

    @Test
    public void onePinKnockedDown() {
        BowlingGame game = new BowlingGame();
        game.roll(1);
        for (int i = 0; i < 19; i++) {
            game.roll(0);
        }
        assertEquals(1, game.score());
    }

    @Test
    public void spareFollowedByThree() {
        BowlingGame game = new BowlingGame();
        game.roll(5);
        game.roll(5); // Spare
        game.roll(3);
        for (int i = 0; i < 17; i++) {
            game.roll(0);
        }
        assertEquals(16, game.score());
    }

    @Test
    public void noSpareButTensInTwoRolls() {
        BowlingGame game = new BowlingGame();
        game.roll(0);
        game.roll(4);
        game.roll(6);
        game.roll(3);
        for (int i = 0; i < 16; i++) {
            game.roll(0);
        }
        assertEquals(13, game.score());
    }

    @Test
    public void twoSparesInARow() {
        BowlingGame game = new BowlingGame();
        game.roll(7);
        game.roll(3); // Spare
        game.roll(4);
        game.roll(6); // Spare
        game.roll(5);
        for (int i = 0; i < 15; i++) {
            game.roll(0);
        }
        assertEquals(34, game.score());
    }

    @Test
    public void firstFrameStrike() {
        BowlingGame game = new BowlingGame();
        game.roll(10); // Strike
        game.roll(3);
        game.roll(6);
        for (int i = 0; i < 16; i++) {
            game.roll(0);
        }
        assertEquals(28, game.score());
    }

    @Test
    public void twoStrikesInARow() {
        BowlingGame game = new BowlingGame();
        game.roll(10); // Strike
        game.roll(10); // Strike
        game.roll(4);
        game.roll(2);
        for (int i = 0; i < 14; i++) {
            game.roll(0);
        }
        assertEquals(46, game.score());
    }

    @Test
    public void perfectGame() {
        BowlingGame game = new BowlingGame();
        for (int i = 0; i < 12; i++) {
            game.roll(10); // 12 strikes
        }
        assertEquals(300, game.score());
    }

    @Test
    public void allSparesWithFivePins() {
        BowlingGame game = new BowlingGame();
        for (int i = 0; i < 21; i++) {
            game.roll(5); // 21 rolls of 5 pins
        }
        assertEquals(150, game.score());
    }

    @Test
    public void tooManyRollsNotAllowed() {
        BowlingGame game = new BowlingGame();
        for (int i = 0; i < 20; i++) {
            game.roll(4);
        }
        assertThrows(IllegalStateException.class, () -> {
            game.roll(4);
        });
    }

    @Test
    public void tenthFrameSpareAllowsExtraRoll() {
        BowlingGame game = new BowlingGame();
        for (int i = 0; i < 18; i++) {
            game.roll(4);
        }
        game.roll(5);
        game.roll(5); // Spare in the 10th frame
        game.roll(7); // Extra roll
        assertEquals(89, game.score());
    }

    @Test
    public void unfinishedGameScore() {
        BowlingGame game = new BowlingGame();
        game.roll(10); // Strike
        game.roll(7);
        game.roll(2);
        assertEquals(28, game.score());
    }

    @Test
    public void invalidTenthFrameRollNotAllowed() {
        BowlingGame game = new BowlingGame();
        for (int i = 0; i < 18; i++) {
            game.roll(4);
        }
        game.roll(3);
        game.roll(6); // No spare or strike in the 10th frame
        assertThrows(IllegalStateException.class, () -> {
            game.roll(5); // Extra roll not allowed
        });
    }

}
