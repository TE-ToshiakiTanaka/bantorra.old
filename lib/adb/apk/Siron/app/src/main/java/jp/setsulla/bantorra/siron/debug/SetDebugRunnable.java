package jp.setsulla.bantorra.siron.debug;

import jp.setsulla.bantorra.siron.MessageManager;

import android.content.Intent;
/**
 * Created by setsulla on 2015/11/03.
 */
public class SetDebugRunnable implements Runnable {

    public static final String DEBUG_ON = "jp.setsulla.bantorra.siron.DEBUG_ON";
    private final Intent mOrigIntent;
    private final int mActionId;

    public SetDebugRunnable(Intent intent, int id) {
        mOrigIntent = intent;
        mActionId = id;
    }

    @Override
    public void run() {
        Debug.setUserDebug(true);
        MessageManager.getInstance().sendMessage(mActionId, true, mOrigIntent);
    }
}