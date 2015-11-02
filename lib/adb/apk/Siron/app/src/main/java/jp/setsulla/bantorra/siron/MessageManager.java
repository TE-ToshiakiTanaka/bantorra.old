package jp.setsulla.bantorra.siron;

import android.os.Handler;
import android.content.Intent;
import android.os.Message;
import android.util.Log;

import jp.setsulla.bantorra.siron.debug.Debug;
import static jp.setsulla.bantorra.siron.SironService.APP_TAG;


/**
 * Created by setsulla on 2015/11/03.
 */
public class MessageManager {
    private static final String TAG = MessageManager.class.getSimpleName();
    private final Handler mTargetHandler;
    private static MessageManager sInstance;
    private static final int NOT_USED = -1;
    private static final int SUCCESS = 1;
    private static final int FAILURE = 0;

    private MessageManager(Handler targetHandler) {
        mTargetHandler = targetHandler;
    }

    public synchronized static MessageManager createNewMessageManager(Handler targetHandler) {
        if (targetHandler == null) {
            throw new IllegalArgumentException("Handler can not be null");
        }
        sInstance = new MessageManager(targetHandler);
        return sInstance;
    }

    public static MessageManager getInstance() {
        return sInstance;
    }

    public boolean getResultFromMessage(Message msg) {
        switch (msg.arg1) {
            case SUCCESS:
                return true;
            case FAILURE:
                return false;
        }
        throw new IndexOutOfBoundsException(
                "Message does not have correct possible values, either 1 or 0. Use message manager to create messages");
    }

    public Intent getIntentFromMessage(Message msg) {
        return ((Intent)msg.obj);
    }

    public synchronized boolean sendMessage(int id, boolean isSuccess, Intent intent) {
        if (id < 0 || !mTargetHandler.getLooper().getThread().isAlive()) {
            if (Debug.isUserEnabled()) {
                Log.d(APP_TAG, TAG + " Not sending message because id [" + id
                        + "] is less than zero or underlaying message queue has died ["
                        + !mTargetHandler.getLooper().getThread().isAlive() + "]");
            }
            return false;
        }
        int isSuccessInt = isSuccess ? SUCCESS : FAILURE;
        Message msg = mTargetHandler.obtainMessage(id, isSuccessInt, NOT_USED, intent);
        msg.sendToTarget();
        return true;
    }

    public synchronized boolean sendMessage(int message) {
        if (!mTargetHandler.getLooper().getThread().isAlive()) {
            if (Debug.isUserEnabled()) {
                Log.d(APP_TAG, TAG + " Not sending message because underlaying message queue has died ["
                        + !mTargetHandler.getLooper().getThread().isAlive() + "]");
            }
            return false;
        }
        mTargetHandler.obtainMessage(message).sendToTarget();
        return true;
    }

    public synchronized boolean sendMessage(int message, int arg){
        if (!mTargetHandler.getLooper().getThread().isAlive()) {
            if (Debug.isUserEnabled()) {
                Log.d(APP_TAG, TAG + " Not sending message because underlaying message queue has died ["
                        + !mTargetHandler.getLooper().getThread().isAlive() + "]");
            }
            return false;
        }

        Message msg = mTargetHandler.obtainMessage(message,SUCCESS, arg);
        msg.sendToTarget();

        return true;
    }

    public int getIdFromMessage(Message msg) {
        return msg.what;
    }
}