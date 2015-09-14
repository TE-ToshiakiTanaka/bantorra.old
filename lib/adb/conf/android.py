class Android:
    # adb get property
    PROP_LANGUAGE = "persist.sys.language"
    PROP_COUNTRY = "persist.sys.country"
    PROP_BOOT_COMPLETED = "sys.boot_completed"
    PROP_SIM_STATE = "gsm.sim.state"

    # adb shell dumpsys category
    CATEGORY_POWER = "power"
    CATEGORY_INPUT = "input"
    CATEGORY_WIFI = "wifi"
    CATEGORY_AUDIO = "audio"
    CATEGORY_STATUSBAR = "statusbar"
    CATEGORY_ACTIVITY = "activity activities"

    # dumpsys value
