package jp.setsulla.bantorra.lascall;

import com.android.uiautomator.testrunner.UiAutomatorTestCase;

import android.graphics.Point;
import android.os.Bundle;
import android.os.RemoteException;

import java.util.StringTokenizer;

public class Lascall extends UiAutomatorTestCase {
    public enum PRESS {
        HOME("home"),
        ENTER("enter"),
        MENU("menu"),
        RECENT("recent"),
        SEARCH("search"),
        BACK("back"),
        UNKNOWN("unknown");

        private final String str;
        private PRESS(String str){ this.str = str; }
        public String String(){ return this.str; }

        public static PRESS get(String str){
            for(PRESS p: PRESS.values()){
                if(str.equals(p.String())){
                    return p;
                }
            }
            return UNKNOWN;
        }
    }

    public void press() throws RemoteException {
        Bundle args = this.getParams();
        String key = args.getString("key");
        PRESS p = PRESS.get(key);
        assertNotNull(p);
        switch(p){
            case HOME: assertTrue(getUiDevice().pressHome()); break;
            case BACK: assertTrue(getUiDevice().pressBack()); break;
            case MENU: assertTrue(getUiDevice().pressMenu()); break;
            case ENTER: assertTrue(getUiDevice().pressEnter()); break;
            case RECENT: assertTrue(getUiDevice().pressRecentApps()); break;
            case SEARCH: assertTrue(getUiDevice().pressSearch()); break;
            default: System.out.println("Error");
        }
    }

    public void wakeup() throws RemoteException{
        getUiDevice().wakeUp();
    }

    public void swipe(){
        Bundle args = this.getParams();
        String x_str = args.getString("x");
        String y_str = args.getString("y");
        StringTokenizer x = new StringTokenizer(x_str, ",");
        StringTokenizer y = new StringTokenizer(y_str, ",");
        assertTrue(x.countTokens() == y.countTokens());
        Point[] point = new Point[x.countTokens()];
        int i = 0;
        while(x.hasMoreTokens()){
            point[i] = new Point(
                    Integer.parseInt(x.nextToken()), Integer.parseInt(y.nextToken()));
            i++;
        }
        assertTrue(getUiDevice().swipe(point, 10));
    }

    public void tap(){
        Bundle args = this.getParams();
        int x = args.getInt("x");
        int y = args.getInt("y");
        assertTrue(getUiDevice().click(x, y));
    }

    public void notification(){
        assertTrue(getUiDevice().openNotification());
    }

    public void quicksettings(){
        assertTrue(getUiDevice().openQuickSettings());
    }
}
