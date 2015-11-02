package jp.setsulla.bantorra.siron;

import android.content.Context;
import android.content.Intent;
import android.os.Handler;
import android.os.Message;

import jp.setsulla.bantorra.siron.debug.SetDebugRunnable;

import java.util.regex.Matcher;
import java.util.regex.Pattern;
/**
 * Created by setsulla on 2015/11/03.
 */
public class RunnableFactory implements IRunnableFactory {

    private final Context mContext;
    private static IRunnableFactory sInstance = null;

    public static IRunnableFactory createNewFactory(Context ctx, Handler handler) {
        if (sInstance != null) {
            return sInstance;
        } else {
            return new RunnableFactory(ctx, handler);
        }
    }

    private RunnableFactory(Context ctx, Handler handler) {
        if (ctx == null || handler == null) {
            throw new IllegalArgumentException("No argument can be null");
        }
        mContext = ctx;
        MessageManager.createNewMessageManager(handler);
    }

    // TODO All runnable should have the same constructor args and manage
    // their intent data within their own class.
    public Runnable build(Intent intent) {
        if (intent != null && intent.getAction() != null) {
            String intentAction = intent.getAction();
            String[] token = intentAction.split("\\.", 0);
            String command = token[token.length - 1];
            Action action = Action.getActionFromValue(intentAction);
            int actionId = Action.getActionId(action);
            switch (action) {
                case SET_DEBUG_ON_ACTION:
                    SetDebugRunnable setDebug = new SetDebugRunnable(intent, actionId);
                    return new LogRunnable(setDebug, command);
                default:
            }
        }
        // Unknown intent do nothing.
        // TODO this should not return null but rather an Unknown runnable instead
        return null;
    }

    private boolean isInt(String val){
        String reg = "\\A[-]?[0-9]+\\z";
        Matcher m1 = Pattern.compile(reg).matcher(val);
        return m1.find();
    }

    public String getIntentAction(Message msg) {
        int actionId = MessageManager.getInstance().getIdFromMessage(msg);
        Action action = Action.getActionFromId(actionId);
        return action.getActionValue();
    }

    public boolean getActionResult(Message msg) {
        return MessageManager.getInstance().getResultFromMessage(msg);
    }

    public Intent getOriginalIntent(Message msg) {
        return MessageManager.getInstance().getIntentFromMessage(msg);
    }
}