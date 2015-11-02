package jp.setsulla.bantorra.siron;

import android.util.Log;
import static jp.setsulla.bantorra.siron.SironService.APP_TAG;

/**
 * Created by setsulla on 2015/11/03.
 */
public class LogRunnable implements Runnable {
    Runnable mActionRunnable;
    String mCommand;

    public LogRunnable(Runnable actionRunnable, String command) {
        this.mActionRunnable = actionRunnable;
        this.mCommand = command;
    }

    @Override
    public void run() {
        Log.d(APP_TAG, "Executing command " + mCommand);
        mActionRunnable.run();
        Log.d(APP_TAG, "Done executing command " + mCommand);
    }
}