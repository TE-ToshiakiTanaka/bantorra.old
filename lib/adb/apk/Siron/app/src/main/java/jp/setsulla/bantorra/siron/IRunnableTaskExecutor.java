package jp.setsulla.bantorra.siron;

/**
 * Created by setsulla on 2015/11/03.
 */

public interface IRunnableTaskExecutor {
    void submitTask(Runnable runnable);
    void submitTaskFirst(Runnable runnable);
    void execute() throws IllegalThreadStateException;
    void shutdown();
    void clearTasks();
    boolean hasTasks();
}