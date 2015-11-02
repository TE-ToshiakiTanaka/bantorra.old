package jp.setsulla.bantorra.siron.debug;

/**
 * Created by setsulla on 2015/11/03.
 */
public class Debug {
    private Debug() {}
    private volatile static boolean isUserDebugEnabled = true;
    private static boolean isDevelopmentDebugEnabled = true;

    public static boolean isUserEnabled() {
        return isUserDebugEnabled || isDevelopmentDebugEnabled;
    }

    public static boolean isDevelopmentEnabled() {
        return isDevelopmentDebugEnabled;
    }

    public synchronized static void setUserDebug(boolean isEnabled) {
        isUserDebugEnabled = isEnabled;
    }
}