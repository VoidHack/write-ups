# __Sharif CTF 8__ 
## _Barnamak_

## Information
**Category:** | **Points:** | **Writeup Author**
--- | --- | ---
Reverse | 200 | merrychap

**Description:** 

> Run the application and capture the flag!

## Solution
### Decompiling
We are given with apk file. First of all, we have to decompile it. I used [jadx](https://github.com/skylot/jadx) for this, but you can use whatever tool you want. Okay, let's break into the code!

<p align="center">
  <img src="screens/classes.png">
</p>

### Code reversing
As we can see, this apk is some challenge service where we have to pass 2 checks (as said in the ```Resourses/res/values/strings.xml```).

There are many different classes: network availability checker, some views and fragments (it's a kind of subview), SMS sender, and others.

The interesting class here is ```ChallengeFragmentOnClickListener```. It tells us what is going on when we click on Challenge button.

<!-- <script src="https://gist.github.com/merrychap/30b7b3d724bb99daedaf526b7d81e4c7.js"></script> -->
```java
public class ChallengeFragmentOnClickListener implements OnClickListener {
    private Context context;
    private ChallengeFragment fragment;

    public ChallengeFragmentOnClickListener(ChallengeFragment fragment, Context context) {
        this.fragment = fragment;
        this.context = context;
        PackageManager pm = context.getPackageManager();
        String strPhone = "XXXXXXXXXXX";
        ArrayList messageParts = SmsManager.getDefault().divideMessage("1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890TEST");
        Context curContext = context.getApplicationContext();
        int partsCount = messageParts.size();
        ArrayList sentPendings = new ArrayList(partsCount);
        ArrayList deliveredPendings = new ArrayList(partsCount);
        for (int i = 1; i < partsCount; i++) {
            PendingIntent sentPending = PendingIntent.getBroadcast(curContext, 0, new Intent("SENT"), 0);
            curContext.registerReceiver(new BroadcastReceiver() {
                public void onReceive(Context arg0, Intent arg1) {
                    switch (getResultCode()) {
                    }
                }
            }, new IntentFilter("SENT"));
            sentPendings.add(sentPending);
            PendingIntent deliveredPending = PendingIntent.getBroadcast(curContext, 0, new Intent("DELIVERED"), 0);
            curContext.registerReceiver(new BroadcastReceiver() {
                public void onReceive(Context arg0, Intent arg1) {
                    switch (getResultCode()) {
                    }
                }
            }, new IntentFilter("DELIVERED"));
            deliveredPendings.add(deliveredPending);
        }
    }

    public void onClick(View view) {
        View parent = (View) view.getParent().getParent();
        switch (view.getId()) {
            case R.id.challenge_button_check:
                if (this.fragment.b()) {
                    this.fragment.a();
                    return;
                }
                return;
            default:
                return;
        }
    }

    public boolean isInternetAvailable() {
        try {
            if (InetAddress.getByName("google.com").equals("")) {
                return false;
            }
            return true;
        } catch (Exception e) {
            return false;
        }
    }
}
```

### Checks 
```ChallengeFragmentOnClickListener``` class has ```ChallengeFragment``` field, about which we will tell later. In the onClick function happen the next checks:

```java
private ChallengeFragment fragment;

[...]

if (this.fragment.b()) {
    this.fragment.a();
    return;
}
```

Let's explore ```ChallengeFragment``` class for understanding above ```a``` and ```b``` functions:

<!-- <script src="https://gist.github.com/merrychap/a5143e10e5fee69e193bb875e5fcba6b.js"></script> -->

```java
public class ChallengeFragment extends Fragment implements LocationListener {
    private Context context;
    private Location location;
    private LocationManager locationManager;
    private TextView textViewLatitude;
    private TextView textViewLatitude1;
    private TextView textViewLongitude;
    View view;

    public void onActivityCreated(Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
    }

    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        this.view = inflater.inflate(R.layout.fragment_challenge, container, false);
        ((Button) this.view.findViewById(R.id.challenge_button_check)).setOnClickListener(new ChallengeFragmentOnClickListener(this, getContext()));
        this.textViewLatitude = (TextView) this.view.findViewById(R.id.TextView_A);
        this.textViewLongitude = (TextView) this.view.findViewById(R.id.TextView_B);
        this.textViewLatitude.setText(" Waiting ");
        this.textViewLongitude.setText("For A Lock...");
        LocationManager mLocationManager = (LocationManager) getContext().getSystemService("location");
        return this.view;
    }

    public void onStart() {
        super.onStart();
        this.context = getActivity().getApplicationContext();
        this.locationManager = (LocationManager) this.context.getSystemService("location");
    }

    public void onResume() {
        super.onResume();
        if (ContextCompat.checkSelfPermission(this.context, "android.permission.ACCESS_FINE_LOCATION") == 0 || ContextCompat.checkSelfPermission(this.context, "android.permission.ACCESS_COARSE_LOCATION") == 0) {
            this.locationManager.requestLocationUpdates("gps", 1000, 1000.0f, this);
        }
    }

    public void onPause() {
        super.onPause();
        this.locationManager.removeUpdates(this);
    }

    public boolean b() {
        Integer i = Integer.valueOf(Integer.parseInt("2C", 16));
        int aat = i.intValue() + 1;
        int bbt = (-Integer.valueOf(Integer.parseInt("5B", 16)).intValue()) - 2;
        if (this.location == null) {
            return false;
        }
        if (((int) this.location.getLatitude()) == aat && ((int) this.location.getLongitude()) == bbt) {
            ((Vibrator) this.context.getSystemService("vibrator")).hasVibrator();
            Toast.makeText(this.context, getString(R.string.string_a), 0).show();
            return true;
        }
        Toast.makeText(this.context, getString(R.string.string_b), 0).show();
        return false;
    }

    public void onLocationChanged(Location location) {
        if (location != null) {
            this.textViewLatitude.setText(" " + location.getLatitude());
            this.textViewLongitude.setText(" " + location.getLongitude());
        } else {
            this.textViewLatitude.setText("A: N/A");
            this.textViewLongitude.setText("B: N/A");
        }
        this.location = location;
    }

    public void onStatusChanged(String s, int i, Bundle bundle) {
    }

    public void onProviderEnabled(String s) {
    }

    public void onProviderDisabled(String s) {
    }

    private static String iia(int[] input, String key) {
        String output = "";
        for (int i = 0; i < input.length; i++) {
            output = output + ((char) ((input[i] - 48) ^ key.charAt(i % (key.length() - 1))));
        }
        return output;
    }

    public void a() {
        AlertDialog alertDialog = new Builder(getActivity().getWindow().getContext()).create();
        alertDialog.setTitle("Root Alert ! ");
        alertDialog.setMessage("This program is at risk of root access,you should immediately exit the application.");
        alertDialog.setButton(-1, "OK", new OnClickListener() {
            public void onClick(DialogInterface context, int which) {
                if (c.a() || c.b() || c.c()) {
                    int[] aa1 = new int[]{147, 146, 71, 53, 172, 150, 128, 117, 124, 141, 164, 118, 173, 163, 172, 139, 159, 173, 166, 114, 125, 137, 60, 112, 135, 136, 152, 112, 172, 153, 136, TransportMediator.KEYCODE_MEDIA_PAUSE, 151, 172, 175, 79, 134, 136, 75, 116, 135, 115, 135, TransportMediator.KEYCODE_MEDIA_RECORD, 125, 55, 147, 116, 157, 55, 168, TransportMediator.KEYCODE_MEDIA_PLAY, 134, 76, 158, 52, 124, 163, 125, 75, 173, 164, 67, 57};
                    String Res = ChallengeFragment.iia(new int[]{162, 136, 133, 131, 68, 141, 119, 68, 169, 160, 49, 68, 171, TransportMediator.KEYCODE_MEDIA_RECORD, 68, 168, 139, 138, 131, 112, 141, 113, 128, 129}, String.valueOf((int) Math.round(ChallengeFragment.this.location.getLatitude())));
                    Toast.makeText(ChallengeFragment.this.getActivity().getBaseContext(), Res, 0).show();
                    ChallengeFragment.this.textViewLatitude1 = (TextView) ChallengeFragment.this.view.findViewById(R.id.TextView_C);
                    ChallengeFragment.this.textViewLatitude1.setText(Res);
                    System.exit(0);
                }
            }
        });
        alertDialog.setOnDismissListener(new OnDismissListener() {
            public void onDismiss(DialogInterface dialogInterface) {
                System.exit(0);
            }
        });
        alertDialog.show();
    }
}
```

First of all, let's start with ```b``` function. It checks the location of a device. So, it gives us the knowledge of the correct location. 
```
location.getLatitude()  == 45
location.getLongitude() == -93
```

The next function is ```a```. A little bit more complex, but still readable. As we know, if ```b``` check is True, then ```a``` happens.

```java
if (c.a() || c.b() || c.c()) {
```

The code of ```c``` class is placed below:

<!-- <script src="https://gist.github.com/merrychap/7d294863a03dc9fabc8ba3908dbd129d.js"></script> -->

```java
public class c {
    public static boolean a() {
        for (String file : System.getenv("PATH").split(":")) {
            if (new File(file, "su").exists()) {
                return true;
            }
        }
        return false;
    }

    public static boolean b() {
        String s = Build.TAGS;
        if (s == null || !s.contains("test-keys")) {
            return false;
        }
        return true;
    }

    public static boolean c() {
        for (String file : new String[]{"/system/app/Superuser.apk", "/system/xbin/daemonsu", "/system/etc/init.d/99SuperSUDaemon", "/system/bin/.ext/.su", "/system/etc/.has_su_daemon", "/system/etc/.installed_su_daemon", "/dev/com.koushikdutta.superuser.daemon/"}) {
            if (new File(file).exists()) {
                return true;
            }
        }
        return false;
    }
}
```

Functions of this class check if we can get root privilege on a device. So, if we can, then happens the next:

```java
String Res = ChallengeFragment.iia(new int[]{162, 136, 133, 131, 68, 141, 119, 68, 169, 160, 49, 68, 171, TransportMediator.KEYCODE_MEDIA_RECORD, 68, 168, 139, 138, 131, 112, 141, 113, 128, 129}, String.valueOf((int) Math.round(ChallengeFragment.this.location.getLatitude())));

Toast.makeText(ChallengeFragment.this.getActivity().getBaseContext(), Res, 0).show();
```

It's obviuos that ```iia``` function is some kind of decoding. So, if we execute this, then we will get the next message ```Flag is MD5 O Longtiude```. As we know, ```location.getLongitude() == -93```, so we have to just get md5 hash of "-93". Alright, that's all folks.


> SharifCTF{87a20a335768a82441478f655afd95fe}

<p align="center">
  <img src="screens/thats_all_folks.jpg">
</p>