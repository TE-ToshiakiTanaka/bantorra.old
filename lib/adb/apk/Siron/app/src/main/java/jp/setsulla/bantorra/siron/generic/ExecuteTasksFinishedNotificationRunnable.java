package jp.setsulla.bantorra.siron.generic;

import jp.setsulla.bantorra.siron.Action;
import jp.setsulla.bantorra.siron.MessageManager;

/**
 * Created by setsulla on 2015/11/03.
 */
public class ExecuteTasksFinishedNotificationRunnable implements Runnable {
    public static final String MSG_EXECUTE_TASKS_DONE = "jp.setsulla.bantorra.siron.MSG_EXECUTE_TASKS_DONE";
    private int startId;
    private int actionId;

    public ExecuteTasksFinishedNotificationRunnable(int startId) {
        this.startId = startId;
        Action action = Action.getActionFromValue(MSG_EXECUTE_TASKS_DONE);
        actionId = Action.getActionId(action);
    }

    @Override
    public void run() {
        MessageManager.getInstance().sendMessage(actionId, startId);
    }
}